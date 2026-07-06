#!/usr/bin/env python3
"""
skill-optimizer — CLI for semantic and functional skill auditing.
Orchestrates phases 0-8, delegates LLM analysis via resolve_model.py,
generates dual report (file + stdout JSON).

Usage:
    python skill_optimizer.py --batch DIR
    python skill_optimizer.py --skill NAME --skills-dir DIR
    python skill_optimizer.py --batch DIR --apply [--interactive]
    python skill_optimizer.py --batch DIR --threshold 0.7
"""
import argparse
import json
import subprocess
import sys
import yaml
from pathlib import Path

from skill_optimizer_lib import (
    is_core_skill,
    VALID_TIERS,
    load_skill,
    validate_frontmatter,
    check_required_sections,
    check_section_quality,
    check_dry_run,
    check_external_clis,
    resolve_tier_optimal,
    detect_legacy_format,
    compute_structural_score,
    compute_script_score,
    find_duplicates,
    generate_recommendations,
    create_snapshot,
    restore_snapshot,
    generate_report,
    write_report_markdown,
)


# ---------------------------------------------------------------------------
# LLM Delegation (Phase 2)
# ---------------------------------------------------------------------------

ANALYSIS_CRITERIA_TEMPLATE = """Evaluate this skill against these 7 dimensions.
For each dimension, provide a score (0.0-1.0) and a one-line justification.

## Dimensions
1. Intent vs Reality: Do triggers + description predict actual invocation?
2. Minimal Path: Do phases have redundant steps? Can they be collapsed?
3. Decision Points: Where does the LLM decide vs just format? Does it justify the tier?
4. Failure Modes: Do guardrails cover real failures?
5. External Coupling: CLI dependencies without version pinning/fallback?
6. Testability: Is output objectively verifiable? Associated test?
7. Token Efficiency: Are compact rules concise? Noise in prompt?

## Skill Content
Name: {name}
Description: {description}
Model Tier: {model_tier}

### Body
{body}

## Response Format (JSON only)
{{
  "intent_vs_reality": {{"score": 0.0, "justification": "..."}},
  "minimal_path": {{"score": 0.0, "justification": "..."}},
  "decision_points": {{"score": 0.0, "justification": "..."}},
  "failure_modes": {{"score": 0.0, "justification": "..."}},
  "external_coupling": {{"score": 0.0, "justification": "..."}},
  "testability": {{"score": 0.0, "justification": "..."}},
  "token_efficiency": {{"score": 0.0, "justification": "..."}}
}}
"""


def resolve_model(tier: str, execution_dir: Path) -> str:
    """Get model string for a given tier via resolve_model.py."""
    resolve_script = execution_dir / "resolve_model.py"
    if not resolve_script.exists():
        return ""
    try:
        result = subprocess.run(
            [sys.executable, str(resolve_script), tier],
            capture_output=True, text=True, timeout=10,
        )
        data = json.loads(result.stdout.strip())
        if data.get("status") == "success":
            return data["data"]["model"]
    except Exception:
        pass
    return ""


def run_functional_analysis(skill: dict, execution_dir: Path) -> dict:
    """Phase 2: Delegate functional analysis to LLM.

    Returns a dict with dimension scores and an aggregate functional_score.
    If LLM delegation fails, returns zeroed scores with a note.
    """
    fm = skill.get("frontmatter", {})
    prompt = ANALYSIS_CRITERIA_TEMPLATE.format(
        name=fm.get("name", skill.get("name", "?")),
        description=fm.get("description", ""),
        model_tier=fm.get("model_tier", "not set"),
        body=skill.get("body", "")[:4000],  # Truncate to avoid token limits
    )

    model = resolve_model("high", execution_dir)
    if not model:
        return {
            "functional_score": 0.0,
            "dimensions": {},
            "note": "LLM delegation unavailable — resolve_model.py not found or failed",
        }

    # Delegate to LLM via llm_client.py
    llm_script = execution_dir / "llm_client.py"
    if not llm_script.exists():
        return {
            "functional_score": 0.0,
            "dimensions": {},
            "note": "llm_client.py not found",
        }
        
    try:
        # Prompt needs to be passed safely. Since it's long, we can pass it via stdin or args.
        # But for atomic scripts, sys.argv is easier. We will just pass it.
        # However, passing 4k tokens via sys.argv can cause 'argument list too long' on Windows.
        # Let's pass it via stdin.
        result = subprocess.run(
            [sys.executable, "-c", f"""
import sys, json
from llm_client import query_llm
model = sys.argv[1]
prompt = sys.stdin.read()
res = query_llm(model, prompt)
print(json.dumps(res) if res else json.dumps({{"error": "API query failed"}}))
            """, model],
            input=prompt,
            capture_output=True, text=True, timeout=300,
            cwd=str(execution_dir),
            encoding="utf-8"
        )
        # Parse LLM response
        try:
            response = json.loads(result.stdout.strip())
        except json.JSONDecodeError:
            return {
                "functional_score": 0.0,
                "dimensions": {},
                "note": f"LLM error: Invalid JSON. Stderr: {result.stderr.strip()}",
            }
            
        if "error" in response:
            return {
                "functional_score": 0.0,
                "dimensions": {},
                "note": f"LLM error: {response['error']}. Stderr: {result.stderr.strip()}",
            }

        # If we get actual dimension scores, compute aggregate
        dimensions = {}
        total_score = 0.0
        count = 0
        for key in [
            "intent_vs_reality", "minimal_path", "decision_points",
            "failure_modes", "external_coupling", "testability", "token_efficiency",
        ]:
            if key in response:
                dim_score = float(response[key].get("score", 0))
                dimensions[key] = {
                    "score": dim_score,
                    "justification": response[key].get("justification", ""),
                }
                total_score += dim_score
                count += 1
                
        # Calculate functional score out of 1.0 (7 criteria)
        functional_score = round(total_score / count, 2) if count > 0 else 0.0
        
        return {
            "functional_score": functional_score,
            "dimensions": dimensions,
            "note": "LLM functional analysis completed" if count > 0 else "LLM analysis returned invalid schema",
        }
    except Exception as e:
        return {
            "functional_score": 0.0,
            "dimensions": {},
            "note": f"LLM delegation failed: {e}",
        }


# ---------------------------------------------------------------------------
# Skill Analysis Pipeline
# ---------------------------------------------------------------------------

def analyze_skill(skill_name: str, skills_dir: Path, execution_dir: Path) -> dict:
    """Run full analysis pipeline on a single skill (Phases 1-3, 5-6)."""
    skill_path = skills_dir / skill_name
    skill = load_skill(skill_path)

    if not skill:
        return {
            "skill": skill_name,
            "error": "No SKILL.md found or unreadable",
            "structural_score": 0.0,
            "functional_score": 0.0,
            "script_candidate": False,
            "script_score": 0.0,
            "script_needs_review": False,
            "tier_actual": "not set",
            "tier_optimal": "medium",
            "legacy_format": True,
            "is_core": is_core_skill(skill_name),
            "recommendations": [f"[Structural] Skill '{skill_name}' has no readable SKILL.md"],
        }

    fm = skill["frontmatter"]
    body = skill["body"]
    tier_actual = skill["model_tier"]

    # Phase 1: Structural analysis
    fm_validation = validate_frontmatter(fm)
    sections = check_required_sections(body)
    section_quality = check_section_quality(body, sections)
    has_dry_run = check_dry_run(body)
    external_clis = check_external_clis(skill["content"])
    is_legacy = detect_legacy_format(body, fm)
    structural_score = compute_structural_score(sections, has_dry_run, fm_validation)

    # Phase 2: Functional analysis (LLM delegation)
    functional_result = run_functional_analysis(skill, execution_dir)

    # Phase 3: Script candidate
    script_info = compute_script_score(body, skill_name)

    # Tier resolution
    tier_info = resolve_tier_optimal(skill_name, body)

    # Phase 6: Consolidated recommendations
    recs = generate_recommendations(
        skill_name=skill_name,
        sections=sections,
        section_quality=section_quality,
        has_dry_run=has_dry_run,
        fm_validation=fm_validation,
        tier_actual=tier_actual,
        tier_info=tier_info,
        script_info=script_info,
        external_clis=external_clis,
        is_legacy=is_legacy,
    )

    return {
        "skill": skill_name,
        "structural_score": structural_score,
        "functional_score": functional_result["functional_score"],
        "functional_note": functional_result.get("note", ""),
        "script_candidate": script_info["is_candidate"],
        "script_score": script_info["score"],
        "script_reason": script_info["reason"],
        "script_needs_review": script_info.get("needs_agent_review", False),
        "tier_actual": tier_actual or "not set",
        "tier_optimal": tier_info["tier_optimal"],
        "tier_source": tier_info["source"],
        "tier_inferred": tier_info.get("inferred_tier", ""),
        "legacy_format": is_legacy,
        "is_core": is_core_skill(skill_name),
        "has_dry_run": has_dry_run,
        "sections": sections,
        "section_quality": section_quality,
        "external_clis": external_clis,
        "fm_validation": fm_validation,
        "recommendations": recs,
    }


# ---------------------------------------------------------------------------
# Skill Discovery
# ---------------------------------------------------------------------------

def find_all_skills(base_dir: Path) -> list[str]:
    """List all skills (directories containing SKILL.md) in a directory."""
    if not base_dir.exists():
        return []
    return sorted(
        d.name for d in base_dir.iterdir()
        if d.is_dir() and (d / "SKILL.md").exists()
    )


# ---------------------------------------------------------------------------
# Auto-Fix (Phase 8)
# ---------------------------------------------------------------------------

def apply_safe_fixes(
    skill_name: str,
    skills_dir: Path,
    interactive: bool = False,
) -> list[str]:
    """Apply safe auto-fixes to a skill. Returns list of changes made.

    Safe fixes:
      - Fix model_tier if invalid value

    DRY-RUN is NOT auto-injected — it's optional per the style guide.
    Destructive fixes (always require confirmation):
      - Script extraction
      - Legacy migration
    """
    changes: list[str] = []

    # Core/meta skill guard
    if is_core_skill(skill_name):
        return [f"SKIP: {skill_name} — core/meta skill, never auto-fixed"]

    skill_file = skills_dir / skill_name / "SKILL.md"

    if not skill_file.exists():
        return [f"SKIP: {skill_name} — no SKILL.md"]

    content = skill_file.read_text(encoding="utf-8")

    # No automatic DRY-RUN injection — it's optional per the style guide.
    # Skills that need it will have it; skills that don't shouldn't be forced.

    return changes


def validate_post_fix(
    skill_name: str,
    skills_dir: Path,
    pre_sections: dict | None = None,
) -> bool:
    """Validate that a skill is still parseable AND was not degraded by auto-fix.

    The old version of this check only confirmed the file still parsed as
    YAML+body — which is true for almost any edit, so the rollback logic
    that depends on it almost never fired. This version additionally
    confirms no section that was present before the fix went missing
    after it.
    """
    skill = load_skill(skills_dir / skill_name)
    if skill is None:
        return False

    if pre_sections:
        sections_after = check_required_sections(skill["body"])
        lost = [k for k, v in pre_sections.items() if v and not sections_after.get(k, False)]
        if lost:
            return False

    return True


# ---------------------------------------------------------------------------
# Legacy Migration (Phase 8a)
# ---------------------------------------------------------------------------

def is_already_good(skill_name: str, skills_dir: Path) -> bool:
    """Return True if skill is within budget and has valid structure.

    Skills that are already well-structured should NOT be migrated,
    even if they technically trigger legacy detection. This prevents
    over-optimization of clean skills.
    """
    skill = load_skill(skills_dir / skill_name)
    if not skill:
        return False

    body = skill["body"]
    fm = skill.get("frontmatter", {})

    # Must have frontmatter
    if not fm:
        return False

    # Count approximate tokens (word count)
    token_count = len(body.split())

    # If within style guide budget (target 180-450, hard max 1000)
    # and has at least 2 of 4 required sections, it's good enough
    if token_count <= 1000:
        sections = check_required_sections(body)
        present = sum(1 for v in sections.values() if v)
        if present >= 2:
            return True

    return False


# Mapping from legacy section patterns to modern template sections
# Aligned with skill-style-guide.md: Activation Contract, Hard Rules,
# Execution Steps, Output Contract.
LEGACY_SECTION_MAP = {
    r"(?:When to use|Triggers|Cuándo usar)": "## Activation Contract",
    r"(?:Requirements|Dependencies|Dependencias)": "## Prerequisites",
    r"(?:Steps|Workflow|Pasos|Flujo)": "## Execution Steps",
    r"(?:Rules|Constraints|Reglas|Restricciones|Guardrails)": "## Hard Rules",
    r"(?:Examples|Commands|Ejemplos|Comandos|Response Format|Output Format)": "## Output Contract",
}


def migrate_legacy_skill(
    skill_name: str,
    skills_dir: Path,
    generator_model: str = "unknown",
    interactive: bool = False,
) -> list[str]:
    """Phase 8a: Migrate a legacy-format skill to the modern template.

    This is a DESTRUCTIVE operation — always requires confirmation.
    Overwrites the original SKILL.md with the migrated content.

    Returns list of changes made.
    """
    import re

    changes: list[str] = []
    skill_path = skills_dir / skill_name
    skill = load_skill(skill_path)

    if not skill:
        return [f"SKIP: {skill_name} — no SKILL.md"]

    body = skill["body"]
    fm = skill["frontmatter"]

    # Complexity filter: skip sdd-*/skill-* core skills and sub-agent delegation
    if is_core_skill(skill_name):
        return [f"SKIP: {skill_name} — core/meta skill, requires manual rewrite"]

    if re.search(r"\b(sub-agent|subagent|invoke_subagent)\b", body, re.IGNORECASE):
        return [f"SKIP: {skill_name} — delegates to sub-agents, requires manual rewrite"]

    # Build new frontmatter
    new_fm = {
        "name": fm.get("name", skill_name),
        "description": fm.get("description", f"Migrated skill: {skill_name}"),
        "version": fm.get("version", "1.0.0"),
        "author": fm.get("author", "unknown"),
        "generator_model": generator_model,
        "model_tier": fm.get("model_tier", "medium"),
        "inherited_from": skill["path"],
        "migrated_by": "skill-optimizer@3.2.0",
    }

    # Validate model_tier
    if new_fm["model_tier"] not in VALID_TIERS:
        new_fm["model_tier"] = "medium"
        changes.append(f"Fixed invalid model_tier → medium")

    # Semantic mapping: remap old sections to new template
    mapped_sections: dict[str, str] = {}
    residue_blocks: list[str] = []

    # Split body into sections by ## headings
    section_splits = re.split(r"(?=^##\s)", body, flags=re.MULTILINE)

    for block in section_splits:
        block = block.strip()
        if not block:
            continue

        mapped = False
        for legacy_pattern, modern_heading in LEGACY_SECTION_MAP.items():
            if re.search(rf"^##\s+{legacy_pattern}", block, re.IGNORECASE | re.MULTILINE):
                # Extract content after the heading
                content_lines = block.split("\n", 1)
                content = content_lines[1].strip() if len(content_lines) > 1 else ""
                if modern_heading not in mapped_sections:
                    mapped_sections[modern_heading] = content
                else:
                    mapped_sections[modern_heading] += "\n" + content
                mapped = True
                changes.append(f"Mapped '{block.split(chr(10))[0][:50]}' → {modern_heading}")
                break

        if not mapped and block.startswith("##"):
            # Check if it already matches a modern heading
            is_modern = False
            for modern in LEGACY_SECTION_MAP.values():
                if block.startswith(modern):
                    heading_line = block.split("\n", 1)
                    content = heading_line[1].strip() if len(heading_line) > 1 else ""
                    mapped_sections[modern] = content
                    is_modern = True
                    break

            if not is_modern:
                residue_blocks.append(block)
        elif not mapped and not block.startswith("##"):
            # Non-section content (preamble, etc.)
            if block.strip():
                residue_blocks.append(block)

    # Build the new SKILL.md
    fm_yaml = yaml.dump(new_fm, default_flow_style=False, allow_unicode=True, sort_keys=False)
    new_content = f"---\n{fm_yaml}---\n\n"

    # Write sections in template order, preserving unmapped sections
    section_order = [
        "## Activation Contract",
        "## Prerequisites",
        "## Execution Steps",
        "## Hard Rules",
        "## Output Contract",
    ]

    for heading in section_order:
        content = mapped_sections.get(heading, "")
        new_content += f"{heading}\n"
        if content:
            new_content += content + "\n"
        # No TODO placeholders — empty sections are left empty or omitted
        new_content += "\n"

    # Preserve unmapped sections (don't丢弃 content into "Migration Residue")
    if residue_blocks:
        for block in residue_blocks:
            new_content += block + "\n\n"
        changes.append(f"Preserved {len(residue_blocks)} unmapped section(s) as-is")

    # Confirm before writing (ALWAYS for destructive ops)
    if interactive:
        print(f"\n  Legacy migration for {skill_name}:", file=sys.stderr)
        for c in changes:
            print(f"    - {c}", file=sys.stderr)
        response = input(f"  Apply migration to {skill_name}? [y/N]: ").strip().lower()
        if response != "y":
            return [f"SKIP (user declined migration): {skill_name}"]

    # Write
    skill_file = skill_path / "SKILL.md"
    skill_file.write_text(new_content, encoding="utf-8")
    changes.append(f"MIGRATED: {skill_name} → modern template")

    return changes


# ---------------------------------------------------------------------------
# Main CLI
# ---------------------------------------------------------------------------

PENDING_REVIEW_FILENAME = "pending-script-review.json"
ANALYSIS_STATE_FILENAME = "analysis-state.json"


def save_analysis_state(output_dir: Path, results: list, duplicates: list) -> None:
    """Persist the full analysis so a later --resolve-pending invocation
    (a separate process — no shared memory) can patch and finalize it."""
    state_path = output_dir / ANALYSIS_STATE_FILENAME
    state_path.write_text(
        json.dumps({"results": results, "duplicates": duplicates}, indent=2),
        encoding="utf-8",
    )


def load_analysis_state(output_dir: Path) -> tuple[list, list]:
    state_path = output_dir / ANALYSIS_STATE_FILENAME
    if not state_path.exists():
        raise FileNotFoundError(
            f"{state_path} not found — run --batch or --skill first, "
            f"--resolve-pending only finalizes an existing analysis"
        )
    data = json.loads(state_path.read_text(encoding="utf-8"))
    return data["results"], data["duplicates"]


def build_pending_review(results: list, body_by_skill: dict[str, str], output_dir: Path) -> list:
    """Collect skills whose script-candidacy score landed in the gray
    zone into a small reviewable manifest, and write it to disk. The
    orchestrating agent (whatever invoked this script — Claude, Gemini,
    a human at a terminal) reads this file, judges each item itself —
    no API key, no second model — and answers via --resolve-pending.
    """
    pending = []
    for r in results:
        if r.get("script_needs_review") and not r.get("is_core"):
            sname = r["skill"]
            pending.append({
                "skill": sname,
                "score": r.get("script_score"),
                "reason": r.get("script_reason"),
                "body_excerpt": body_by_skill.get(sname, "")[:600],
                "question": (
                    "Does this skill genuinely need an LLM's judgment, or is it "
                    "a deterministic transformation a plain script could do "
                    "identically every time? Answer in your reply, then re-run "
                    "with: python skill_optimizer.py --resolve-pending "
                    "--output-dir <dir> and pipe a JSON answers object via stdin: "
                    '{"<skill>": {"is_candidate": true|false, "reasoning": "<short>"}}'
                ),
            })

    if pending:
        pending_path = output_dir / PENDING_REVIEW_FILENAME
        pending_path.write_text(json.dumps(pending, indent=2), encoding="utf-8")

    return pending


def resolve_pending_review(output_dir: Path, answers: dict) -> dict:
    """Phase 3b: Finalize gray-zone script-candidacy verdicts using the
    orchestrating agent's own judgment (passed in as `answers`) — no
    network call, no API key. Patches the persisted analysis, rewrites
    the report, and clears the pending manifest once every item it
    covers is resolved.
    """
    results, duplicates = load_analysis_state(output_dir)
    result_map = {r["skill"]: r for r in results}

    resolved = []
    still_pending = []
    pending_path = output_dir / PENDING_REVIEW_FILENAME
    pending_items = json.loads(pending_path.read_text(encoding="utf-8")) if pending_path.exists() else []

    for item in pending_items:
        sname = item["skill"]
        answer = answers.get(sname)
        if answer is None:
            still_pending.append(item)
            continue
        r = result_map.get(sname)
        if r is None:
            still_pending.append(item)
            continue
        r["script_candidate"] = bool(answer.get("is_candidate", r["script_candidate"]))
        r["script_needs_review"] = False
        r["script_reason"] = f"Agent-resolved: {answer.get('reasoning', '')}".strip()
        resolved.append(sname)

    # Rewrite report + state with patched results
    report_path = output_dir / "skill-audit-report.md"
    write_report_markdown(results, duplicates, report_path)
    save_analysis_state(output_dir, results, duplicates)

    if still_pending:
        pending_path.write_text(json.dumps(still_pending, indent=2), encoding="utf-8")
    elif pending_path.exists():
        pending_path.unlink()

    script_candidates = [r for r in results if r.get("script_candidate") and not r.get("is_core")]
    tier_mismatches = [
        r for r in results
        if r.get("tier_actual", "") not in ("not set", "") and r.get("tier_actual") != r.get("tier_optimal")
    ]

    return {
        "report_path": str(report_path),
        "skills_analyzed": len(results),
        "script_candidates": len(script_candidates),
        "tier_mismatches": len(tier_mismatches),
        "duplicates": len(duplicates),
        "legacy_format": sum(1 for r in results if r.get("legacy_format")),
        "resolved_pending": resolved,
        "still_pending": [item["skill"] for item in still_pending],
    }


def cleanup_skill(skill_name: str, skills_dir: Path, interactive: bool = False) -> list[str]:
    """Remove bloat from a skill without restructuring.

    Cleans:
      1. Injected DRY-RUN blocks (the generic 5-line blockquote)
      2. TODO placeholders ("TODO: Fill in this section", "TODO: Add specific triggers")
      3. Duplicate DRY-RUN blocks (keep only the first)
      4. Empty Prerequisites sections (only checkmarks, no real content)

    Does NOT:
      - Change headings or section names
      - Restructure content
      - Add or remove sections
      - Modify the frontmatter

    Returns list of changes made.
    """
    import re

    changes: list[str] = []
    skill_file = skills_dir / skill_name / "SKILL.md"

    if not skill_file.exists():
        return [f"SKIP: {skill_name} — no SKILL.md"]

    content = skill_file.read_text(encoding="utf-8")
    original = content

    # 1. Remove injected DRY-RUN blocks (the generic blockquote)
    # Pattern: blockquote starting with [UNIVERSAL DRY-RUN / SIMULATION RULE]
    dry_run_pattern = re.compile(
        r'\n?>\s*\*\*\[UNIVERSAL DRY-RUN / SIMULATION RULE\]\*\*\n'
        r'(?:>\s*.*\n)*'
        r'(?:>\s*\n)*',
        re.MULTILINE,
    )
    matches = dry_run_pattern.findall(content)
    if matches:
        # Remove all but keep track
        content = dry_run_pattern.sub('\n', content)
        changes.append(f"Removed {len(matches)} DRY-RUN block(s)")

    # 2. Remove TODO placeholders
    todo_patterns = [
        r'\n\s*-\s*TODO:\s*Add specific triggers for this skill\s*\n',
        r'\n\s*\*TODO:\s*Fill in this section\.\*\s*\n',
        r'\n\s*TODO:\s*Fill in this section\.?\s*\n',
    ]
    for pattern in todo_patterns:
        todo_matches = re.findall(pattern, content, re.IGNORECASE)
        if todo_matches:
            content = re.sub(pattern, '\n', content, flags=re.IGNORECASE)
            changes.append(f"Removed {len(todo_matches)} TODO placeholder(s)")

    # 3. Remove duplicate DRY-RUN lines (keep only first occurrence)
    dry_run_line_pattern = re.compile(
        r'^(\s*>?\s*(?:DRY-RUN|dry-run|dry_run).*$)',
        re.MULTILINE | re.IGNORECASE,
    )
    lines = content.split('\n')
    seen_dry_run = False
    cleaned_lines = []
    removed_duplicates = 0
    for line in lines:
        if dry_run_line_pattern.match(line):
            if seen_dry_run:
                removed_duplicates += 1
                continue
            seen_dry_run = True
        cleaned_lines.append(line)
    if removed_duplicates:
        content = '\n'.join(cleaned_lines)
        changes.append(f"Removed {removed_duplicates} duplicate DRY-RUN line(s)")

    # 4. Remove empty Prerequisites sections (only checkmarks, no real content)
    prereq_pattern = re.compile(
        r'(?:^##\s+(?:Prerequisites|Requirements)\s*\n)'
        r'((?:\s*-\s*\[[ x]\]\s*.*\n)*)'
        r'(\s*\n)',
        re.MULTILINE,
    )
    prereq_match = prereq_pattern.search(content)
    if prereq_match:
        prereq_content = prereq_match.group(1).strip()
        # Check if it's only checkmarks with no real content
        lines = [l.strip() for l in prereq_content.split('\n') if l.strip()]
        all_checkmarks = all(re.match(r'^-\s*\[[ x]\]', l) for l in lines)
        if all_checkmarks and len(lines) <= 5:
            content = content[:prereq_match.start()] + '\n' + content[prereq_match.end():]
            changes.append(f"Removed empty Prerequisites section ({len(lines)} checkmarks)")

    # 5. Clean up excessive blank lines (3+ consecutive → 2)
    content = re.sub(r'\n{4,}', '\n\n\n', content)

    # Write if changed
    if content != original:
        if interactive:
            print(f"\n  Cleanup for {skill_name}:", file=sys.stderr)
            for c in changes:
                print(f"    - {c}", file=sys.stderr)
            response = input(f"  Apply cleanup to {skill_name}? [y/N]: ").strip().lower()
            if response != "y":
                return [f"SKIP (user declined): {skill_name}"]

        skill_file.write_text(content, encoding="utf-8")
        changes.insert(0, f"CLEANED: {skill_name}")

    return changes


def main():
    parser = argparse.ArgumentParser(
        description="skill-optimizer: Semantic and functional skill auditing",
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--batch", type=str, help="Directory of skills to audit")
    group.add_argument("--skill", type=str, help="Individual skill name to audit")

    parser.add_argument(
        "--skills-dir", type=str,
        help="Base directory for skills (used with --skill). Defaults to --batch value.",
    )
    parser.add_argument(
        "--apply", action="store_true",
        help="Execute safe auto-fixes (creates backup first)",
    )
    parser.add_argument(
        "--interactive", action="store_true",
        help="Require [y/N] confirmation per skill when applying fixes",
    )
    parser.add_argument(
        "--threshold", type=float, default=0.6,
        help="Script candidate threshold (default: 0.6)",
    )
    parser.add_argument(
        "--output-dir", type=str, default=".config",
        help="Directory for output files (default: .config)",
    )
    parser.add_argument(
        "--execution-dir", type=str, default=None,
        help="Directory containing resolve_model.py (default: same as this script)",
    )
    parser.add_argument(
        "--resolve-pending", action="store_true",
        help=(
            "Finalize gray-zone script-candidacy verdicts from a previous "
            "--batch/--skill run. Reads a JSON answers object from stdin: "
            '{"<skill>": {"is_candidate": true|false, "reasoning": "<short>"}}. '
            "No network call — uses --output-dir to locate the prior analysis."
        ),
    )
    parser.add_argument(
        "--cleanup", action="store_true",
        help=(
            "Remove bloat from skills: injected DRY-RUN blocks, TODO placeholders, "
            "duplicate DRY-RUN rules, empty Prerequisites sections. Does NOT "
            "restructure — preserves original content and headings."
        ),
    )

    args = parser.parse_args()

    if args.resolve_pending:
        output_dir = Path(args.output_dir)
        try:
            answers = json.loads(sys.stdin.read())
        except json.JSONDecodeError as e:
            print(json.dumps({"status": "error", "data": None, "error_log": f"Invalid JSON on stdin: {e}"}))
            sys.exit(1)
        try:
            output_data = resolve_pending_review(output_dir, answers)
        except FileNotFoundError as e:
            print(json.dumps({"status": "error", "data": None, "error_log": str(e)}))
            sys.exit(1)
        print(json.dumps({"status": "success", "data": output_data, "error_log": ""}))
        return

    # Resolve directories
    if args.batch:
        skills_dir = Path(args.batch)
    elif args.skill and args.skills_dir:
        skills_dir = Path(args.skills_dir)
    elif args.skill:
        # Default: look in parent's agent-config/skills
        skills_dir = Path.cwd()
    else:
        print(json.dumps({
            "status": "error",
            "data": None,
            "error_log": "Must specify --batch DIR or --skill NAME --skills-dir DIR",
        }))
        sys.exit(1)

    if not skills_dir.exists():
        print(json.dumps({
            "status": "error",
            "data": None,
            "error_log": f"Skills directory not found: {skills_dir}",
        }))
        sys.exit(1)

    execution_dir = Path(args.execution_dir) if args.execution_dir else Path(__file__).parent
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Resolve skill list
    if args.skill:
        skills_to_scan = [args.skill]
    else:
        skills_to_scan = find_all_skills(skills_dir)

    if not skills_to_scan:
        print(json.dumps({
            "status": "error",
            "data": None,
            "error_log": f"No skills found in {skills_dir}",
        }))
        sys.exit(1)

    # ---- Phase 8 pre-step: Snapshot if --apply ----
    backup_path = None
    if args.apply:
        try:
            backup_path = create_snapshot(skills_dir, output_dir)
        except Exception as e:
            print(json.dumps({
                "status": "error",
                "data": None,
                "error_log": f"Failed to create backup: {e}",
            }))
            sys.exit(1)

    # ---- Phases 1-3, 5-6: Analysis ----
    results = []
    loaded_skills = []
    body_by_skill: dict[str, str] = {}
    for sname in skills_to_scan:
        result = analyze_skill(sname, skills_dir, execution_dir)
        results.append(result)

        # Also load skill for duplicate detection + pending-review excerpts
        skill_data = load_skill(skills_dir / sname)
        if skill_data:
            loaded_skills.append(skill_data)
            body_by_skill[sname] = skill_data["body"]

    # ---- Phase 4: Duplicate detection ----
    duplicates = find_duplicates(loaded_skills, threshold=args.threshold)

    # ---- Phase 3b: Gray-zone script-candidacy review manifest ----
    # No network call here. Skills whose heuristic score is genuinely
    # ambiguous get written to a small file for the orchestrating agent
    # (whatever is running this script right now) to judge itself, then
    # finalize via --resolve-pending. See resolve_pending_review() above.
    pending_items = build_pending_review(results, body_by_skill, output_dir)

    # ---- Phase 7: Report ----
    report_path = output_dir / "skill-audit-report.md"
    write_report_markdown(results, duplicates, report_path)

    # ---- Phase 8: Auto-fix (if --apply) ----
    fix_log: list[str] = []
    if args.apply:
        result_map = {r["skill"]: r for r in results}
        
        for sname in skills_to_scan:
            changes = []
            is_legacy = result_map.get(sname, {}).get("legacy_format", False)
            
            if is_legacy:
                # Don't migrate skills that are already well-structured
                if is_already_good(sname, skills_dir):
                    fix_log.append(f"SKIP: {sname} — already within budget, not migrated")
                else:
                    changes.extend(migrate_legacy_skill(sname, skills_dir, interactive=args.interactive))
            
            # Apply safe fixes
            safe_changes = apply_safe_fixes(sname, skills_dir, interactive=args.interactive)
            # Filter out skip messages if we already made migration changes
            if changes and any("SKIP" in c for c in safe_changes):
                safe_changes = [c for c in safe_changes if "SKIP" not in c]
            changes.extend(safe_changes)
                
            if changes:
                fix_log.extend(changes)

            # Validate post-fix
            if changes and not any("SKIP" in c for c in changes):
                if not validate_post_fix(sname, skills_dir, pre_sections=result_map.get(sname, {}).get("sections")):
                    fix_log.append(f"ROLLBACK: {sname} — post-fix validation failed")
                    if backup_path:
                        # Restore just this skill from backup
                        import shutil
                        backup_skill = backup_path / sname
                        target_skill = skills_dir / sname
                        if backup_skill.exists():
                            shutil.rmtree(target_skill)
                            shutil.copytree(backup_skill, target_skill)
                            fix_log.append(f"RESTORED: {sname} from backup")

    # ---- Phase 8b: Cleanup (if --cleanup) ----
    if args.cleanup:
        for sname in skills_to_scan:
            changes = cleanup_skill(sname, skills_dir, interactive=args.interactive)
            if changes:
                fix_log.extend(changes)

    # ---- Output ----
    script_candidates = [
        r for r in results
        if r.get("script_candidate") and not r.get("is_core")
    ]
    tier_mismatches = [
        r for r in results
        if r.get("tier_actual", "") not in ("not set", "")
        and r.get("tier_actual") != r.get("tier_optimal")
    ]

    # Persist full analysis so --resolve-pending (a separate process,
    # no shared memory) can patch and finalize it later.
    save_analysis_state(output_dir, results, duplicates)

    output_data = {
        "report_path": str(report_path),
        "skills_analyzed": len(results),
        "script_candidates": len(script_candidates),
        "tier_mismatches": len(tier_mismatches),
        "duplicates": len(duplicates),
        "legacy_format": sum(1 for r in results if r.get("legacy_format")),
    }

    if pending_items:
        output_data["pending_review"] = {
            "count": len(pending_items),
            "path": str(output_dir / PENDING_REVIEW_FILENAME),
            "note": (
                "Some script-candidacy verdicts are ambiguous. Read the items "
                "at 'path', judge each yourself, then run with --resolve-pending "
                "and pipe your answers as JSON via stdin."
            ),
        }

    if backup_path:
        output_data["backup_path"] = str(backup_path)
    if fix_log:
        output_data["fix_log"] = fix_log

    print(json.dumps({"status": "success", "data": output_data, "error_log": ""}))


if __name__ == "__main__":
    main()

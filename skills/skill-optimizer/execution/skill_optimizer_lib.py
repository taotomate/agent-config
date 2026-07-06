#!/usr/bin/env python3
"""
skill_optimizer_lib — Core library for skill-optimizer.
Parsing, scoring, heuristics, and report generation.

All path-dependent functions receive paths as parameters.
No hardcoded paths. No global mutable state.
"""
import json
import re
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml


# ---------------------------------------------------------------------------
# Constants (values, not paths)
# ---------------------------------------------------------------------------

VALID_TIERS = {"high", "medium", "fast"}

CORE_SKILLS = {
    "sdd-explore", "sdd-propose", "sdd-spec", "sdd-design",
    "sdd-tasks", "sdd-apply", "sdd-verify", "sdd-archive",
    "sdd-init", "sdd-onboard",
}


def is_core_skill(skill_name: str) -> bool:
    """True if this skill must NEVER be auto-fixed, migrated, or extracted
    by skill-optimizer.

    Covers the explicit sdd-* pipeline (CORE_SKILLS) PLUS any skill whose
    name starts with 'skill-' (meta-skills: skill-optimizer, skill-creator,
    skill-migrator, skill-registry, etc.) — per the SKILL.md guardrail:
    "NEVER auto-fix sdd-* or skill-* core skills."

    Bare membership checks against CORE_SKILLS alone do NOT protect
    'skill-optimizer' or 'skill-creator' (they aren't sdd-* and were never
    in that set) — this was a real bug: skill-optimizer could modify or
    migrate itself. Always call this function, not `name in CORE_SKILLS`,
    when deciding whether a skill is touchable.
    """
    return skill_name in CORE_SKILLS or skill_name.startswith("skill-")

SCRIPT_SIGNAL_WEIGHTS = {
    "deterministic_steps": 0.30,
    "external_cli_calls": 0.25,
    "no_llm_judgment": 0.20,
    "pure_transform": 0.15,
    "testable_without_llm": 0.10,
}

# Known tier assignments — fallback when content inference is ambiguous
TIER_FALLBACK_MAP: dict[str, str] = {
    "sdd-propose": "high",
    "sdd-design": "high",
    "sdd-spec": "medium",
    "sdd-explore": "medium",
    "sdd-tasks": "medium",
    "sdd-apply": "medium",
    "sdd-verify": "medium",
    "sdd-archive": "fast",
    "sdd-init": "medium",
    "sdd-onboard": "medium",
    "skill-creator": "high",
    "skill-optimizer": "fast",
    "cognitive-doc-design": "high",
    "thread-dossier": "high",
    "skill-migrator": "fast",
    "skill-registry": "fast",
    "comment-writer": "fast",
    "issue-creation": "fast",
    "go-testing": "fast",
    "fast-file-locator": "fast",
    "auditor": "medium",
}

# CLIs that are real external dependencies (not the runtime itself)
EXTERNAL_CLI_PATTERNS: list[str] = [
    r"\byt-dlp\b",
    r"\bffmpeg\b",
    r"\bgh\b",
    r"\bjq\b",
    r"\bcurl\b",
    r"\bwget\b",
    r"\bnode\b",
    r"\byoutube[._-]transcript\b",
    r"\bdocker\b",
    r"\bkubectl\b",
]

# Patterns that indicate LLM delegation in phase text
LLM_PHASE_INDICATORS = [
    r"\bLLM\s+Delegation\b",
    r"\bHigh\s*[-–—]\s*LLM\b",
    r"\bdelegate\s+to\s+(a\s+)?model\b",
    r"\bsemantic\s+analysis\b",
    r"\bLLM\s+Synthesis\b",
    r"\bresolve_model\b",
]

# Patterns that indicate mechanical/local phases
MECHANICAL_PHASE_INDICATORS = [
    r"\bFast\s*[-–—]\s*(grep|glob|read|local|script)\b",
    r"\bInline\s*[-–—]\s*(grep|glob|read)\b",
    r"\bLocal\s+Script\b",
]

# Required sections in a skill — aligned with skill-style-guide.md.
# Each canonical name maps to acceptable heading variants.
# The style guide defines: Activation Contract, Hard Rules, Decision Gates,
# Execution Steps, Output Contract, References. We accept legacy names too
# so existing skills aren't flagged just for using different headings.
REQUIRED_SECTIONS: dict[str, list[str]] = {
    "Activation Contract": [
        "Activation Contract", "When to Use", "When to use",
        "Context & Triggers", "Triggers",
    ],
    "Hard Rules": [
        "Hard Rules", "Guardrails", "Guardrails (Critical Rules)",
        "Rules", "Constraints",
    ],
    "Execution Steps": [
        "Execution Steps", "Execution Phases", "Steps", "Workflow",
    ],
    "Output Contract": [
        "Output Contract", "Response Format", "Output Format",
    ],
}


# ---------------------------------------------------------------------------
# Frontmatter Parsing (YAML-based)
# ---------------------------------------------------------------------------

def parse_frontmatter(content: str) -> dict[str, Any]:
    """Parse YAML frontmatter from a SKILL.md file.

    Returns a dict with keys: frontmatter (dict), body (str), raw (str).
    If no frontmatter is found, returns empty frontmatter.
    """
    if not content.startswith("---"):
        return {"frontmatter": {}, "body": content, "raw": content}

    end_idx = content.find("---", 3)
    if end_idx == -1:
        return {"frontmatter": {}, "body": content, "raw": content}

    fm_text = content[3:end_idx].strip()
    body = content[end_idx + 3:].strip()

    try:
        fm = yaml.safe_load(fm_text) or {}
    except yaml.YAMLError:
        fm = {}

    return {"frontmatter": fm, "body": body, "raw": content}


def validate_frontmatter(fm: dict) -> dict[str, Any]:
    """Validate frontmatter fields and return a validation report.

    Returns dict with:
      - valid (bool): overall validity
      - errors (list[str]): list of error messages
      - warnings (list[str]): list of warning messages
    """
    errors: list[str] = []
    warnings: list[str] = []

    # Required fields
    if not fm.get("name"):
        errors.append("Missing required field: name")
    if not fm.get("description"):
        errors.append("Missing required field: description")

    # model_tier validation
    tier = fm.get("model_tier")
    if not tier:
        errors.append("Missing required field: model_tier")
    elif tier not in VALID_TIERS:
        errors.append(
            f"Invalid model_tier: '{tier}'. Must be one of: {', '.join(sorted(VALID_TIERS))}"
        )

    # version format
    version = fm.get("version", "")
    if not version:
        warnings.append("Missing version field")
    elif not re.match(r"^\d+\.\d+\.\d+", str(version)):
        warnings.append(f"Version '{version}' does not follow semver format (X.Y.Z)")

    # author
    if not fm.get("author"):
        warnings.append("Missing author field")

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
    }


# ---------------------------------------------------------------------------
# Skill Loading
# ---------------------------------------------------------------------------

def load_skill(skill_path: Path) -> dict | None:
    """Load a skill from its directory and parse its SKILL.md.

    Args:
        skill_path: Path to the skill directory (must contain SKILL.md).

    Returns:
        Parsed skill dict or None if SKILL.md not found.
    """
    skill_file = skill_path / "SKILL.md"
    if not skill_file.exists():
        return None

    try:
        content = skill_file.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None

    parsed = parse_frontmatter(content)
    fm = parsed["frontmatter"]

    return {
        "name": fm.get("name", skill_path.name),
        "path": str(skill_file),
        "content": content,
        "body": parsed["body"],
        "frontmatter": fm,
        "model_tier": fm.get("model_tier", ""),
    }


# ---------------------------------------------------------------------------
# Section Checking
# ---------------------------------------------------------------------------

def check_required_sections(body: str) -> dict[str, bool]:
    """Check for presence of required sections.

    Uses flexible matching: a heading like "## General Review Rules"
    matches the "Hard Rules" requirement because it contains "Rules".

    Returns a dict mapping section name → found (bool).
    """
    results: dict[str, bool] = {}
    for section_name, patterns in REQUIRED_SECTIONS.items():
        found = False
        for p in patterns:
            # Flexible match: heading contains the pattern as a word
            if re.search(rf"^##\s+.*?\b{re.escape(p)}\b", body, re.MULTILINE | re.IGNORECASE):
                found = True
                break
            # Also try exact match for backward compatibility
            if re.search(rf"^##\s+{re.escape(p)}", body, re.MULTILINE):
                found = True
                break
        results[section_name] = found
    return results


def check_section_quality(body: str, sections: dict[str, bool]) -> dict[str, str]:
    """Basic quality check on sections that exist.

    Returns a dict mapping section name → quality assessment.
    Possible values: 'missing', 'empty', 'minimal', 'adequate'.
    """
    quality: dict[str, str] = {}

    for section_name, found in sections.items():
        if not found:
            quality[section_name] = "missing"
            continue

        # Find the section content (between this heading and the next ## heading)
        patterns = REQUIRED_SECTIONS[section_name]
        section_body = ""
        for p in patterns:
            # Flexible match: heading contains the pattern as a word
            match = re.search(
                rf"^##\s+.*?\b{re.escape(p)}\b\s*\n(.*?)(?=^##\s|\Z)",
                body,
                re.MULTILINE | re.DOTALL | re.IGNORECASE,
            )
            if match:
                section_body = match.group(1).strip()
                break
            # Also try exact match
            match = re.search(
                rf"^##\s+{re.escape(p)}\s*\n(.*?)(?=^##\s|\Z)",
                body,
                re.MULTILINE | re.DOTALL,
            )
            if match:
                section_body = match.group(1).strip()
                break

        if not section_body:
            quality[section_name] = "empty"
        elif len(section_body.split()) < 8:
            quality[section_name] = "minimal"
        else:
            quality[section_name] = "adequate"

    return quality


def check_dry_run(body: str) -> bool:
    """Check for presence of the universal DRY-RUN rule."""
    return bool(re.search(
        r"\bDRY-RUN\b|\bdry-run\b|\bdry_run\b|\bsimulacro\b",
        body,
        re.IGNORECASE,
    ))


# ---------------------------------------------------------------------------
# External CLI Detection
# ---------------------------------------------------------------------------

_FENCED_CODE_BLOCK_RE = re.compile(r"```.*?```", re.DOTALL)


def check_external_clis(content: str) -> list[str]:
    """Detect external CLI dependencies in skill content.

    Only scans fenced code blocks (```...```), not free prose. A regex
    match against the full document text can't tell "this skill RUNS
    ffmpeg" apart from "this skill explains that it does NOT use
    ffmpeg" — which is exactly the false positive that fired on
    skill-optimizer's own SKILL.md (a sentence explaining it checks
    OTHER skills for ffmpeg/gh usage triggered a false "uses ffmpeg,
    gh" flag). Commands actually run by a skill show up in its code
    blocks (powershell/bash snippets); mentions in prose do not need
    to be flagged.

    Filters out false positives like 'python' used as runtime.
    """
    code_blocks = _FENCED_CODE_BLOCK_RE.findall(content)
    code_text = "\n".join(code_blocks).lower()

    found: list[str] = []
    for pattern in EXTERNAL_CLI_PATTERNS:
        if re.search(pattern, code_text):
            clean_name = pattern.replace(r"\b", "").replace("[._-]", "-")
            found.append(clean_name)
    return found


# ---------------------------------------------------------------------------
# Tier Inference
# ---------------------------------------------------------------------------

def infer_tier_from_content(body: str) -> str:
    """Infer the optimal model tier by analyzing phase annotations.

    Counts LLM-delegation phases vs mechanical phases to determine
    the complexity level required.

    Returns: 'high', 'medium', or 'fast'.
    """
    llm_phase_count = 0
    mechanical_phase_count = 0

    # Count phases with LLM delegation indicators
    for pattern in LLM_PHASE_INDICATORS:
        llm_phase_count += len(re.findall(pattern, body, re.IGNORECASE))

    # Count mechanical/local phases
    for pattern in MECHANICAL_PHASE_INDICATORS:
        mechanical_phase_count += len(re.findall(pattern, body, re.IGNORECASE))

    total_phases = llm_phase_count + mechanical_phase_count

    if total_phases < 2:
        # Not enough signal to trust a ratio — a single incidental mention
        # (e.g. a filename like 'resolve_model' referenced in a "known
        # limitations" note, not an actual delegated phase) shouldn't be
        # able to swing the tier on its own. Fall back to medium, the
        # same "can't infer" default used when total_phases == 0.
        return "medium"

    llm_ratio = llm_phase_count / total_phases

    if llm_ratio >= 0.4:
        return "high"
    elif llm_ratio == 0 and mechanical_phase_count > 0:
        return "fast"
    else:
        return "medium"


def resolve_tier_optimal(skill_name: str, body: str) -> dict[str, Any]:
    """Resolve the optimal tier for a skill using content inference + fallback map.

    Returns a dict with:
      - tier_optimal (str): the recommended tier
      - source (str): 'inferred' or 'fallback_map' or 'default'
      - inferred_tier (str | None): what content analysis suggests
    """
    inferred = infer_tier_from_content(body)

    # If we have a known mapping, use it as authoritative but report mismatch
    if skill_name in TIER_FALLBACK_MAP:
        fallback = TIER_FALLBACK_MAP[skill_name]
        return {
            "tier_optimal": fallback,
            "source": "fallback_map",
            "inferred_tier": inferred,
        }

    # No known mapping — use inference
    if inferred != "medium":
        # Inference gave a strong signal (not the default)
        return {
            "tier_optimal": inferred,
            "source": "inferred",
            "inferred_tier": inferred,
        }

    # Default when nothing specific is found
    return {
        "tier_optimal": "medium",
        "source": "default",
        "inferred_tier": inferred,
    }


# ---------------------------------------------------------------------------
# Legacy Format Detection
# ---------------------------------------------------------------------------

def detect_legacy_format(body: str, frontmatter: dict) -> bool:
    """Detect if a skill uses legacy format (pre-v2.0).

    Legacy indicators:
      - No YAML frontmatter
      - Missing Hard Rules section (or legacy name: Guardrails, Rules, etc.)

    DRY-RUN is NOT a legacy indicator — many skills don't need it
    (code review, research, documentation). The style guide does not
    require it.
    """
    if not frontmatter:
        return True

    sections = check_required_sections(body)
    if not sections.get("Hard Rules", False):
        return True

    return False


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

def compute_structural_score(
    sections: dict[str, bool],
    has_dry_run: bool,
    fm_validation: dict[str, Any],
) -> float:
    """Compute structural compliance score (0.0 – 1.0).

    Weights:
      - Section presence: 60%
      - Section count (all present): 10% bonus
      - Frontmatter validity: 30%

    DRY-RUN is NOT scored — it's optional per the style guide.
    """
    section_count = sum(1 for v in sections.values() if v)
    total_sections = len(sections) if sections else 1
    section_ratio = section_count / total_sections

    all_sections_bonus = 0.1 if section_count == total_sections else 0.0
    fm_score = 0.3 if fm_validation.get("valid", False) else 0.0

    # Partial credit for frontmatter with only warnings (no errors)
    if not fm_validation.get("valid") and not fm_validation.get("errors"):
        fm_score = 0.2

    return round(section_ratio * 0.6 + all_sections_bonus + fm_score, 2)


def compute_script_score(body: str, skill_name: str) -> dict[str, Any]:
    """Compute script candidate score using phase analysis.

    Instead of naive regex on keywords, analyzes phase annotations
    to determine how much of the skill is mechanical vs LLM-dependent.

    Returns dict with:
      - score (float): 0.0–1.0
      - is_candidate (bool): score > threshold
      - signals (dict): individual signal results
      - reason (str): human-readable explanation
      - needs_agent_review (bool): True when the score lands in the gray
        zone (0.3–0.6) — genuinely ambiguous, neither a confident "yes"
        nor a confident "no". These cases are NOT escalated to an
        external LLM API: the orchestrating agent (the one already
        running this skill — Claude, Gemini, whatever invoked the
        script) judges them itself in a second pass via
        --resolve-pending. No API key, no network call, no second
        model — just the agent that's already in the loop.
    """
    # sdd-*/skill-* skills are never script candidates (pipeline cohesion)
    if is_core_skill(skill_name):
        return {
            "score": 0.0,
            "is_candidate": False,
            "signals": {},
            "reason": "Core/meta skill — pipeline cohesion, never extractable",
            "needs_agent_review": False,
        }

    # Count phase types
    llm_count = 0
    mechanical_count = 0
    for pattern in LLM_PHASE_INDICATORS:
        llm_count += len(re.findall(pattern, body, re.IGNORECASE))
    for pattern in MECHANICAL_PHASE_INDICATORS:
        mechanical_count += len(re.findall(pattern, body, re.IGNORECASE))

    total = llm_count + mechanical_count
    external_clis = check_external_clis(body)

    # Same principle as infer_tier_from_content: don't let a single
    # incidental mention decide the verdict in either direction.
    #   - One stray mechanical-phrase mention + the body simply not using
    #     one of a handful of "judgment" words was enough to score a
    #     skill as a script candidate even when it genuinely needs
    #     judgment (false positive).
    #   - One incidental mention of an LLM-phrase (e.g. a comparison
    #     aside: "unlike X, which does semantic analysis...") was enough
    #     to zero out every mechanical signal for a skill that's
    #     actually 100% deterministic (false negative).
    if total < 2:
        return {
            "score": 0.0,
            "is_candidate": False,
            "signals": {},
            "reason": "Insufficient phase annotations to judge — not enough signal either way",
            "needs_agent_review": False,
        }

    # Broader than the original decide/choose/evaluate/assess list, which
    # under-counted real judgment language (e.g. "determine the best
    # approach", "use your judgment") and biased the score toward
    # false-positive script candidates.
    judgment_words = re.search(
        r"\b(decide|choose|evaluate|assess|determine|judg(e|ment)|"
        r"interpret|discretion|best approach|use criteria)\b",
        body, re.IGNORECASE,
    )

    # Tolerate incidental LLM-phrase mentions when mechanical evidence
    # clearly dominates, instead of requiring an absolute llm_count == 0.
    # That strict requirement was the actual false-negative bug: one
    # incidental mention (e.g. a comparison aside) was indistinguishable
    # from a real LLM-delegation phase and zeroed out every mechanical
    # signal regardless of how much real mechanical evidence existed
    # alongside it.
    llm_tolerance = mechanical_count // 2
    mechanical_dominant = llm_count <= llm_tolerance

    signals = {
        # Now requires >=2 mechanical mentions, not just >0 — one stray
        # mention of a mechanical-phase phrase isn't enough evidence.
        "deterministic_steps": mechanical_count >= 2 and mechanical_dominant,
        "external_cli_calls": len(external_clis) > 0,
        "no_llm_judgment": mechanical_dominant and not judgment_words,
        "pure_transform": bool(re.search(
            r"\b(format|convert|transform|parse|extract)\b.*\b(json|yaml|csv|markdown)\b",
            body, re.IGNORECASE,
        )),
        "testable_without_llm": (
            mechanical_count >= 2
            and mechanical_dominant
            and not judgment_words
        ),
    }

    score = sum(
        SCRIPT_SIGNAL_WEIGHTS[k] for k, v in signals.items() if v
    )
    score = round(score, 2)

    # Build reason
    if score > 0.6:
        reason = f"High script score ({score}): {mechanical_count} mechanical phases, {llm_count} LLM phases"
    elif total == 0:
        reason = "No phase annotations found — unable to determine"
    else:
        reason = f"Low script score ({score}): {llm_count} LLM phases require agent judgment"

    # Score band where the heuristic itself has weak/conflicting evidence
    # either way. These get flagged for the orchestrating agent to judge
    # in a second pass (--resolve-pending) — not escalated to an external
    # API. Below this band the heuristic's "not a candidate" default is
    # trusted; at/above 0.6 it's already confident ("yes").
    SCRIPT_GRAY_ZONE_LOW, SCRIPT_GRAY_ZONE_HIGH = 0.3, 0.6
    needs_review = SCRIPT_GRAY_ZONE_LOW <= score <= SCRIPT_GRAY_ZONE_HIGH

    return {
        "score": score,
        "is_candidate": score > 0.6,
        "signals": signals,
        "reason": reason,
        "needs_agent_review": needs_review,
    }


# ---------------------------------------------------------------------------
# Duplicate Detection (Jaccard Similarity)
# ---------------------------------------------------------------------------

def tokenize_skill_identity(skill: dict) -> set[str]:
    """Extract identity tokens from a skill for duplicate comparison.

    Uses: triggers, description, and phase names.
    """
    tokens: set[str] = set()
    fm = skill.get("frontmatter", {})
    body = skill.get("body", "")

    # Description tokens
    desc = fm.get("description", "")
    tokens.update(
        w.lower() for w in re.findall(r"\b\w{3,}\b", desc)
    )

    # Trigger tokens (from Activation Contract / Context & Triggers section)
    trigger_match = re.search(
        r"(?:Activation\s+Contract|Context\s*&\s*Triggers|When\s+to\s+[Uu]se|Triggers).*?\n(.*?)(?=^##\s|\Z)",
        body, re.MULTILINE | re.DOTALL | re.IGNORECASE,
    )
    if trigger_match:
        trigger_text = trigger_match.group(1)
        tokens.update(
            w.lower() for w in re.findall(r"\b\w{3,}\b", trigger_text)
        )

    # Phase name tokens
    for phase_match in re.finditer(r"^###\s+(.+)", body, re.MULTILINE):
        tokens.update(
            w.lower() for w in re.findall(r"\b\w{3,}\b", phase_match.group(1))
        )

    return tokens


def compute_jaccard(set_a: set, set_b: set) -> float:
    """Compute Jaccard similarity between two sets."""
    if not set_a and not set_b:
        return 0.0
    intersection = set_a & set_b
    union = set_a | set_b
    return round(len(intersection) / len(union), 3)


def find_duplicates(
    skills: list[dict], threshold: float = 0.7
) -> list[dict[str, Any]]:
    """Find potential duplicate/overlapping skill pairs.

    Returns list of dicts with: skill_a, skill_b, jaccard_score.
    """
    tokenized: list[tuple[str, set[str]]] = []
    for s in skills:
        name = s.get("name", s.get("frontmatter", {}).get("name", "unknown"))
        tokens = tokenize_skill_identity(s)
        tokenized.append((name, tokens))

    duplicates: list[dict[str, Any]] = []
    for i in range(len(tokenized)):
        for j in range(i + 1, len(tokenized)):
            name_a, tokens_a = tokenized[i]
            name_b, tokens_b = tokenized[j]
            score = compute_jaccard(tokens_a, tokens_b)
            if score >= threshold:
                duplicates.append({
                    "skill_a": name_a,
                    "skill_b": name_b,
                    "jaccard_score": score,
                })

    return duplicates


# ---------------------------------------------------------------------------
# Contextual Recommendations
# ---------------------------------------------------------------------------

def generate_recommendations(
    skill_name: str,
    sections: dict[str, bool],
    section_quality: dict[str, str],
    has_dry_run: bool,
    fm_validation: dict[str, Any],
    tier_actual: str,
    tier_info: dict[str, Any],
    script_info: dict[str, Any],
    external_clis: list[str],
    is_legacy: bool,
) -> list[str]:
    """Generate contextual recommendations with specific data from the skill.

    Each recommendation references the analysis dimension that flagged it
    and includes concrete details from the skill being analyzed.
    """
    recs: list[str] = []

    # Frontmatter errors (Structural)
    for err in fm_validation.get("errors", []):
        recs.append(f"[Structural] {err}")

    # Frontmatter warnings
    for warn in fm_validation.get("warnings", []):
        recs.append(f"[Structural] {warn}")

    # Missing sections
    missing = [k for k, v in sections.items() if not v]
    if missing:
        recs.append(
            f"[Structural] Missing required sections: {', '.join(missing)}. "
            f"See template_skill.md for reference structure."
        )

    # Empty or minimal sections
    weak = [k for k, q in section_quality.items() if q in ("empty", "minimal")]
    if weak:
        recs.append(
            f"[Intent vs Reality] Sections present but weak ({', '.join(weak)}). "
            f"A section with <3 lines likely doesn't cover its purpose."
        )

    # DRY-RUN rule — optional, not mandatory
    if not has_dry_run:
        recs.append(
            "[Structural] No DRY-RUN/simulation rule found. "
            "This is optional — only add if the skill involves executable operations."
        )

    # Tier mismatch
    tier_optimal = tier_info.get("tier_optimal", "medium")
    if tier_actual and tier_actual != tier_optimal:
        inferred = tier_info.get("inferred_tier", "?")
        source = tier_info.get("source", "?")
        recs.append(
            f"[Decision Points] Tier mismatch: declared '{tier_actual}', "
            f"optimal '{tier_optimal}' (source: {source}, inferred: {inferred}). "
            f"Review if the skill's phases justify the current tier."
        )

    # Inferred vs fallback disagreement
    inferred = tier_info.get("inferred_tier")
    if (
        inferred
        and tier_info.get("source") == "fallback_map"
        and inferred != tier_optimal
    ):
        recs.append(
            f"[Decision Points] Content analysis infers tier '{inferred}' but "
            f"fallback map says '{tier_optimal}'. Consider updating the map or the skill phases."
        )

    # Script candidate
    if script_info.get("is_candidate") and not is_core_skill(skill_name):
        recs.append(
            f"[Minimal Path] Script candidate (score: {script_info['score']}): "
            f"{script_info['reason']}. "
            f"Consider extracting deterministic logic to execution/ and leaving a thin wrapper."
        )

    # External dependencies
    if external_clis:
        recs.append(
            f"[External Coupling] External CLI dependencies detected: "
            f"{', '.join(external_clis)}. Add version pinning and fallback in Prerequisites."
        )

    # Legacy format
    if is_legacy:
        recs.append(
            "[Structural] Legacy format detected (missing frontmatter or Hard Rules section). "
            "Consider running migration (--apply) to update structure."
        )

    return recs


# ---------------------------------------------------------------------------
# Snapshot / Backup
# ---------------------------------------------------------------------------

def create_snapshot(source_dir: Path, output_dir: Path) -> Path:
    """Create a timestamped backup of the skills directory.

    Returns the path to the backup directory.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = output_dir / f"skill-backup-{timestamp}"
    shutil.copytree(source_dir, backup_dir)
    return backup_dir


def restore_snapshot(backup_dir: Path, target_dir: Path) -> None:
    """Restore a skills directory from a snapshot backup."""
    if not backup_dir.exists():
        raise FileNotFoundError(f"Backup not found: {backup_dir}")
    # Remove current and replace with backup
    if target_dir.exists():
        shutil.rmtree(target_dir)
    shutil.copytree(backup_dir, target_dir)


# ---------------------------------------------------------------------------
# Report Generation
# ---------------------------------------------------------------------------

def generate_report(results: list[dict], duplicates: list[dict]) -> dict:
    """Generate consolidated audit report data."""
    return {
        "skills": results,
        "duplicates": duplicates,
        "generated_at": datetime.now().isoformat(),
        "total": len(results),
    }


def write_report_markdown(
    results: list[dict],
    duplicates: list[dict],
    output_path: Path,
) -> None:
    """Write human-readable audit report to markdown file."""
    script_candidates = [
        r for r in results
        if r.get("script_candidate") and not r.get("is_core")
    ]
    tier_mismatches = [
        r for r in results
        if r.get("tier_actual") and r.get("tier_optimal")
        and r["tier_actual"] != r["tier_optimal"]
    ]
    legacy_skills = [r for r in results if r.get("legacy_format")]

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# Skill Audit Report\n\n")
        f.write(f"**Generated:** {datetime.now().isoformat()}\n")
        f.write(f"**Skills analyzed:** {len(results)}\n")
        f.write(f"**Script candidates:** {len(script_candidates)}\n")
        f.write(f"**Tier mismatches:** {len(tier_mismatches)}\n")
        f.write(f"**Legacy format:** {len(legacy_skills)}\n")
        f.write(f"**Potential duplicates:** {len(duplicates)}\n\n")

        # Summary table
        f.write("## Per-Skill Scorecards\n\n")
        f.write("| Skill | Tier | Structural | Functional | Script | Legacy | Recs |\n")
        f.write("|-------|------|-----------|------------|--------|--------|------|\n")
        for r in sorted(results, key=lambda x: x.get("structural_score", 0)):
            tier_flag = "⚠️" if r.get("tier_actual") != r.get("tier_optimal") else "✓"
            legacy_flag = "🔴" if r.get("legacy_format") else "—"
            rec_count = len(r.get("recommendations", []))
            f.write(
                f"| {r.get('skill', '?')} "
                f"| {tier_flag} {r.get('tier_actual', '?')}→{r.get('tier_optimal', '?')} "
                f"| {r.get('structural_score', 0)} "
                f"| {r.get('functional_score', 0)} "
                f"| {r.get('script_score', 0)} "
                f"| {legacy_flag} "
                f"| {rec_count} |\n"
            )

        # Script candidates
        f.write("\n## Script Candidates\n\n")
        if script_candidates:
            for r in script_candidates:
                f.write(f"- **{r['skill']}** (score: {r['script_score']}): {r.get('script_reason', '')}\n")
        else:
            f.write("None\n")

        # Tier mismatches
        f.write("\n## Tier Mismatches\n\n")
        if tier_mismatches:
            for r in tier_mismatches:
                f.write(f"- **{r['skill']}**: declared={r['tier_actual']} → optimal={r['tier_optimal']}\n")
        else:
            f.write("None\n")

        # Duplicates
        f.write("\n## Potential Duplicates\n\n")
        if duplicates:
            for d in duplicates:
                f.write(f"- **{d['skill_a']}** ↔ **{d['skill_b']}** (Jaccard: {d['jaccard_score']})\n")
        else:
            f.write("None\n")

        # Legacy
        f.write("\n## Legacy Format Skills\n\n")
        if legacy_skills:
            for r in legacy_skills:
                f.write(f"- **{r['skill']}**\n")
        else:
            f.write("None\n")

        # Detailed recommendations
        f.write("\n## Fix Prioritization\n\n")
        for r in sorted(results, key=lambda x: x.get("structural_score", 0)):
            recs = r.get("recommendations", [])
            if recs:
                f.write(f"### {r.get('skill', '?')}\n\n")
                for rec in recs:
                    f.write(f"- {rec}\n")
                f.write("\n")

#!/usr/bin/env python3
r"""
skill_catalog - Scan, hash, deduplicate, and version-track skills across directories.

Usage:
    python skill_catalog.py --scan D:\path\to\skills1 D:\path\to\skills2 ...
    python skill_catalog.py --scan D:\path\to\skills --active-agent-config D:\path\to\agent-config\skills
    python skill_catalog.py --report (markdown report to stdout)
    python skill_catalog.py --json (machine-readable output)
    python skill_catalog.py --cleanup (archive duplicate non-active copies to .skill-archive/)

Outputs:
    - Duplicate groups (same content hash, different locations)
    - Version inventory per skill
    - Active vs archived status
    - Recommendations (which to keep, which to archive)
"""

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

SCAN_EXTENSIONS = {".md"}
SKIP_DIRS = {".git", "__pycache__", ".pytest_cache", ".tmp", "node_modules", "backups"}
ARCHIVE_DIRS = {"archive", "archived", ".bak", "old", "deprecated"}


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------

def parse_frontmatter(content: str) -> dict[str, Any]:
    """Extract YAML frontmatter from a markdown file."""
    if not content.startswith("---"):
        return {}
    end = content.find("---", 3)
    if end == -1:
        return {}
    try:
        return yaml.safe_load(content[3:end].strip()) or {}
    except yaml.YAMLError:
        return {}


def content_hash(content: str) -> str:
    """SHA-256 hash of the file content (normalized: strip trailing whitespace per line)."""
    normalized = "\n".join(line.rstrip() for line in content.splitlines())
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:16]


def extract_skill_name(content: str, path: Path) -> str:
    """Get skill name from frontmatter or fall back to parent directory name."""
    fm = parse_frontmatter(content)
    return fm.get("name", path.parent.name)


def extract_version(content: str) -> str:
    """Get version from frontmatter."""
    fm = parse_frontmatter(content)
    return str(fm.get("version", "unknown"))


def extract_description(content: str) -> str:
    """Get description from frontmatter, truncated to 80 chars."""
    fm = parse_frontmatter(content)
    desc = fm.get("description", "")
    return desc[:80] + "..." if len(desc) > 80 else desc


# ---------------------------------------------------------------------------
# Scanning
# ---------------------------------------------------------------------------

def scan_directory(root: Path) -> list[dict[str, Any]]:
    """Recursively scan a directory for SKILL.md files."""
    results = []
    for skill_file in sorted(root.rglob("SKILL.md")):
        # Skip archived/backup directories
        parts = skill_file.parts
        if any(skip in parts for skip in ARCHIVE_DIRS):
            continue
        if any(skip in parts for skip in SKIP_DIRS):
            continue

        try:
            content = skill_file.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue

        fm = parse_frontmatter(content)
        results.append({
            "path": str(skill_file),
            "parent_dir": str(skill_file.parent),
            "name": extract_skill_name(content, skill_file),
            "version": extract_version(content),
            "description": extract_description(content),
            "hash": content_hash(content),
            "lines": len(content.splitlines()),
            "size_bytes": len(content.encode("utf-8")),
            "frontmatter": fm,
        })
    return results


# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------

def find_duplicates(skills: list[dict]) -> list[list[dict]]:
    """Group skills by content hash. Only groups with 2+ entries are duplicates."""
    by_hash: dict[str, list[dict]] = {}
    for s in skills:
        by_hash.setdefault(s["hash"], []).append(s)
    return [group for group in by_hash.values() if len(group) > 1]


def build_version_map(skills: list[dict]) -> dict[str, list[dict]]:
    """Map skill name → list of all found versions across locations."""
    by_name: dict[str, list[dict]] = {}
    for s in skills:
        by_name.setdefault(s["name"], []).append(s)
    return by_name


def identify_active(skills: list[dict], active_dirs: list[str]) -> list[dict]:
    """Mark skills that live in the active agent-config directories."""
    active_set = set()
    for d in active_dirs:
        active_set.add(str(Path(d).resolve()))

    for s in skills:
        skill_parent = str(Path(s["parent_dir"]).resolve())
        s["is_active"] = any(
            skill_parent == a or skill_parent.startswith(a + "\\")
            for a in active_set
        )
    return skills


def generate_recommendations(
    duplicates: list[list[dict]],
    version_map: dict[str, list[dict]],
    active_dirs: list[str],
) -> list[str]:
    """Generate actionable recommendations."""
    recs = []

    # Duplicate recommendations
    for group in duplicates:
        name = group[0]["name"]
        active = [s for s in group if s.get("is_active")]
        inactive = [s for s in group if not s.get("is_active")]

        if active and inactive:
            active_path = active[0]["parent_dir"]
            inactive_paths = [s["parent_dir"] for s in inactive]
            recs.append(
                f"KEEP active: {name} at {active_path}\n"
                f"  Archive or delete duplicates: {', '.join(inactive_paths)}"
            )
        elif len(group) > 1:
            paths = [s["parent_dir"] for s in group]
            recs.append(
                f"DEDUPE: {name} has {len(group)} identical copies at:\n"
                f"  {chr(10).join('  ' + p for p in paths)}\n"
                f"  Keep one, archive the rest."
            )

    # Version conflict recommendations
    for name, versions in version_map.items():
        unique_versions = set(v["version"] for v in versions)
        if len(unique_versions) > 1:
            active = [v for v in versions if v.get("is_active")]
            active_ver = active[0]["version"] if active else "none"
            recs.append(
                f"VERSION CONFLICT: {name} — active={active_ver}, "
                f"found versions: {', '.join(sorted(unique_versions))}"
            )

    return recs


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def print_report(
    skills: list[dict],
    duplicates: list[list[dict]],
    version_map: dict[str, list[dict]],
    recommendations: list[str],
):
    """Print human-readable markdown report."""
    active_count = sum(1 for s in skills if s.get("is_active"))
    total = len(skills)

    print(f"# Skill Catalog Report")
    print(f"**Generated:** {datetime.now().isoformat()}")
    print(f"**Total skills scanned:** {total}")
    print(f"**Active (in agent-config):** {active_count}")
    print(f"**Duplicate groups:** {len(duplicates)}")
    print(f"**Version conflicts:** {sum(1 for v in version_map.values() if len(set(x['version'] for x in v)) > 1)}")
    print()

    # Active inventory
    print("## Active Skills")
    print("| Skill | Version | Lines | Path |")
    print("|-------|---------|-------|------|")
    for s in sorted(skills, key=lambda x: x["name"]):
        if s.get("is_active"):
            print(f"| {s['name']} | {s['version']} | {s['lines']} | `{s['parent_dir']}` |")
    print()

    # Duplicates
    if duplicates:
        print("## Duplicate Groups (identical content)")
        for i, group in enumerate(duplicates, 1):
            name = group[0]["name"]
            h = group[0]["hash"]
            print(f"### {i}. {name} (hash: {h})")
            for s in group:
                marker = " **[ACTIVE]**" if s.get("is_active") else ""
                print(f"- `{s['parent_dir']}` — v{s['version']}, {s['lines']} lines{marker}")
            print()

    # Recommendations
    if recommendations:
        print("## Recommendations")
        for i, rec in enumerate(recommendations, 1):
            print(f"{i}. {rec}")
            print()


def print_json(
    skills: list[dict],
    duplicates: list[list[dict]],
    version_map: dict[str, list[dict]],
    recommendations: list[str],
):
    """Print machine-readable JSON output."""
    # Strip frontmatter from output (not serializable cleanly)
    clean_skills = [
        {k: v for k, v in s.items() if k != "frontmatter"}
        for s in skills
    ]
    output = {
        "generated_at": datetime.now().isoformat(),
        "total_scanned": len(skills),
        "active_count": sum(1 for s in skills if s.get("is_active")),
        "duplicate_groups": len(duplicates),
        "skills": clean_skills,
        "duplicates": [
            {
                "hash": g[0]["hash"],
                "name": g[0]["name"],
                "locations": [
                    {"path": s["parent_dir"], "version": s["version"], "active": s.get("is_active", False)}
                    for s in g
                ],
            }
            for g in duplicates
        ],
        "version_conflicts": {
            name: list(set(v["version"] for v in versions))
            for name, versions in version_map.items()
            if len(set(v["version"] for v in versions)) > 1
        },
        "recommendations": recommendations,
    }
    print(json.dumps(output, indent=2, ensure_ascii=False))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Skill catalog: scan, hash, deduplicate, track versions.")
    parser.add_argument("--scan", nargs="+", required=True, help="Directories to scan for SKILL.md files")
    parser.add_argument("--active-agent-config", nargs="*", default=[], help="Path(s) to active agent-config skills/ directories")
    parser.add_argument("--json", action="store_true", help="Output JSON instead of markdown")
    parser.add_argument("--save", help="Save report to file instead of stdout")
    parser.add_argument("--cleanup", action="store_true", help="Archive non-active duplicate copies to .skill-archive/")
    parser.add_argument("--dry-run", action="store_true", help="Show what cleanup would do without moving files")
    parser.add_argument("--update-registry", metavar="PATH", help="Generate skill-registry.md at PATH from scanned skills")
    args = parser.parse_args()

    # Scan all directories
    all_skills = []
    for scan_dir in args.scan:
        p = Path(scan_dir)
        if not p.exists():
            print(f"Warning: {scan_dir} does not exist, skipping", file=sys.stderr)
            continue
        all_skills.extend(scan_directory(p))

    if not all_skills:
        print("No SKILL.md files found in any scanned directory.", file=sys.stderr)
        sys.exit(1)

    # Mark active skills
    all_skills = identify_active(all_skills, args.active_agent_config)

    # Analyze
    duplicates = find_duplicates(all_skills)
    version_map = build_version_map(all_skills)
    recommendations = generate_recommendations(duplicates, version_map, args.active_agent_config)

    # Cleanup mode
    if args.cleanup:
        archive_duplicates(duplicates, args.active_agent_config, dry_run=args.dry_run)
        return

    # Update registry mode
    if args.update_registry:
        generate_registry(all_skills, Path(args.update_registry))
        print(f"Registry updated: {args.update_registry}", file=sys.stderr)

    # Output
    if args.save:
        import io
        buf = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = buf
        if args.json:
            print_json(all_skills, duplicates, version_map, recommendations)
        else:
            print_report(all_skills, duplicates, version_map, recommendations)
        sys.stdout = old_stdout
        Path(args.save).write_text(buf.getvalue(), encoding="utf-8")
        print(f"Report saved to {args.save}", file=sys.stderr)
    else:
        if args.json:
            print_json(all_skills, duplicates, version_map, recommendations)
        else:
            print_report(all_skills, duplicates, version_map, recommendations)


def archive_duplicates(duplicates: list[list[dict]], active_dirs: list[str], dry_run: bool = False):
    """Move non-active duplicate skill directories to .skill-archive/."""
    import shutil

    archive_root = Path(".skill-archive")
    moved = 0
    skipped = 0

    for group in duplicates:
        active = [s for s in group if s.get("is_active")]
        inactive = [s for s in group if not s.get("is_active")]

        if not active or not inactive:
            skipped += len(group)
            continue

        for s in inactive:
            src = Path(s["parent_dir"])
            skill_name = src.name
            dest = archive_root / skill_name

            if dry_run:
                print(f"  [DRY RUN] Would archive: {src} -> {dest}")
            else:
                archive_root.mkdir(exist_ok=True)
                if dest.exists():
                    # Already archived, skip
                    print(f"  [SKIP] Already archived: {skill_name}")
                    skipped += 1
                    continue
                shutil.move(str(src), str(dest))
                print(f"  [MOVED] {src} -> {dest}")
            moved += 1

    print(f"\nArchived: {moved} | Skipped: {skipped}")
    if dry_run:
        print("(dry run — no files were actually moved)")


def generate_registry(skills: list[dict], output_path: Path):
    """Generate skill-registry.md from scanned skills."""
    from datetime import datetime

    # Extract trigger from frontmatter description or body
    def get_trigger(skill: dict) -> str:
        fm = skill.get("frontmatter", {})
        desc = fm.get("description", "")
        # Try to extract trigger from description
        if "Trigger:" in desc:
            trigger = desc.split("Trigger:", 1)[1].strip()
            # Remove trailing quotes and dots
            trigger = trigger.strip("\"'").rstrip(".")
            return trigger[:80]  # Truncate long triggers
        # Fallback: use first line of description
        if desc:
            first_line = desc.split("\n")[0].strip()
            return first_line[:80]
        return "N/A"

    lines = []
    lines.append("---")
    lines.append("name: skill-registry")
    lines.append("description: Auto-generated skill registry. Do not edit manually — run skill_catalog.py --update-registry to regenerate.")
    lines.append(f"version: 2.1.0")
    lines.append("author: TaoTomate")
    lines.append("generator_model: mimo-auto")
    lines.append("inherited_from: skill-registry/SKILL.md")
    lines.append("---")
    lines.append("")
    lines.append("# Skill Registry")
    lines.append("")
    lines.append(f"**Auto-generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"**Total skills:** {len(skills)}")
    lines.append("")
    lines.append("## Skills")
    lines.append("")
    lines.append("| Trigger | Skill | Path |")
    lines.append("|---------|-------|------|")

    for s in sorted(skills, key=lambda x: x["name"]):
        trigger = get_trigger(s)
        name = s["name"]
        # Use relative path from agent-config root
        rel_path = s["path"].replace("\\", "/")
        # Try to make relative to skills/ directory
        if "skills/" in rel_path:
            rel_path = "skills/" + rel_path.split("skills/", 1)[1]
        lines.append(f"| {trigger} | {name} | `{rel_path}` |")

    lines.append("")
    lines.append("## Notes")
    lines.append("")
    lines.append("- Auto-generated by `skill_catalog.py --update-registry`")
    lines.append("- Do not edit manually — changes will be overwritten")
    lines.append("- To add a skill: place SKILL.md in skills/ and re-run the script")

    output_path.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
broken_reference_fixer — Scan files for broken references and optionally fix them.

Scans a directory for file references (paths, imports, links) that point to
non-existent files. Generates a JSON report. Can apply conservative fixes
when the replacement is unambiguous.
"""

import argparse
import json
import os
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Reference patterns
# ---------------------------------------------------------------------------

PATTERNS = {
    "hardcoded_path": re.compile(
        r'["\']([A-Za-z]:\\[^"\']+|/[a-z][^"\']+)["\']'
        r'|'
        r'(?<!["\'])([A-Za-z]:\\[\w\\.\-/]+)',
        re.IGNORECASE,
    ),
    "relative_path": re.compile(
        r'["\'](\.{1,2}/[^"\']+)["\']'
        r'|'
        r'(?<!["\'])(\.{1,2}/[\w.\-/]+)',
    ),
    "tilde_path": re.compile(
        r'["\'](~[^"\']+)["\']'
        r'|'
        r'(?<!["\'])(~[\w.\-/]+)',
    ),
    "js_import": re.compile(
        r'(?:require\(["\']([^"\']+)["\']\)|from\s+["\']([^"\']+)["\'])',
    ),
    "markdown_link": re.compile(
        r'\[([^\]]*)\]\(([^)]+)\)',
    ),
    "frontmatter_source": re.compile(
        r'^(?:source|location|depends_on|inherited_from):\s*(.+)$',
        re.MULTILINE,
    ),
}

# Patterns to skip (placeholders, URLs, etc.)
SKIP_PATTERNS = [
    re.compile(r'^/path/to/'),  # placeholder paths
    re.compile(r'^/abs/'),  # arxiv placeholder
    re.compile(r'^https?://'),  # URLs
    re.compile(r'^<[a-z]+://'),  # template URLs
    re.compile(r'^\$'),  # environment variables
    re.compile(r'^<[A-Z_]+>'),  # template variables
]

SKIP_EXTENSIONS = {
    ".pyc", ".pyo", ".so", ".dll", ".exe", ".bin",
    ".json", ".yaml", ".yml", ".toml", ".ini",
    ".gitignore", ".gitkeep", ".DS_Store",
}

SKIP_DIRS = {
    "node_modules", ".git", "__pycache__", ".venv", "venv",
    ".mypy_cache", ".pytest_cache", "dist", "build",
}

# Common Python packages that are NOT local files
PYTHON_PACKAGES = {
    "accelerate", "anthropic", "boto3", "bs4", "click", "datasets",
    "diffusers", "docker", "fastapi", "flask", "google", "grpc",
    "httpx", "huggingface_hub", "jinja2", "json", "jwt", "langchain",
    "litellm", "llama_cpp", "mcp", "numpy", "ollama", "openai",
    "os", "pandas", "pathlib", "pillow", "pydantic", "pytest",
    "qdrant_client", "redis", "requests", "re", "safetensors",
    "scipy", "setuptools", "shutil", "sqlite3", "subprocess",
    "sys", "tempfile", "time", "torch", "transformers", "trl",
    "typer", "typing", "unittest", "urllib", "uuid", "vllm",
    "warnings", "websockets", "yaml", "zlib",
}


# ---------------------------------------------------------------------------
# Scanner
# ---------------------------------------------------------------------------

def scan_file(filepath: Path, base_dir: Path) -> list[dict[str, Any]]:
    """Scan a single file for references."""
    findings = []
    try:
        content = filepath.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return findings

    rel_path = filepath.relative_to(base_dir)
    lines = content.split("\n")

    for line_num, line in enumerate(lines, 1):
        for ref_type, pattern in PATTERNS.items():
            for match in pattern.finditer(line):
                ref_value = match.group(1) or match.group(2) or ""
                if not ref_value or ref_value.startswith("http"):
                    continue
                if ref_type == "frontmatter_source" and "gentleman" in ref_value.lower():
                    continue  # skip inherited_from attribution
                # Skip placeholders, URLs, env vars, templates
                if any(skip.match(ref_value) for skip in SKIP_PATTERNS):
                    continue

                findings.append({
                    "file": str(rel_path),
                    "line": line_num,
                    "reference_type": ref_type,
                    "reference": ref_value,
                    "raw_line": line.strip()[:200],
                })

    return findings


def resolve_reference(ref: str, ref_type: str, file_path: Path, base_dir: Path) -> str | None:
    """Try to resolve a reference to an absolute path."""
    if ref_type == "hardcoded_path":
        p = Path(ref)
        if p.exists():
            return str(p)
        # Check if it's a \tmp\ path (exists on system)
        if ref.startswith("\tmp\"):
            return "system_tmp"
        return None

    if ref_type == "python_import":
        # Skip known Python packages (not local files)
        top_level = ref.split(".")[0].lower()
        if top_level in PYTHON_PACKAGES:
            return "builtin"
        # Only check local imports
        parts = ref.split(".")
        candidate = file_path.parent / ("/".join(parts) + ".py")
        if candidate.exists():
            return str(candidate)
        candidate = file_path.parent / "/".join(parts) / "__init__.py"
        if candidate.exists():
            return str(candidate)
        return None

    if ref_type == "tilde_path":
        expanded = Path(os.path.expanduser(ref))
        if expanded.exists():
            return str(expanded)
        return None

    if ref_type in ("relative_path",):
        resolved = (file_path.parent / ref).resolve()
        if resolved.exists():
            return str(resolved)
        return None

    if ref_type == "js_import":
        if ref.startswith("."):
            resolved = (file_path.parent / ref).resolve()
            for ext in ["", ".js", ".ts", ".mjs", "/index.js", "/index.ts"]:
                if (resolved.parent / (resolved.name + ext)).exists():
                    return str(resolved.parent / (resolved.name + ext))
        return None

    if ref_type == "markdown_link":
        if ref.startswith("http"):
            return None
        resolved = (file_path.parent / ref).resolve()
        return str(resolved) if resolved.exists() else None

    if ref_type == "frontmatter_source":
        resolved = (base_dir / ref).resolve()
        if resolved.exists():
            return str(resolved)
        # Try relative to file
        resolved = (file_path.parent / ref).resolve()
        return str(resolved) if resolved.exists() else None

    return None


def build_file_index(base_dir: Path) -> dict[str, list[Path]]:
    """Build an index of files grouped by stem name for fast candidate lookup."""
    index = {}
    for p in base_dir.rglob("*"):
        if p.is_file() and p.suffix in {".py", ".md", ".ts", ".js", ".sh"}:
            stem = p.stem
            if stem not in index:
                index[stem] = []
            index[stem].append(p)
    return index


def find_candidates(ref: str, file_index: dict[str, list[Path]]) -> list[Path]:
    """Find files with similar names using pre-built index."""
    name = Path(ref).stem if "." in ref else Path(ref).name
    return file_index.get(name, [])[:5]  # limit


# ---------------------------------------------------------------------------
# Fix engine
# ---------------------------------------------------------------------------

# Detect OS and set correct separator
IS_WINDOWS = os.name == "nt"
PATH_SEP = "\\" if IS_WINDOWS else "/"

def normalize_path_seps(ref: str) -> str:
    """Normalize path separators to current OS format."""
    if IS_WINDOWS:
        # Convert forward slashes to backslashes on Windows
        return ref.replace("/", "\\")
    else:
        # Convert backslashes to forward slashes on Linux/Mac
        return ref.replace("\\", "/")

def is_separator_issue(ref: str, resolved: str) -> bool:
    """Check if the only issue is path separator mismatch."""
    normalized = normalize_path_seps(ref)
    return normalized == resolved or Path(normalized).resolve() == Path(resolved).resolve()

def apply_fix(filepath: Path, old_ref: str, new_ref: str, dry_run: bool) -> dict:
    """Apply a fix to a file. Returns fix record."""
    if dry_run:
        return {
            "file": str(filepath),
            "old": old_ref,
            "new": new_ref,
            "status": "would_fix",
        }

    try:
        content = filepath.read_text(encoding="utf-8")
        if old_ref in content:
            new_content = content.replace(old_ref, new_ref, 1)
            # Backup
            backup = filepath.with_suffix(filepath.suffix + ".bak")
            shutil.copy2(filepath, backup)
            filepath.write_text(new_content, encoding="utf-8")
            return {
                "file": str(filepath),
                "old": old_ref,
                "new": new_ref,
                "status": "fixed",
                "backup": str(backup),
            }
    except Exception as e:
        return {
            "file": str(filepath),
            "old": old_ref,
            "new": new_ref,
            "status": "error",
            "error": str(e),
        }
    return {"file": str(filepath), "old": old_ref, "status": "skipped"}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def scan_directory(directory: Path) -> dict:
    """Scan all files in directory for broken references."""
    findings = []
    files_scanned = 0

    for filepath in directory.rglob("*"):
        if not filepath.is_file():
            continue
        if filepath.suffix in SKIP_EXTENSIONS:
            continue
        if any(skip in filepath.parts for skip in SKIP_DIRS):
            continue
        if filepath.suffix not in {".md", ".py", ".js", ".ts", ".sh", ".txt"}:
            continue

        files_scanned += 1
        file_findings = scan_file(filepath, directory)

        for f in file_findings:
            resolved = resolve_reference(
                f["reference"], f["reference_type"], filepath, directory
            )
            f["status"] = "valid" if resolved else "missing"
            if resolved:
                f["resolved_path"] = resolved
            findings.append(f)

    return {
        "scan_date": datetime.now(timezone.utc).isoformat(),
        "directory": str(directory),
        "files_scanned": files_scanned,
        "references_found": len(findings),
        "broken_references": findings,
    }


def fix_references(report: dict, directory: Path, dry_run: bool, apply: bool) -> dict:
    """Attempt to fix broken references based on report, prioritized by frequency."""
    fixes_applied = []
    fixes_suggested = []
    manual_review = []

    # Build file index once for fast candidate lookup
    file_index = build_file_index(directory)

    # Count frequency of each reference
    ref_freq = {}
    for ref in report["broken_references"]:
        key = ref["reference"]
        ref_freq[key] = ref_freq.get(key, 0) + 1

    # Sort by frequency (most common first) for batch processing
    sorted_refs = sorted(report["broken_references"], key=lambda x: ref_freq[x["reference"]], reverse=True)

    # Process in batches of 50
    batch_size = 50
    for i in range(0, len(sorted_refs), batch_size):
        batch = sorted_refs[i:i+batch_size]
        
        for ref in batch:
            filepath = directory / ref["file"]
            if not filepath.exists():
                continue

            # 1. Check if it's just a path separator issue (cross-platform fix)
            normalized = normalize_path_seps(ref["reference"])
            if normalized != ref["reference"]:
                # Check if normalized path exists
                if ref["reference_type"] == "hardcoded_path":
                    check_path = Path(normalized)
                elif ref["reference_type"] == "relative_path":
                    check_path = filepath.parent / normalized
                elif ref["reference_type"] == "markdown_link":
                    check_path = filepath.parent / normalized
                else:
                    check_path = None

                if check_path and check_path.exists():
                    result = apply_fix(filepath, ref["reference"], normalized, dry_run)
                    if result["status"] in ("fixed", "would_fix"):
                        result["reason"] = "separator normalization"
                        result["frequency"] = ref_freq.get(ref["reference"], 1)
                        fixes_applied.append(result)
                        continue

            # 2. Search for candidates on-demand (only during fix)
            candidates = find_candidates(ref["reference"], file_index)

            if len(candidates) == 1:
                # Single candidate — verify compatibility
                candidate_path = candidates[0]
                if filepath.suffix == candidate_path.suffix:
                    result = apply_fix(filepath, ref["reference"], str(candidate_path.relative_to(directory)), dry_run)
                    if result["status"] in ("fixed", "would_fix"):
                        result["reason"] = "candidate match"
                        result["frequency"] = ref_freq.get(ref["reference"], 1)
                        fixes_applied.append(result)
                    else:
                        fixes_suggested.append(result)
                else:
                    manual_review.append({
                        "file": ref["file"],
                        "reason": "type mismatch",
                        "reference": ref["reference"],
                        "candidate": str(candidate_path.relative_to(directory)),
                        "frequency": ref_freq.get(ref["reference"], 1),
                    })
            elif len(candidates) > 1:
                manual_review.append({
                    "file": ref["file"],
                    "reason": "multiple candidates",
                    "reference": ref["reference"],
                    "candidates": [str(c.relative_to(directory)) for c in candidates],
                    "frequency": ref_freq.get(ref["reference"], 1),
                })
            else:
                manual_review.append({
                    "file": ref["file"],
                    "reason": "no candidates found",
                    "reference": ref["reference"],
                    "frequency": ref_freq.get(ref["reference"], 1),
                })

    # Add frequency info to all results
    for item in fixes_applied + fixes_suggested:
        item["frequency"] = ref_freq.get(item.get("old", ""), 1)

    return {
        "fixes_applied": fixes_applied,
        "fixes_suggested": fixes_suggested,
        "manual_review_needed": manual_review,
        "ref_frequency": ref_freq,
    }


def main():
    parser = argparse.ArgumentParser(description="Scan for broken file references")
    parser.add_argument("--scan", type=str, help="Directory to scan")
    parser.add_argument("--file", type=str, help="Single file to scan")
    parser.add_argument("--fix", type=str, help="Directory to fix (with --report)")
    parser.add_argument("--report", type=str, help="JSON report file for fix mode")
    parser.add_argument("--output", type=str, default=".tmp", help="Output directory")
    parser.add_argument("--dry-run", action="store_true", help="Preview fixes without applying")
    parser.add_argument("--apply", action="store_true", help="Apply fixes")
    args = parser.parse_args()

    if args.scan:
        directory = Path(args.scan).resolve()
        if not directory.exists():
            print(f"Error: {directory} does not exist", file=sys.stderr)
            sys.exit(1)

        report = scan_directory(directory)

        output_dir = Path(args.output)
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / "broken-references.json"

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        print(json.dumps({
            "status": "success",
            "report_path": str(output_file),
            "files_scanned": report["files_scanned"],
            "broken_references": len(report["broken_references"]),
        }))

    elif args.fix:
        if not args.report:
            print("Error: --report required with --fix", file=sys.stderr)
            sys.exit(1)

        with open(args.report, "r", encoding="utf-8") as f:
            report = json.load(f)

        directory = Path(args.fix).resolve()
        result = fix_references(report, directory, args.dry_run, args.apply)

        output_file = Path(args.report).with_name("fix-results.json")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        print(json.dumps({
            "status": "success",
            "fixes_applied": len(result["fixes_applied"]),
            "fixes_suggested": len(result["fixes_suggested"]),
            "manual_review": len(result["manual_review_needed"]),
            "report_path": str(output_file),
        }))

    elif args.file:
        filepath = Path(args.file).resolve()
        if not filepath.exists():
            print(f"Error: {filepath} does not exist", file=sys.stderr)
            sys.exit(1)

        findings = scan_file(filepath, filepath.parent)
        print(json.dumps(findings, indent=2, ensure_ascii=False))

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()

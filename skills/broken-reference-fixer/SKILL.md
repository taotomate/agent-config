---
name: broken-reference-fixer
description: "Scans files in a directory for broken references (paths, imports, links) and generates a JSON report with optional conservative auto-fix. Trigger: 'check broken references', 'validate references', 'fix broken links', 'scan references'."
version: "1.0"
author: TaoTomate
model_tier: fast
---

## Context & Triggers

**When to use this skill:**
- When the user wants to verify all file references in a directory are valid
- When cleaning up after renames, moves, or deletions
- Triggers: "check broken references", "validate references", "fix broken links", "scan references"

## Execution Phases

### 1. Diagnosis Phase
- Determine the target directory (default: `skills/`)
- Determine scan scope: all files or specific types

### 2. Action Phase
- Run the scanner script:
  ```bash
  python <skill_dir>/scripts/broken_reference_fixer.py --scan <directory> --output <temp_dir>
  ```
- Review the JSON report

### 3. Verification Phase
- Present findings to user
- For fixes: use `--fix` mode with appropriate flags

## Reference Types Scanned

| Type | Pattern | Example |
|------|---------|---------|
| Hardcoded path | `D:\...\file` or `C:/.../file` | `python D:\path\script.py` |
| Relative path | `./`, `../`, `~` | `@reference/config.md` |
| Python import | `import X`, `from X import` | `import synapse.cli` |
| JS/TS import | `require()`, `from "..." import` | `require("./utils")` |
| Markdown link | `[text](path)` | `[docs](references/setup.md)` |
| Frontmatter field | `source:`, `location:`, `depends_on:` | `source: scripts/helper.py` |

**NOT scanned:** `inherited_from` (attribution only, not functional dependency)

## Commands

```bash
# Scan mode - generates JSON report
python scripts/broken_reference_fixer.py --scan <directory> --output <temp_dir>

# Fix mode - dry run (shows what would change)
python scripts/broken_reference_fixer.py --fix <directory> --report <report.json> --dry-run

# Fix mode - apply conservative fixes only
python scripts/broken_reference_fixer.py --fix <directory> --report <report.json> --apply

# Single file scan
python scripts/broken_reference_fixer.py --file <path_to_file>
```

## Fix Strategy (Conservative)

| Scenario | Action |
|----------|--------|
| Path separator mismatch (`/` vs `\`) | Auto-fix: normalize to current OS format |
| 1 exact match (same name, same relative dir) | Auto-fix + log |
| Multiple matches | Ask user |
| Name match but different content | Report, do not fix |
| No matches | Report for manual intervention |
| Broken relative path | Try to resolve, if fails → report |

## Cross-Platform Support

This skill works on **any OS** (Windows, Linux, macOS):
- Detects current OS automatically
- Normalizes path separators to native format (`\` on Windows, `/` on Linux/Mac)
- First tool to run when migrating skills between platforms

### Pre-fix Verifications
1. File exists at suggested path
2. Same file type (.py → .py, .md → .md)
3. Compatible content (imports match exports)
4. No multiple versions (if >1 candidate, ask user)

## Output Format

```json
{
  "scan_date": "ISO-8601",
  "directory": "scanned path",
  "files_scanned": N,
  "references_found": N,
  "broken_references": [
    {
      "file": "relative/path/to/file",
      "line": N,
      "reference_type": "type",
      "reference": "raw reference string",
      "expected_path": "full expected path",
      "status": "missing|ambiguous|incompatible",
      "suggestion": "description of fix or reason"
    }
  ],
  "fixes_applied": [],
  "fixes_suggested": [],
  "manual_review_needed": []
}
```

## Guardrails (Critical Rules)
- **NEVER** auto-fix without verifying file compatibility
- **NEVER** fix when multiple candidates exist without asking user
- **ALWAYS** log every fix attempt (applied or skipped)
- **ALWAYS** preserve original file content (backup before modify)
- **NEVER** modify files outside the target directory
- **ALWAYS** use `--dry-run` first to preview changes

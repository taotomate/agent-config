# Safe Marker Removal via truncate() with Content-After Detection

## Problem

YouTube scraper v1 appended `<!-- youtube-scraper: processed -->` to mark files as scanned. This marker sometimes sits *before* user content that was added later (editing notes, Hermes skill writes, etc). Blindly removing the last N bytes would destroy that content.

## Solution: `clean_markers.py`

Three-mode script that:

1. **`--scan`** (read-only): reads entire file, finds marker position, checks if anything meaningful exists after it
2. **`--dry-run`**: shows what `--safe` would do without touching files
3. **`--safe`**: removes markers **only** from files where the marker is the last significant content, using `truncate()`

### Classification logic

```
For each file with marker:
  lines_after_marker = lines after marker line, minus blank lines
  
  if lines_after_marker is empty:
    → ✅ SAFE: marker is at end → truncate OK
  else:
    → ⚠️ NEEDS REVIEW: content was added after marker → DON'T TOUCH
```

### Why truncate() over rewrite?

- `truncate(pos)` only changes the file size metadata in the filesystem — existing bytes stay untouched on disk
- `open(file, "w")` rewrites the entire file — risky if interrupted mid-write
- There is **no shell equivalent** of `>>` that removes the last line. `>>` works because the OS only needs to know file length and append position. Removing a line requires reading the file to find the `\n` boundary first.

### MS-DOS / shell append for reference

- CMD: `echo texto >> archivo.txt`
- Bash: `echo "texto" >> archivo.txt`  
- PowerShell: `Add-Content -Path archivo.txt -Value "texto"`

These all use append mode (`"a"`) which is what v1's `mark_file_processed()` did with `open(file_path, "a")`.

### Real-world scan results (2026-06-07, full scan)

Scanning C:\\ and D:\\ (11,203 text files scanned):
- **10,363 files** with v1 marker
- **10,353 ✅ safe** (marker at end, no content after) → truncate OK
- **10 ⚠️ needs review** — content added after marker by Hermes (MEMORY.md, skill SKILL.md files, openspec docs, etc.)
- Flagged files were in `hermes-data/memories/`, `hermes-data/skills/media/youtube-scraper/`, `Proj-youtube-scraper/openspec/`, and `Proj-youtube-scraper-v2/README.md`
- 99.9% safe — the marker is almost always the last content in the file

### Test truncate with backup: `test_truncate.py`

Before running `--safe` on the full disk, use `test_truncate.py` to:
1. List all ⚠️ needs-review files with preview of content after marker
2. Select 10 ✅ safe files, create backups in `backups_truncate_test/`, truncate them, verify marker is gone
3. If something goes wrong, restore from backup dir

```bash
$PY test_truncate.py
```

This scans both drives, so run as background with `notify_on_complete=true`.

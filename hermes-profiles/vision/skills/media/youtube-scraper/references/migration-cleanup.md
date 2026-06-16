# v1→v2 Migration & Safe Marker Removal

## Migration Strategy

v1 tracked "already scanned" files by appending a marker line into each file:
```
<!-- youtube-scraper: processed -->
```
This was done via `open(file_path, "a")` (append mode), equivalent to `echo "..." >> file`.

v2 uses SQLite table `scanned_files` exclusively — no file modification at all.

### Migration steps (zero data loss):
1. Run `migrate_v1_to_v2.py --roots "D:\" "C:\"` — scans for marked files, populates `scanned_files` with mtime/size/last_scanned/video_count
2. Run `clean_markers.py --scan` — audit which files have markers and whether they're safe to clean
3. Run `clean_markers.py --dry-run` — verify what would be truncated
4. Run `clean_markers.py --safe` — truncate markers from safe files only
5. Files with content after the marker stay untouched (⚠️ flag)

## Why truncate() is safer than rewrite

| Operation | How it works | Risk |
|-----------|-------------|------|
| `open(f,"w")` + write | Reads file → strips marker → writes entire file back | Encoding bugs, permission changes, race conditions |
| `truncate(pos)` | Changes file size metadata only; existing bytes untouched | Minimal — only risk is wrong position |

No shell command exists for "remove last line" like `>>` adds a line. Append only needs file length; removal needs to find the newline position, requiring a read+seek.

## File safety classification

`clean_markers.py` reads the ENTIRE file to classify:

- **✅ SAFE**: Markers is the last significant line (only whitespace after). `truncate()` at the byte position before the marker.
- **⚠️ NEEDS REVIEW**: Non-whitespace content exists after the marker. Something was added post-scrape. File is NOT modified — user must inspect manually.
- **❌ ERROR**: Could not read file.

This prevents data loss when the user (or another tool) edited a file after the scraper marked it.

## Key lesson

In-file markers (any kind — HTML comments, special lines, xattrs) are fragile for tracking "already processed" state:
- They corrupt structured files (entry_points.txt, JSON, CSV headers)
- They create false positives when files are copied/versioned
- They can't handle the "content added after" case gracefully

DB-based tracking with mtime+size checks is strictly superior for filesystem scanners.

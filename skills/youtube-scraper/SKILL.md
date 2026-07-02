---
model_tier: inherited
name: youtube-scraper
version: 3
description: YouTube link scraper — scan local files for YouTube URLs, scrape metadata via yt-dlp, download transcripts. DB-tracked (no in-file markers).
trigger: When the user mentions youtube-scraper, scanning for YouTube links, or the Proj-youtube-scraper project.
---

## Execution Phases



**DRY-RUN RULE:** Before executing any destructive or external operation, first perform a dry-run to preview what will happen. Show the user what actions would be taken, then ask for confirmation before proceeding.
> **[UNIVERSAL DRY-RUN / SIMULATION RULE]**
> If the user requests execution in `--dry-run` mode or asks for a "simulation", the agent will **NOT** execute commands that alter system state or call destructive MCP tools in the Action Phase.
> Instead, the agent will print the exact payload (JSON, code block, or parameters) it planned to execute, and will wait for explicit human approval.
### 1. Preparation Phase
- Load references and verify prerequisites
- Resolve target scope

### 2. Action Phase
- Execute the main workflow (original content below preserves existing steps)

### 3. Verification Phase
- Verify output matches expected results

## Context & Triggers
**When to use this skill:**
- TODO: Add specific triggers for this skill
- Triggers: "youtube-scraper", "use youtube-scraper"



# YouTube Scraper — Link extraction, metadata, and transcripts

CLI tool at `D:\Engram_SDD\Proj-youtube-scraper-v2\` that scans local files for YouTube URLs, scrapes video metadata via yt-dlp, and downloads transcripts.


## Prerequisites
- [ ] Read access to target files/directories
- [ ] Write access for auto-fix operations


## Commands

```bash
python youtube_scraper.py scan "D:\SomeDir"        # Scan one directory
python youtube_scraper.py full-scan "C:\" "D:\"     # Scan multiple roots
python youtube_scraper.py scrape                     # Download pending metadata
python youtube_scraper.py list [--tag] [--channel]   # List/filter videos
python youtube_scraper.py download-subs              # Download transcripts
python youtube_scraper.py stats                      # Tracking stats
python youtube_scraper.py clean                      # Purge stale file records
python youtube_scraper.py rescan --all               # Force rescan of all
```

## Architecture

There are **two versions** of the scraper. Know which one you're working with:

- **v1** at `D:\Engram_SDD\Proj-youtube-scraper\` — Production DB with 1,855+ videos. Has its own `db.py`, `scraper.py`, etc.
- **v2** at `D:\Engram_SDD\Proj-youtube-scraper-v2\` — Rewrite with SQLite file tracking (`scanned_files`, mtime/size checks). Smaller dataset (testing-scale).

**Both versions now have identical `videos` table schemas: 75 columns (72 yt-dlp fields + id + url + scraped_at + has_transcript). Updated jun 2026.**

### v2 Design (no in-file markers)

- **No in-file markers** — v1 wrote `<!-- youtube-scraper: processed -->` into files, which corrupted Python package metadata (entry_points.txt). v2 uses SQLite exclusively for tracking.
- **mtime + size tracking** in `scanned_files` table — only re-scans files that are new, modified, or flagged for rescan.
- **Excludes `*.egg-info/` and `*.dist-info/`** — Python package metadata directories are pruned from os.walk and skipped. These files must NEVER be modified by external tools.
- **Bookmark detection**: Chrome/Edge JSON, Firefox places.sqlite, Netscape HTML.
- **Supported text extensions**: `.md .txt .html .htm .org .rst .csv`

## DB Schema

Both v1 and v2 now use the **same 75-column `videos` table** (all 72 useful yt-dlp fields + tracking columns).

### `videos` table (75 columns)

**Identity:** id, url, title, fulltitle, display_id, webpage_url, webpage_url_basename, webpage_url_domain, original_url
**Uploader/Channel:** uploader, uploader_id, uploader_url, channel, channel_id, channel_url, channel_follower_count, channel_is_verified
**Content:** description, tags, categories, creators, language, age_limit, availability, chapters
**Stats:** view_count, like_count, comment_count, average_rating
**Media:** upload_date, timestamp, duration, duration_string, thumbnail, thumbnails, is_live, was_live, live_status, media_type, playable_in_embed
**Video/Audio Technical:** width, height, fps, aspect_ratio, resolution, stretched_ratio, dynamic_range, vcodec, acodec, abr, vbr, tbr, asr, audio_channels, ext, filesize_approx
**Format:** format, format_id, format_note, formats, requested_formats
**Playlist:** playlist, playlist_index
**Other:** protocol, extractor, extractor_key, epoch, release_timestamp, release_year, requested_subtitles, heatmap
**Captions:** auto_captions_langs, manual_captions_langs
**Tracking:** scraped_at, has_transcript, unavailable

### Other tables (both versions)

- `transcripts` — video_id, text, language, downloaded_at
- `video_sources` — video_id, file_path (many-to-many)
- `scanned_files` — file_path, mtime, file_size, video_count, last_scanned, needs_rescan (v2 only)

### Verifying schema

Always verify the actual DB schema — don't assume migrations ran:
```python
cursor.execute("PRAGMA table_info(videos)")
```

### Mandatory: scraper ↔ DB alignment check

After ANY change to scraper fields or DB schema, verify all three layers match:

```python
import inspect, re, sqlite3, scraper, db

source = inspect.getsource(scraper.fetch_metadata)
scraper_fields = set(re.findall(r"\"(\w+)\":", source))

conn = sqlite3.connect('youtube_scraper.db')
cursor = conn.cursor()
cursor.execute('PRAGMA table_info(videos)')
db_fields = {row[1] for row in cursor.fetchall()} - {'id', 'url', 'has_transcript', 'scraped_at'}
conn.close()

missing_in_db = scraper_fields - db_fields - {'id'}
missing_in_scraper = db_fields - scraper_fields
assert not missing_in_db, f"Missing in DB: {missing_in_db}"
assert not missing_in_scraper, f"Missing in scraper: {missing_in_scraper}"
print(f"✓ All {len(scraper_fields & db_fields)} fields aligned")
```

## Dependencies

```bash
uv pip install --python <venv-python> yt-dlp youtube-transcript-api
```

The venv is at `D:\Engram_SDD\Hermes-Nous\hermes-agent\venv\` (Python 3.11.15). Use `uv pip install --python <path>` since the venv has no pip.

## Pitfalls

- **On this Windows host, `python3` does not exist** — only `python` (3.11.15) is available. Always use `python`, never `python3`. This applies to all terminal calls and scripts.
- **Always verify the actual DB schema, don't assume migrations ran** — `ALTER TABLE` in `db.py` uses try/except to skip existing columns, but if the DB was created from an old schema version, the columns simply won't exist. Query with `PRAGMA table_info(videos)` to confirm actual columns before debugging missing data.
- **v2 has 75 columns, not 29** — the schema was expanded in jun 2026 to capture all 72 yt-dlp fields. Don't reference the old 29-column count.
- **v1 is frozen** — don't invest more work in v1. All new development goes into v2.
- **Never write markers into `*.egg-info/*` or `*.dist-info/*`** — `entry_points.txt` has a strict format; any non-entry-point line (comments, HTML markers, etc.) crashes `importlib.metadata` on Python 3.11+ with `TypeError: Pair.__new__() missing 1 required positional argument: 'value'`. This broke `hermes doctor`.
- **In-file markers are fragile** — they modify user files, can corrupt structured formats, and give false positives. Always use a separate tracking DB or sidecar file instead.
- **Browser bookmark files should not be modified** — Chrome Bookmarks JSON, Firefox places.sqlite — read-only.
- **yt-dlp rate limiting** — the scraper adds 2-5s random delays between requests. Do not remove these.
- **Bash/MSYS path mangling of `C:\\` and `D:\\`** — in Git Bash (MSYS), double-quoted `"C:\\"` and `"D:\\"` get mangled. Use **single quotes**: `'C:\\'` `'D:\\'`. Even better, pass paths via Python `ROOTS = ["C:\\\\", "D:\\\\"]` in scripts instead of CLI args to avoid shell quoting entirely.
- **venv has no pip** — the Hermes venv at `hermes-agent/venv/` was built by uv and has no pip module. Install deps with `uv pip install --python <venv>/Scripts/python.exe <package>`. Do NOT use the system `pip` (it targets Python 3.12 user-site, not the 3.11 venv).
- **DB file locked by running process on Windows** — if you can't delete/rename the DB, a background process still has it open. Kill the process first, or use a new DB filename.
- **md_parser v2 API: `scan_paths()` and `scan_directory()`, NOT `parse_file()`** — the v2 md_parser has no `parse_file` function. Use `scan_paths(paths, conn=conn)` for full-drive scans. It handles exclusions, mtime tracking, and bookmark detection internally.
- **Scrape in parallel batches** — for large scrape jobs, use `ThreadPoolExecutor` with 3-5 workers and batches of 10-20 videos. Add 3s delays between batches to avoid rate limiting. See `full_pipeline.py` for the reference pattern.
- **Always align scraper output ↔ DB columns ↔ save_video_metadata** — when adding new fields, update all three: `scraper.py` return dict, `db.py` schema, and `db.py` save function. Mismatches cause silent data loss.
- **v2 md_parser has NO `parse_file` function** — v2's `md_parser` uses `scan_directory()` and `scan_paths()`, NOT `parse_file()`. Using `parse_file` causes `module 'md_parser' has no attribute 'parse_file'` on every file. Always use `md_parser.scan_paths(paths, conn=conn)` for v2.
- **Mark failed videos as unavailable** — after a scrape fails (video deleted/private/terminated), set `unavailable=1` so the pipeline doesn't waste time re-trying. Update `get_pending_metadata()` to filter out unavailable videos. See `references/video-inference.md` for recovery techniques.
- **Wayback Machine inference for unavailable videos** — for videos marked `unavailable=1`, use the Wayback Machine API (`archive.org/wayback/available?url=youtube.com/watch?v={id}`) to recover title, channel, and description from archived snapshots. This works for ~50% of unavailable videos. See `references/video-inference.md` for the full method and parser patterns. Google webcache does NOT work programmatically (rate-limited/blocked without API key). Google Search also returns 0 results without API key.
- **User preference: capture ALL fields first, assign utility later** — don't pre-select which yt-dlp fields to keep. Capture everything (72 fields) into the DB, then decide what's useful. The DB is the source of truth; views/reports can filter later.
- **v1 md_parser HAS `parse_file`** — v1's `md_parser` uses `parse_file(file_path)` which returns a dict `{file_path: [video_ids]}`. Don't mix up the APIs between versions.

## Migration & Cleanup Tools

Three scripts in the v2 project directory handle v1→v2 migration and marker cleanup:

### `migrate_v1_to_v2.py` — READ ONLY
Scans disk for files with v1 marker, reads their mtime/size/video_count, inserts into `scanned_files` table. **Does not modify any file.**
```bash
python migrate_v1_to_v2.py --roots "D:\" "C:\"
```

### `clean_markers.py` — SAFE marker removal
Three modes:
- `--scan` (default): read-only audit — classifies each marked file as ✅ safe or ⚠️ needs-review
- `--dry-run`: shows what `--safe` would do
- `--safe`: **removes markers only from safe files** using `truncate()` (shrinks file without rewriting content)

Key: if content was added AFTER the marker (user edits, other tools), the file is flagged ⚠️ and NOT touched.

### `test_truncate.py` — Small-scale truncate test with backup
Lists ⚠️ needs-review files, then truncates 10 ✅ safe files with .bak copies in `backups_truncate_test/`. Use before running `--safe` on full disk.
```bash
$PY test_truncate.py
```

### `remove_markers.py` — full marker removal (rewrites file)
Less safe — rewrites entire file sans marker. Use `clean_markers.py` instead.

## Marker Cleanup Results (2026-06-11)

Ran `clean_markers.py --scan` then `--safe` on C:\ and D:\:
- **13,654** files scanned
- **12,502** had the v1 marker `<!-- youtube-scraper: processed -->`
- **12,468** safely truncated (marker was last line)
- **34 files** need manual review (content after marker)
- **0** errors

The 34 files needing review are mostly project-internal files (SKILL.md, references, openspecs) where the marker was embedded mid-content. See the scan output for the full list.

### Why truncate() over rewrite?

`truncate()` only changes the file size metadata — existing bytes on disk are untouched. This is the safest way to remove trailing content. There is no shell equivalent of `>>` that removes the last line (append works because the OS just needs file length; removal needs to know where the line starts, requiring a full read).

## Running the scraper

### v2 (current development version)
```bash
PY="/d/Engram_SDD/Hermes-Nous/hermes-agent/venv/Scripts/python.exe"
cd /d/Engram_SDD/Proj-youtube-scraper-v2
$PY youtube_scraper.py <command> [args]
```

### v1 (production data)
```bash
PY="/d/Engram_SDD/Hermes-Nous/hermes-agent/venv/Scripts/python.exe"
cd /d/Engram_SDD/Proj-youtube-scraper
$PY youtube_scraper.py <command> [args]
```

Do NOT use the system `python` (Python 3.12) — yt-dlp is installed in the 3.11 venv.

### Full scan across drives

```bash
$PY youtube_scraper.py full-scan 'C:\\' 'D:\\'
```
Bash quoting: use single quotes around `C:\\` and `D:\\` — double quotes get mangled by MSYS path expansion.

### Full pipeline (scan + scrape)

v2 has a `full_pipeline.py` that does the complete workflow in order:
1. Full scan of C:\ and D:\ for YouTube links
2. Parallel scrape of metadata in batches (3 workers, batch size 10, 3s delay between rounds)

```bash
cd /d/Engram_SDD/Proj-youtube-scraper-v2
python full_pipeline.py
```

Run in background with `notify_on_complete=true` — it takes a while for full drives.

### Drive scan helper scripts

Both v1 and v2 have a `drive_scan.py` script that recursively scans C:\ and D:\ with smart exclusions (Windows, AppData, node_modules, .git, .egg-info, .dist-info, binary files). v2's version also uses `should_scan_file()` to skip unchanged files via mtime/size check.

These scripts are NOT part of the official argparse CLI — they're standalone helpers in each project root.

```bash
# v2 (uses scanned_files tracking)
cd /d/Engram_SDD/Proj-youtube-scraper-v2 && python drive_scan.py
```

## Session Search & History Patterns

When the user asks "what were we talking about" or "give me a chronology":
- `session_search(limit=10, sort="oldest")` — lists all sessions chronologically with previews
- `session_search(query="topic", limit=5)` — FTS5 search across sessions
- `session_search(session_id="...", around_message_id=N, window=10)` — scroll inside a session
- **Session compaction is per-session**, not shared. When context fills up, each session compacts independently.
- The user's main Telegram session started ~May 27, 2026. Earlier sessions are background/cli context.

## Pipeline Workflow

For the full scan→scrape→infer pipeline (parallel batches, Wayback Machine recovery, DuckDuckGo/Bing fallback, and generic-title cleaning), see:
`references/pipeline-workflow.md`

## See also

- `references/pipeline-workflow.md` — full pipeline: scan, parallel scrape, Wayback/DDG inference, stats (jun 2026)
- `references/video-inference.md` — recovering metadata for deleted/private videos via Google cache, Wayback Machine, and Google Search.
- `references/v2-schema.md` — complete 75-column schema reference with all 72 yt-dlp fields grouped by category.
- `references/yt-dlp-fields.md` — full list of all 72 yt-dlp fields the scraper captures (updated jun 2026: all fields now captured).
- `references/entry-points-debug.md` — debugging session for the entry_points.txt corruption that led to v2.
- `references/migration-cleanup.md` — v1→v2 migration strategy and safe marker removal approach.
- `references/clean-markers-pattern.md` — safe marker removal via truncate() with content-after detection.
- `references/v1-v2-schema-gap.md` — ~~column-by-column comparison~~ RESOLVED: v2 now has the authoritative 75-column schema (jun 2026).


## Guardrails (Critical Rules)
- **NEVER** execute destructive operations without explicit user confirmation
- **ALWAYS** verify target exists before operating
- **ALWAYS** handle errors gracefully — skip with warning, don't crash


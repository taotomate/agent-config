---
name: youtube-scraper-pipeline
description: YouTube Scraper v2 — Full pipeline for scanning local files for YouTube links, scraping metadata via yt-dlp, and recovering deleted video info via Wayback Machine. Covers DB schema (75 fields), parallel scraping, and inference methods.
---

# YouTube Scraper v2 — Pipeline

## Project Layout
- **Dir**: `D:\Engram_SDD\Proj-youtube-scraper-v2\`
- **DB**: `youtube_scraper_new.db` (75 columns — all yt-dlp fields)
- **Key scripts**: `full_pipeline.py`, `wayback_inference.py`
- **v1 is frozen** — incomplete schema, don't use

## DB Schema
The `videos` table has 75 columns covering all yt-dlp fields:
- **Identity**: id, url, title, fulltitle, display_id, webpage_url, webpage_url_basename, webpage_url_domain, original_url
- **Uploader/Channel**: uploader, uploader_id, uploader_url, channel, channel_id, channel_url, channel_follower_count, channel_is_verified
- **Content**: description, tags, categories, creators, language, age_limit, availability, chapters
- **Stats**: view_count, like_count, comment_count, average_rating
- **Media**: upload_date, timestamp, duration, duration_string, thumbnail, thumbnails, is_live, was_live, live_status, media_type, playable_in_embed
- **Technical**: width, height, fps, aspect_ratio, resolution, stretched_ratio, dynamic_range, vcodec, acodec, abr, vbr, tbr, asr, audio_channels, ext, filesize_approx
- **Format**: format, format_id, format_note, formats, requested_formats
- **Playlist**: playlist, playlist_index
- **Other**: protocol, extractor, extractor_key, epoch, release_timestamp, release_year, requested_subtitles, heatmap
- **Captions**: auto_captions_langs, manual_captions_langs
- **Tracking**: scraped_at, has_transcript, unavailable
- **Inferred**: inferred_title, inferred_channel, inferred_description, inferred_source, inferred_url

## Key APIs

### md_parser (v2)
- **USE**: `md_parser.scan_paths(paths, conn, skip_dirs, progress_callback)` or `md_parser.scan_directory(dir_path, conn, ...)`
- **DO NOT USE**: `md_parser.parse_file()` — does NOT exist in v2
- `conn` parameter enables mtime/size tracking via `scanned_files` table

### scraper
- `scraper.fetch_metadata(video_id)` → returns dict with ALL 72 yt-dlp fields, or None on failure
- Has built-in random delay (2-5s) to avoid rate limiting

### db
- `db.init_db(conn)` — creates all tables with migration-safe ALTER TABLEs
- `db.get_pending_metadata(conn)` — returns videos WHERE scraped_at IS NULL AND unavailable=0
- `db.save_video_metadata(conn, video_id, metadata)` — saves all 72 fields

## Pipeline Steps

### 1. Scan Links
```python
results = md_parser.scan_paths(["C:\\", "D:\\"], conn=conn)
# Returns {file_path: [video_ids]}
# Automatically tracks scanned_files with mtime/size
```

### 2. Scrape Metadata (Parallel)
Use `full_pipeline.py` which does:
- Batches of 10 videos
- 3 parallel workers (ThreadPoolExecutor)
- 3s delay between batches
- Auto-marks failed videos as `unavailable=1`

### 3. Recover Deleted Videos (Wayback Machine)
Use `wayback_inference.py`:
- Queries archive.org API for each unavailable video
- Parses title, channel, description from Wayback snapshots
- **Filters generic titles**: "This video isn't available anymore", "Video unavailable", "We're sorry to see you go!", "- YouTube", "YouTube"
- Recovery rate: ~47% of deleted videos

### 4. Fallback Inference (DuckDuckGo + Bing)
For videos that Wayback can't recover (~53% of deleted videos), use `fallback_inference.py`:
- **Method 1**: DuckDuckGo Instant Answer API (JSON, no rate-limit)
- **Method 2**: DuckDuckGo HTML search (fallback)
- **Method 3**: Bing web search (final fallback)
- Same generic-title filtering as Wayback
- Slower than Wayback (1s delay per video, sequential)
- **Recovery rate**: ~23% of remaining videos, but many are generic results
- **After running**: manually review and mark generic results as `unavailable=1`

### 4. Fallback Inference (DuckDuckGo + Bing)
For videos that Wayback can't recover (~53% of deleted videos), use `fallback_inference.py`:
- **Method 1**: DuckDuckGo Instant Answer API (JSON, no rate-limit)
- **Method 2**: DuckDuckGo HTML search (fallback)
- **Method 3**: Bing web search (final fallback)
- Same generic-title filtering as Wayback
- Slower than Wayback (1s delay per video, sequential)
- **Recovery rate**: ~23% of remaining videos, but many are generic results
- **After running**: manually review and mark generic results as `unavailable=1`

### 5. Cleaning Generic Inference Results
After fallback inference, clean up generic titles:
```python
import sqlite3
conn = sqlite3.connect('youtube_scraper_new.db')
cursor = conn.cursor()
generics = ['YouTube App - App Store', 'Google', 'Facebook', 'Reverse Video Search',
            'SongFinder', 'Number Lore', 'The Music Channel', 'How to Watch Deleted']
for g in generics:
    cursor.execute('''
        UPDATE videos 
        SET unavailable = 1, inferred_title = NULL, inferred_source = NULL, inferred_url = NULL
        WHERE inferred_title LIKE ?
    ''', (f'%{g}%',))
conn.commit()
```

## Final Stats (jun 2026)
- **1,605 videos** with full yt-dlp metadata (direct scrape)
- **103 videos** with inferred metadata (92 Wayback + 11 DDG/Bing real titles)
- **250 videos** marked unavailable (irrecoverable)
- **Total**: 1,958 videos in DB
- **Overall recovery rate**: ~43% of deleted videos recovered via inference

### 4. Fallback Inference (DuckDuckGo + Bing)
For videos that Wayback can't recover (~53% of deleted videos), use `fallback_inference.py`:
- **Method 1**: DuckDuckGo Instant Answer API (JSON, no rate-limit)
- **Method 2**: DuckDuckGo HTML search (fallback)
- **Method 3**: Bing web search (final fallback)
- Same generic-title filtering as Wayback
- Slower than Wayback (1s delay per video, sequential)
- **Recovery rate**: ~23% of remaining videos, but many are generic results
- **After running**: manually review and mark generic results as `unavailable=1`

### 5. Cleaning Generic Inference Results
After fallback inference, clean up generic titles:
```python
import sqlite3
conn = sqlite3.connect('youtube_scraper_new.db')
cursor = conn.cursor()
generics = ['YouTube App - App Store', 'Google', 'Facebook', 'Reverse Video Search',
            'SongFinder', 'Number Lore', 'The Music Channel', 'How to Watch Deleted']
for g in generics:
    cursor.execute('''
        UPDATE videos 
        SET unavailable = 1, inferred_title = NULL, inferred_source = NULL, inferred_url = NULL
        WHERE inferred_title LIKE ?
    ''', (f'%{g}%',))
conn.commit()
```

## Final Stats (jun 2026)
- **1,605 videos** with full yt-dlp metadata (direct scrape)
- **103 videos** with inferred metadata (92 Wayback + 11 DDG/Bing real titles)
- **250 videos** marked unavailable (irrecoverable)
- **Total**: 1,958 videos in DB
- **Overall recovery rate**: ~43% of deleted videos recovered via inference

## What NOT to do
- **Google webcache**: Blocks programmatic access with CAPTCHA/429. Not viable without API key.
- **Google Search**: Same rate limiting issue without API key.
- **parse_file()**: Doesn't exist in v2 md_parser. Use scan_paths().
- **DB locked on Windows**: SQLite journal files (.db-journal) lock the DB. If `ALTER TABLE` or queries time out, another process (e.g., SQLiteDatabaseBrowserPortable.exe) has the handle. Close the GUI tool first. Don't retry in a loop — it won't fix itself until the handle is released.
- **Don't re-scrape unavailable videos**: Check `unavailable=1` flag before scraping.

## Telegram Commands Reference
Ver `hermes-multi-provider-routing/references/telegram-commands.md` para la lista completa de 127 comandos.
Más usados: `/new` `/stop` `/background(bg/btw)` `/steer` `/queue(q)` `/model` `/status` `/help`

## Known Overlap

This skill (`data-science/youtube-scraper-pipeline`) and `media/youtube-scraper` cover the same project.
The `media/youtube-scraper` skill is the **canonical** reference with full schema and pitfalls.
This skill is a leaner workflow summary. When in doubt, consult the canonical skill first.
"

## OpenRouter Free Models DB
Local DB at `hermes-data/openrouter_models.db` — 27 free models with categories, context lengths, modalities.
Update script: `D:\Engram_SDD\Proj-youtube-scraper-v2\update_models_db.py`

Top free models:
- **Agentic**: owl-alpha (1M ctx), gpt-oss-120b (131K), hermes-3-405b (131K)
- **Coding**: qwen3-coder (1M), kimi-k2.6 (262K, multimodal), laguna-m.1 (262K)
- **General**: nemotron-3-ultra-550b (1M), nemotron-3-super-120b (1M)
- **Multimodal**: gemma-4-31b-it (262K), nemotron-nano-12b-v2-vl (128K)
- **Lightweight**: llama-3.2-3b (131K), nemotron-nano-9b (128K)

Suggested fallback chain: owl-alpha → nemotron-3-ultra → hermes-3 → gpt-oss → llama-3.3-70b:free

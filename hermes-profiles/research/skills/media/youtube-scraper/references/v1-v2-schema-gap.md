# v1 vs v2 Schema Gap

## Discovery (2026-06-07)

The v2 `db.py` was built from an early v1 baseline and is missing 20 columns that were added to v1's `videos` table.

### v1 `videos` columns (28 total)

| Column | Type | Description |
|--------|------|-------------|
| id | TEXT PK | YouTube video ID |
| url | TEXT | Full YouTube URL |
| title | TEXT | Video title |
| webpage_url | TEXT | Canonical webpage URL |
| uploader_id | TEXT | Uploader's unique ID |
| channel | TEXT | Channel display name |
| channel_id | TEXT | Channel unique ID |
| channel_url | TEXT | Channel URL |
| channel_follower_count | INTEGER | Subscriber count |
| channel_is_verified | INTEGER | Verified badge (0/1) |
| description | TEXT | Video description |
| tags | TEXT (JSON) | List of tags |
| categories | TEXT (JSON) | List of categories |
| language | TEXT | Primary language code |
| age_limit | INTEGER | Age restriction |
| availability | TEXT | public/private/unlisted |
| view_count | INTEGER | View count |
| like_count | INTEGER | Like count |
| comment_count | INTEGER | Comment count |
| upload_date | TEXT | YYYYMMDD format |
| duration | INTEGER | Duration in seconds |
| duration_string | TEXT | Human-readable duration |
| thumbnail | TEXT | Thumbnail URL |
| is_live | INTEGER | Currently live (0/1) |
| was_live | INTEGER | Was a live stream (0/1) |
| auto_captions_langs | TEXT (JSON) | Auto-generated caption languages |
| manual_captions_langs | TEXT (JSON) | Manual caption languages |
| scraped_at | TEXT | ISO datetime of metadata scrape |
| has_transcript | INTEGER | Transcript downloaded (0/1/NULL) |

### v2 `videos` columns (8 total)

Only: id, url, title, description, channel, tags, scraped_at, has_transcript

### Missing in v2

All of these are absent from v2's `db.py`:
- webpage_url, uploader_id
- channel_id, channel_url, channel_follower_count, channel_is_verified
- categories, language, age_limit, availability
- view_count, like_count, comment_count
- upload_date, duration, duration_string, thumbnail, is_live, was_live
- auto_captions_langs, manual_captions_langs

### Fix

To bring v2 up to v1's schema level, add the missing columns to v2's `db.py` CREATE TABLE statement and add corresponding ALTER TABLE entries in the migration block. Also update `save_video_metadata()` to accept and store the additional fields from yt-dlp's `extract_info()` output.

The v1 `scraper.py` already captures all these fields from yt-dlp — the v2 `scraper.py` only captures title, description, channel, and tags.

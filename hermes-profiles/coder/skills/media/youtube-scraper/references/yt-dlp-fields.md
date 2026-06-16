# yt-dlp Available Fields (YouTube)

Tested against `dQw4w9WgXcQ` on 2026-06-07. yt-dlp returns **74 fields** for a YouTube video.

## Fields captured by the scraper (28 fields)

These are extracted in `scraper.py` → `fetch_metadata()` and stored in the `videos` table:

| Field | yt-dlp key | Type | Notes |
|-------|-----------|------|-------|
| title | `title` | str | Full title |
| webpage_url | `webpage_url` | str | Clean URL |
| uploader_id | `uploader_id` | str | e.g. `@RickAstleyYT` |
| channel | `uploader` or `channel` | str | Display name |
| channel_id | `channel_id` | str | UC... format |
| channel_url | `channel_url` or `uploader_url` | str | Full channel URL |
| channel_follower_count | `channel_follower_count` | int | |
| channel_is_verified | `channel_is_verified` | bool | |
| description | `description` | str | Full description |
| tags | `tags` | list[str] | |
| categories | `categories` | list[str] | e.g. `['Music']` |
| language | `language` | str | e.g. `'en'` |
| age_limit | `age_limit` | int | 0, 18, etc. |
| availability | `availability` | str | `'public'`, `'private'`, etc. |
| view_count | `view_count` | int | |
| like_count | `like_count` | int | |
| comment_count | `comment_count` | int | |
| upload_date | `upload_date` | str | YYYYMMDD format |
| duration | `duration` | int | Seconds |
| duration_string | `duration_string` | str | e.g. `'3:33'` |
| thumbnail | `thumbnail` | str | URL to maxresdefault |
| is_live | `is_live` | bool | |
| was_live | `was_live` | bool | |
| auto_captions_langs | `automatic_captions` (keys) | list[str] | Languages with auto captions |
| manual_captions_langs | `subtitles` (keys) | list[str] | Languages with manual captions |

## Other notable yt-dlp fields NOT captured

These are available in the raw `info` dict but not stored in DB:

- `fulltitle`, `display_id`, `extractor`, `extractor_key`
- `formats` (large), `thumbnails` (all sizes), `chapters`, `heatmap`
- `fps`, `width`, `height`, `resolution`, `aspect_ratio`
- `vcodec`, `acodec`, `vbr`, `abr`, `tbr`
- `dynamic_range`, `audio_channels`, `asr`
- `filesize_approx`, `protocol`
- `live_status`, `media_type`, `playable_in_embed`
- `release_timestamp`, `release_year`
- `_format_sort_fields`, `_has_drm` (internal)

## How to discover fields for a new video

```python
from yt_dlp import YoutubeDL
ydl_opts = {'skip_download': True, 'quiet': True, 'no_warnings': True}
with YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info('https://www.youtube.com/watch?v=VIDEO_ID', download=False)
    for key in sorted(info.keys()):
        print(f'{key}: {type(info[key]).__name__}')
```

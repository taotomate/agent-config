# v2 DB Schema — Complete 75-column `videos` table

All 72 yt-dlp fields + id, url, scraped_at, has_transcript.

## Column list (75 total)

### Tracking (4)
id, url, scraped_at, has_transcript

### Identity (7)
title, fulltitle, display_id, webpage_url, webpage_url_basename, webpage_url_domain, original_url

### Uploader/Channel (8)
uploader, uploader_id, uploader_url, channel, channel_id, channel_url, channel_follower_count, channel_is_verified

### Content (8)
description, tags, categories, creators, language, age_limit, availability, chapters

### Stats (4)
view_count, like_count, comment_count, average_rating

### Media (11)
upload_date, timestamp, duration, duration_string, thumbnail, thumbnails, is_live, was_live, live_status, media_type, playable_in_embed

### Video/Audio technical (17)
width, height, fps, aspect_ratio, resolution, stretched_ratio, dynamic_range, vcodec, acodec, abr, vbr, tbr, asr, audio_channels, ext, filesize_approx

### Format (5)
format, format_id, format_note, formats, requested_formats

### Playlist (2)
playlist, playlist_index

### Other (8)
protocol, extractor, extractor_key, epoch, release_timestamp, release_year, requested_subtitles, heatmap

### Captions (2)
auto_captions_langs, manual_captions_langs

## yt-dlp fields NOT captured (internal)
_has_drm, _format_sort_fields

## Data types mapping
- JSON list fields (stored as TEXT): tags, categories, creators, chapters, thumbnails, formats, requested_formats, requested_subtitles, heatmap, auto_captions_langs, manual_captions_langs
- Boolean → INTEGER (0/1/NULL): channel_is_verified, is_live, was_live, playable_in_embed
- Dates: upload_date (TEXT "YYYYMMDD"), timestamp (INTEGER unix epoch)

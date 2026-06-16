# Video Inference — Recovering Metadata for Unavailable Videos

When YouTube videos are deleted, made private, or their accounts are terminated, yt-dlp returns "Video unavailable". This document covers techniques to recover metadata for those videos.

## Test Results (15 videos, jun 2026)

| Method | Found | With Title | With Channel | Viability |
|--------|-------|------------|--------------|-----------|
| Wayback Machine API | 8/15 (53%) | 8 (3 real, 5 generic) | 3 | Best method |
| Google webcache | 15/15 (100%) | 0 (Google page title, not video) | 0 | Blocked by CAPTCHA |
| Google Search | 0/15 (0%) | 0 | 0 | Blocked without API key |

**Conclusion: Wayback Machine is the only viable programmatic method.**

## Wayback Machine Method

### API Endpoint

```
https://archive.org/wayback/available?url=youtube.com/watch?v={video_id}
```

Returns JSON with `archived_snapshots.closest.url` if a snapshot exists.

### Parsing the Snapshot HTML

Once you have the snapshot URL, fetch it and extract:

**Title patterns** (try in order):
- `"title":{"runs":[{"text":"..."}]}` — YouTube JSON in page
- `"title":"..."` — Simple JSON
- `<title>...</title>` — HTML title tag
- `itemprop="name" content="..."` — Schema.org

**Channel patterns:**
- `"channelName":"..."`
- `"ownerChannelName":"..."`
- `"author":"..."`
- `/channel/UC...` or `/@handle` in hrefs

**Description patterns:**
- `"description":{"simpleText":"..."}`
- `itemprop="description" content="..."`
- `<meta name="description" content="...">`

### Filtering Generic Titles

Wayback snapshots often return the generic YouTube page title `"- YouTube"` instead of the actual video title. Filter these out — only store inferred data when the title is meaningful (not generic, not empty, not just the YouTube domain).

### DB Schema for Inferred Data

```sql
ALTER TABLE videos ADD COLUMN inferred_title TEXT;
ALTER TABLE videos ADD COLUMN inferred_channel TEXT;
ALTER TABLE videos ADD COLUMN inferred_description TEXT;
ALTER TABLE videos ADD COLUMN inferred_source TEXT;
ALTER TABLE videos ADD COLUMN inferred_url TEXT;
```

### Rate Limits

- Wayback Machine: ~15 req/s. Use 0.5s delays between requests to be polite.
- The API call is lightweight; the heavy part is fetching the full snapshot HTML.

## Why Google Methods Don't Work

**Google webcache** (`webcache.googleusercontent.com`): Returns 302 redirect to CAPTCHA page for programmatic requests. Even when returning 200, the HTML contains the Google search results page, not the cached video content.

**Google Search** (`google.com/search`): Serves different content to browsers vs. programmatic requests. Useful results loaded via JavaScript. No parseable video data in the raw HTML.

**Both methods require official Google APIs** (Custom Search API with key) to work reliably.

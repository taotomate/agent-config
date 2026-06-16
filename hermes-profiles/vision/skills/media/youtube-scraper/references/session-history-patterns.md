# Session History & Compaction Patterns

## How to Reconstruct Conversation History

When the user asks "what were we talking about" or "give me a chronology":

1. **List all sessions chronologically:**
   ```
   session_search(limit=10, sort="oldest")
   ```
   Returns session_id, preview, message_count, timestamps.

2. **Search for specific topics across sessions:**
   ```
   session_search(query="topic keyword", limit=5)
   ```
   Uses FTS5 — supports AND, OR, NOT, quoted phrases, prefix wildcards.

3. **Scroll inside a specific session:**
   ```
   session_search(session_id="...", around_message_id=N, window=10)
   ```
   Use `match_message_id` from discovery results as anchor.
   To scroll forward: pass last message's id as `around_message_id`.
   To scroll backward: pass first message's id.

## Session Compaction

- **Per-session**, not shared across sessions.
- When context fills up, the current session compacts independently.
- Previous sessions are NOT affected.
- The compacted summary includes: Active Task, Completed Actions, In Progress, Blocked, Key Decisions, Pending Asks.
- After compaction, the agent only has the summary — not the full transcript.
- Use `session_search` to recover details from compacted sessions.

## This User's Session History

- Main Telegram session started ~May 27, 2026
- Earlier sessions are background/cli context
- Key projects: YouTube Scraper v2, Hermes Gateway, PrometeOS, Cloudflare Tunnel

---
name: fast-file-locator
description: Instantly finds files on Windows via Everything HTTP API (MFT). Thin wrapper over execution/fast_file_locator.py.
version: 1.2.0
author: TaoTomate
generator_model: nemotron-3-ultra-free
inherited_from: fast-file-locator/SKILL.md
migrated_by: skill-optimizer@1.0.0
model_tier: fast
---

## Context & Triggers
**When to use this skill:**
- Find files quickly on Windows without iterating directories.
- Locate the absolute path of a specific file by name or extension.
- Triggers: "find file", "locate file", "Everything", "fast file"

## Prerequisites
- [ ] **Everything** running with HTTP server enabled (Tools → Options → HTTP Server → Enable HTTP server)
- [ ] Environment variables (optional):
  - `EVERYTHING_URL` (default: http://localhost/)
  - `EVERYTHING_USER` (default: user)
  - `EVERYTHING_PASS` (default: 123456 — it is recommended to change)

## Execution Phases


### 1. Action Phase
- Execute the script:
  ```bash
  python execution/fast_file_locator.py "<query>" <count>
  ```
- Parameters:
  - `query`: file name or pattern (supports Everything syntax: `ext:log`, `*.py`, `!folder:`)
  - `count`: result limit (default 10)

### 2. Verification Phase
- Validate the script returns `{"status": "success"}` with results.
- If it fails, verify that Everything is running with HTTP server enabled.

## Guardrails (Critical Rules)
- **ALWAYS** validate the script returns valid JSON before presenting results.
- **NEVER** iterate directories with `os.walk` as fallback — Everything search is the only path.
- **NEVER** hardcode credentials — use environment variables.

## Data Structures / Examples & Commands

### CLI
```bash
python execution/fast_file_locator.py docker-compose.yml 5
python execution/fast_file_locator.py "ext:log C:\Users\user\project" 10
```

### Expected Output
```json
{"status": "success", "data": {"query": "docker-compose.yml", "count": 1, "results": [{"filename": "docker-compose.yml", "path": "C:\\Users\\user\\project", "full_path": "C:\\Users\\user\\project\\docker-compose.yml", "size": "1234", "date_modified": "2025-01-01 12:00:00"}]}, "error_log": ""}
```

## Troubleshooting
- *Error "Everything unavailable"*: Everything is not running or HTTP server is disabled. Open Everything → Tools → Options → HTTP Server → Enable.
- *Error 401*: Incorrect credentials. Verify `EVERYTHING_USER` and `EVERYTHING_PASS`.

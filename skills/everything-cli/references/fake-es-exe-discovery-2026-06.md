# Fake es.exe Discovery — 2026-06

## Symptom
User has an `es.exe` file at `D:\Engram_SDD\Tools\es.exe` that produces no output — not even an error — when invoked with any arguments.

## Root Cause
The file is **not the real Everything CLI**. It's a copy of `cmd.exe` renamed to `es.exe`. When you run `es.exe /?`, it shows the CMD help screen instead of Everything help.

## How to Detect

```bash
# Real Everything CLI responds with:
cmd.exe /c "C:\Program Files (x86)\Everything\es.exe -version"
# Output: "ES 1.1.0.30" + usage info

# Fake es.exe (cmd.exe renamed) responds with:
cmd.exe /c "D:\Engram_SDD\Tools\es.exe /?"
# Output: CMD.EXE help (shows /C, /K, /Q, etc.)
```

## Lesson Learned
**Never assume a binary is fake just because it returns empty output.** The real Everything CLI also returns empty when its service isn't running. Always:
1. Check `es -version` — real CLI shows version string
2. Try the HTTP API at `http://127.0.0.1:80` — works independently of CLI
3. Check `tasklist /FI IMAGENAME eq Everything.exe` for the service

## Real es.exe Locations
- `C:\Program Files (x86)\Everything\es.exe` ← ships with Everything installer
- `C:\Program Files\Everything\es.exe` ← 64-bit install

## Resolution
Use the real es.exe from the Everything install directory, or better yet, use the HTTP API which doesn't require the service process.

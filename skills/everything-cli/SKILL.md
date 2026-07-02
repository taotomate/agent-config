---
name: everything-cli
description: "Use when the user asks to search files with Everything (es.exe). Wraps VoidTools Everything CLI on Windows — verifies the binary is genuine, auto-starts the service if not running, then searches by filename, path, extension, or regex."
version: 1.1.0
author: OWL
model_tier: medium
license: MIT
platforms: [windows]
metadata:
  hermes:
    tags: [everything, search, files, windows, es.exe, voidtools]
    related_skills: []
---

## Execution Phases


**DRY-RUN RULE:** Before executing any destructive or external operation, first perform a dry-run to preview what will happen. Show the user what actions would be taken, then ask for confirmation before proceeding.
### 1. Preparation Phase
- Load references and verify prerequisites
- Resolve target scope

### 2. Action Phase
- Execute the main workflow (original content below preserves existing steps)

### 3. Verification Phase
- Verify output matches expected results

## Context & Triggers
**When to use this skill:**
- Triggers: "everything-cli", "use everything-cli"


# Everything CLI (es.exe)

Search the filesystem using VoidTools Everything from the command line. Much faster than `dir /s` or MSYS `find` because Everything uses its own NTFS index.


## CRITICAL: Verify the Binary First

Before trusting any `es.exe` path, verify it's the **real Everything CLI** and not a renamed `cmd.exe` or other executable.

```bash
cmd.exe /c "<path_to_es.exe> /?"
```

**If the output shows anything other than "Everything"** (e.g. it shows CMD help, version info unrelated to Everything, or produces no output at all), the binary is **fake/broken**. Do NOT use it.

The real `es.exe` from VoidTools:
- Responds to `/?` with Everything-specific help
- Is typically located in `C:\Program Files\Everything\es.exe` or alongside `Everything.exe`
- Is a small file (~1MB), not a copy of cmd.exe

**If the binary is fake or missing**, fall back to MSYS `find`:
```bash
find /d/ -name "*pattern*" 2>/dev/null
```

## Default Path

The real Everything CLI (`es.exe`) ships with the Everything install, typically at:
```
C:\Program Files (x86)\Everything\es.exe
```

**WARNING:** A file named `es.exe` at `D:\Engram_SDD\Tools\es.exe` is a FAKE — it's actually `cmd.exe` renamed. It will silently return empty output. Always verify with `es -version` (should return `ES X.X.X.X`, not cmd help).

If the user has es.exe elsewhere, ask for the path. Override with `ES_PATH` env var if needed.

If es.exe is not at the above path, common alternatives:
- `C:\Program Files\Everything\es.exe`
- `D:\Engram_SDD\Tools\es.exe` (may be a fake — verify with `es -version`)

### How to Search

Everything exposes an HTTP server on `http://127.0.0.1:80` (configurable in Everything Options → HTTP Server). Use Python's `urllib` to query directly — this is the most reliable search method.

### HTTP API Search

```python
import urllib.request, base64, urllib.parse

username = "user"  # from Everything Options → HTTP Server
password = ""      # get from user if unknown

credentials = base64.b64encode(f"{username}:{password}".encode()).decode()
headers = {"Authorization": f"Basic {credentials}"}

url = f"http://127.0.0.1/?search={urllib.parse.quote(pattern)}"
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req, timeout=10) as resp:
    html = resp.read().decode('utf-8')
```

The response is HTML. Parse results from the table rows.

### Resultados HTML

La respuesta HTML contiene filas con clase `trdata1`/`trdata2`. Extraer:
- Nombre: texto dentro de `<td class="folder">` o `<td class="file">`
- Path: texto dentro de `<td class="pathdata">`
- Tamaño: texto dentro de `<td class="sizedata">`
- Fecha: texto dentro de `<td class="modifieddata">`

Verificar `<p class="numresults">` para el total de resultados.

Ver referencia completa con script Python listo para usar en `references/http-api-reference.md`.

---

## Auth

If the HTTP server has a username/password, build a Basic auth header:
```python
import base64
credentials = base64.b64encode(f"{username}:{password}".encode()).decode()
headers = {"Authorization": f"Basic {credentials}"}
```

### Fallback

If the HTTP server is not responding (connection refused / 401 without credentials):
1. Try without auth (some installations have empty password)
2. Fall back to MSYS `find`:
   ```bash
   find /c/ -name "*pattern*" 2>/dev/null
   ```
3. As last resort, use the CLI `es.exe` (requires service running)

If the user has es.exe elsewhere, ask for the path. Override with `ES_PATH` env var if needed.

## How It Works

Everything runs as a background service that indexes NTFS volumes. The CLI (`es.exe`) queries that service and returns matching paths. If the service is not running, the CLI produces no output.

## Step 1: Check if Everything Service is Running

```bash
cmd.exe /c "tasklist /FI IMAGENAME eq Everything.exe 2>nul"
```

If the output contains `Everything.exe` with a PID → service is running. Proceed to Step 2.

If not running → go to Step 1a.

### Step 1a: Start the Service

The CLI (`es.exe`) returns empty output if the Everything service is not running. The service is launched via the GUI executable.

Common install paths:
- `C:\Program Files (x86)\Everything\Everything.exe`
- `C:\Program Files\Everything\Everything.exe`

Ask the user for the path if not found at those locations. Also accept `EVERYTHING_GUI_PATH` env var.

Launch the GUI (it starts the service, then the GUI can be closed):
```bash
cmd.exe /c "start \"\" \"<path_to_GUI>\""
```

Wait 5 seconds after launching for the service to initialize the index. If this is a first-ever start, the index may take longer (ask the user to wait and check again).

**If the service still doesn't start**, ask the user to open Everything GUI manually and close it. That initializes the service on the system.

## Step 2: Run the Search

Always invoke via `cmd.exe /c` from bash/MSYS — `es.exe` is a native Windows executable.

### Basic filename search
```bash
cmd.exe /c "<path_to_es.exe> <pattern>"
```

### Search in specific path
```bash
cmd.exe /c "<path_to_es.exe> <pattern> <path>"
```

### Regex search
```bash
cmd.exe /c "<path_to_es.exe> /r <regex>"
```

### Case-insensitive search
```bash
cmd.exe /c "<path_to_es.exe> /i <pattern>"
```

### Extension filter
```bash
cmd.exe /c "<path_to_es.exe> ext:<ext>"
```

### Limit results
```bash
cmd.exe /c "<path_to_es.exe> /<count> <pattern>"
```
Example: `/50` returns max 50 results.

## Common Patterns

| Goal | Command |
|---|---|
| Find a file by name | `es.exe taotomate` |
| Find in specific folder | `es.exe taotomate D:\Engram_SDD` |
| Find by extension | `es.exe ext:py` |
| Regex match | `es.exe /r "taotomate.*\.py"` |
| Case-insensitive | `es.exe /i Taotomate` |
| Limit to 20 results | `es.exe /20 taotomate` |

## Output Format

Everything returns one path per line:
```
D:\folder\taotomate\file1.py
D:\folder\taotomate\file2.py
```

If no matches → empty output (exit code 0).

## Pitfalls

## Pitfalls

1. **Service not running = silent empty output.** Always check `tasklist` first. If the user says "es.exe didn't find anything", 99% of the time the service is not running.

2. **Bash eats backslashes.** Never call `es.exe` directly from bash — always wrap in `cmd.exe /c "..."`.

3. **Quotes in pattern.** If the pattern contains spaces, wrap in double quotes inside the cmd.exe call:
   ```bash
   cmd.exe /c "D:\Engram_SDD\Tools\es.exe \"my file.txt\""
   ```

4. **Everything index not fresh.** After creating new files, Everything may take a few seconds to index them. If a just-created file doesn't appear, wait and retry.

5. **No results but you know the file exists.** The NTFS index may be rebuilding. Run `Everything.exe` GUI once to trigger a re-index.

6. **Fake es.exe (cmd.exe renamed).** Some users have an `es.exe` that is actually `cmd.exe` copied/renamed — it produces no output and no error. Verify the real es.exe by checking `es -version` (should show "ES X.X.X.X"). The real es.exe ships with Everything install at `C:\Program Files (x86)\Everything\es.exe`.

7. **HTTP Server is the fallback.** If the CLI doesn't work (service not running, fake es.exe), use the Everything HTTP Server API on `http://127.0.0.1:80` — it works as long as Everything GUI is running, even if the local service process isn't detected by tasklist.

8. **Don't assume "not installed" without checking.** The user corrected me: Everything IS installed and the HTTP server IS running. Always try the HTTP API (`http://127.0.0.1:80`) before concluding anything is broken. Also verify the es.exe is real (not a cmd.exe rename) with `es -version`.

9. **User skills vs repo skills.** Hermes loads skills from multiple directories:
   - **Repo skills**: `<HERMES_HOME>/skills/` and `<HERMES_HOME>/hermes-agent/skills/` — bundled with Hermes, overwritten on update
   - **User skills**: `~/.hermes/skills/` — personal/custom skills, safe from updates
   - **External skill repos**: some users keep skills in git repos like `~/TaoTomate.Dots/agent-config/skills/` (not auto-loaded by Hermes)
   When `skill_manage` says "not found", the skill may be a user skill in a non-standard location. Use `search_files` or direct file reads to locate it.

10. **User's skill library pattern.** This user keeps a separate skill repo (`TaoTomate.Dots`) with SDD workflow skills. To apply operations to ALL installed skills across all locations, enumerate directories from all three sources:
    ```python
    sources = [
        "<HERMES_HOME>/skills",
        "<HERMES_HOME>/hermes-agent/skills",
        "~/.hermes/skills",
    ]
    ```
    Deduplicate by skill name, prioritizing user skills over repo skills when names collide.

## References

- `references/fake-es-exe-discovery-2026-06.md` — how to detect a renamed cmd.exe masquerading as es.exe

## Verification

After running a search:
- If output has paths → success, present results to user
- If output is empty → check service status (Step 1), then try fallback to `find`
- If `es.exe /?` shows non-Everything output → binary is fake, inform user and fall back to `find`
- If `es.exe` itself doesn't exist → inform user Everything CLI is not installed at the expected path


## Guardrails (Critical Rules)
- **NEVER** execute destructive operations without explicit user confirmation
- **ALWAYS** verify target exists before operating
- **ALWAYS** handle errors gracefully — skip with warning, don't crash


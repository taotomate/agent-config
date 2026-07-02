---
name: hermes-gateway-windows
description: "Run and troubleshoot the Hermes gateway on Windows — startup, Telegram, service lifecycle, path quirks."
version: 1.0.0
author: agent
model_tier: medium
platforms: [windows]
metadata:
  hermes:
    tags: [hermes, gateway, telegram, windows, service, startup]
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
- Triggers: "hermes-gateway-windows", "use hermes-gateway-windows"


# Hermes Gateway on Windows

Class-level skill for operating the Hermes gateway process on Windows — starting it, wiring Telegram, fixing the common dead-process problem, and understanding the non-obvious path layout.


## Key Facts About This Setup

- **hermes.cmd location**: `C:\Users\user\AppData\Roaming\local\hermes-bin\hermes.cmd`
  - Wrapper that calls `D:\Engram_SDD\Hermes-Nous\hermes-agent\venv\Scripts\hermes.exe`
- **HERMES_HOME**: `D:\Engram_SDD\Hermes-Nous\hermes-data` (not `~/.hermes` — set via env var)
- **Config file**: `D:\Engram_SDD\Hermes-Nous\hermes-data\config.yaml`
- **Env/secrets**: `D:\Engram_SDD\Hermes-Nous\hermes-data\.env`
- **Logs**: `D:\Engram_SDD\Hermes-Nous\hermes-data\logs\gateway.log`
- **Gateway state**: `D:\Engram_SDD\Hermes-Nous\hermes-data\gateway_state.json`
- **Startup item**: `C:\Users\user\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\Hermes_Gateway.cmd`

Use the full path to hermes.cmd in bash/execute_code contexts:
`/c/Users/user/AppData/Roaming/local/hermes-bin/hermes.cmd`

## Telegram Configuration

Telegram is configured via `.env` (not config.yaml `platforms:` section). The active keys:

```
TELEGRAM_BOT_TOKEN=<token>
TELEGRAM_HOME_CHANNEL=6391081685
TELEGRAM_ALLOWED_USERS=6391081685
```

The `gateway.platforms: {}` in config.yaml being empty is normal — Telegram picks up from env vars automatically.

**TELEGRAM_ALLOWED_USERS must be the user's numeric Telegram ID, not the bot's @username.**
The user's ID is `6391081685` (Manu). Setting it to `@System_Rootbot` causes every inbound message to be silently rejected with "Unauthorized user" — the bot receives messages fine but never processes them.

## Checking Status

```bash
hermes.cmd gateway status
```

Two things to check:
1. "Windows login item installed" — startup item present
2. "Gateway process running (PID: XXXX)" — process actually running

The `gateway_state.json` may say `"state": "running"` with a stale PID from a previous run.
**Do not trust gateway_state.json** — always use `gateway status` to verify the process is live.

## Starting / Stopping

```bash
# Start (spawns background process)
hermes.cmd gateway start

# Stop
hermes.cmd gateway stop

# Restart
hermes.cmd gateway restart

# Check logs
tail -30 "D:\Engram_SDD\Hermes-Nous\hermes-data\logs\gateway.log"
```

After `gateway start`, wait 4-5 seconds then check logs to confirm Telegram connected:
```
[Telegram] Connected to Telegram (polling mode)
✓ telegram connected
Gateway running with 1 platform(s)
```

## Install as Windows Startup Service

Already installed in this setup. If needed to reinstall:
```bash
hermes.cmd gateway install
```

This creates a `.cmd` file in the Windows Startup folder that launches the gateway minimized on login.

## Common Problem: Gateway Installed But Not Running

The most common scenario: `gateway status` shows startup item present but no process.

**Cause**: The process was killed (reboot, crash, manual kill) and the startup item didn't fire yet (or user hasn't rebooted).

**Fix**: Just run `hermes.cmd gateway start`. It spawns the process immediately without needing a reboot.

## Pitfalls

### Running hermes from bash/execute_code
`hermes` or `hermes.cmd` without full path fails in bash because the Windows PATH isn't fully inherited.
Always use the full POSIX path:
```bash
'/c/Users/user/AppData/Roaming/local/hermes-bin/hermes.cmd' gateway status
```

Or use execute_code with `terminal()` and the full path.

### Interactive wizard needs PTY
`hermes.cmd gateway setup` is interactive — it will hang waiting for input if called in a non-interactive context. Use it from PowerShell/Windows Terminal directly, or pipe `Y\n` if you just need to confirm a prompt. For non-interactive configuration, edit `.env` and `config.yaml` directly.

### gateway setup wizard prompt
When setup detects an installed-but-not-running gateway, it asks:
```
⚠ Gateway service is installed but not running.
  Start it now? [Y/n]:
```
Bypass this entirely by using `hermes.cmd gateway start` directly.

### HERMES_HOME vs ~/.hermes
This install uses a custom HERMES_HOME. Commands like `cat ~/.hermes/config.yaml` will NOT find the config. Always use the explicit path `D:\Engram_SDD\Hermes-Nous\hermes-data\` or check `$HERMES_HOME`.

### HomeAssistant error is harmless
The gateway log shows `[Homeassistant] Failed to connect: q/api/websocket` — this is because `HASS_URL=q` in `.env` is a placeholder. It does not affect Telegram. The gateway starts with 1 platform (Telegram) and logs a reconnection watcher for HA.

### gateway_state.json stale PID
After a crash or kill, `gateway_state.json` may show `"gateway_state": "running"` with a dead PID. `hermes.cmd gateway status` does a live process check and correctly reports the process as absent. The stale state file is overwritten on next start.

### Startup watchdog script may be missing
`hermes.cmd gateway install` creates a startup item at:
`C:\Users\user\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\Hermes_Gateway.cmd`

That item calls `C:\Users\user\AppData\Local\hermes\gateway-service\Hermes_Gateway.cmd` — but that second script can go missing after updates or installs. If the startup item exists but the gateway never auto-starts after reboot, the watchdog script is probably absent.

Fix — create it manually:
```
C:\Users\user\AppData\Local\hermes\gateway-service\Hermes_Gateway.cmd
```
Contents:
```bat
@echo off
rem Hermes Agent Gateway - Auto-restart watchdog
:loop
"C:\Users\user\AppData\Roaming\local\hermes-bin\hermes.cmd" gateway run
timeout /t 5 /nobreak >nul
goto loop
```
The `goto loop` means if the process dies it restarts automatically within 5 seconds. This is the correct content — `gateway run` (not `gateway start`) because `run` is the foreground command the watchdog wraps.

## Verifying Telegram Connection

After starting, confirm in logs:
```
[Telegram] set_my_commands OK ...  (30 cmds registered)
[Telegram] Connected to Telegram (polling mode)
✓ telegram connected
```

Then send a message to `@System_Rootbot` in Telegram — it should respond.

### Messages arrive but bot doesn't respond

If the bot receives messages (Telegram shows them delivered) but never replies, check logs for:
```
WARNING gateway.run: Unauthorized user: <id> (<name>) on telegram
```

This means the user's numeric Telegram ID is not in TELEGRAM_ALLOWED_USERS. The fix:
```bash
sed -i 's/TELEGRAM_ALLOWED_USERS=.*/TELEGRAM_ALLOWED_USERS=6391081685/' \
  '/d/Engram_SDD/Hermes-Nous/hermes-data/.env'
sed -i 's/TELEGRAM_HOME_CHANNEL=.*/TELEGRAM_HOME_CHANNEL=6391081685/' \
  '/d/Engram_SDD/Hermes-Nous/hermes-data/.env'
```
Then restart: `hermes.cmd gateway restart`

Common mistake: setting TELEGRAM_ALLOWED_USERS to the bot's @username instead of the human user's numeric ID.

## Updating Hermes

```bash
hermes.cmd update
```

**Windows-specific: hermes.exe locked during update.**
On Windows, `hermes update` replaces `hermes.exe` in-place. If the gateway or the current agent session is running, the file is locked and uv will error:
```
error: failed to remove file `...\Scripts\hermes.exe`: The process cannot access the file because it is being used by another process. (os error 32)
```

The update script handles this gracefully — it downloads the ZIP, extracts the new Python code (89+ files updated), and schedules the .exe replacement. The code is live immediately; only the .exe shim needs a restart to fully replace.

**To do a clean update with no lock errors:**
1. Stop the gateway: `hermes.cmd gateway stop` (or `taskkill /F /IM hermes.exe` from cmd.exe if stop hangs)
2. Close any active `hermes.cmd` CLI sessions
3. Run update from a non-hermes context (PowerShell, cmd.exe, or a fresh terminal that did NOT invoke hermes.exe)
4. Re-run `hermes.cmd gateway start` after

Note: if you ARE running inside a hermes agent session (like this one), you cannot kill your own hermes.exe. The update will still apply the new Python code via ZIP — just restart the gateway afterward to get the new shim too.

After update, restart the gateway:
```bash
hermes.cmd gateway restart
```

## References

- `references/gateway-windows-session-2026-06.md` — first successful setup session details


## Guardrails (Critical Rules)
- **NEVER** execute destructive operations without explicit user confirmation
- **ALWAYS** verify target exists before operating
- **ALWAYS** handle errors gracefully — skip with warning, don't crash


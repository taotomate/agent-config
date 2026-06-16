# Gateway Windows Setup — Session 2026-06-01

## Environment

- Hermes v0.14.0
- HERMES_HOME: D:\Engram_SDD\Hermes-Nous\hermes-data
- hermes.cmd: C:\Users\user\AppData\Roaming\local\hermes-bin\hermes.cmd
- Bot: @System_Rootbot
- Home channel: @System_Rootbot
- Allowed users: @System_Rootbot
- Model: Claude Sonnet 4.6 via Anthropic API

## What Was Found

- TELEGRAM_BOT_TOKEN already present in .env (set in a prior session)
- gateway.platforms: {} in config.yaml — empty is correct, Telegram reads from .env
- Gateway was installed as Windows startup item but the process had died
- gateway_state.json showed stale "running" state with dead PID 22732

## Fix Applied

Single command:
```
hermes.cmd gateway start
```

Output: "✓ Gateway started via direct spawn (PID 7444)"

## Log Confirmation (success markers)

```
2026-06-01 07:23:14 INFO [Telegram] set_my_commands OK for scope BotCommandScopeDefault (30 cmds)
2026-06-01 07:23:14 INFO [Telegram] Telegram menu: 30 commands registered, 14 hidden
2026-06-01 07:23:14 INFO [Telegram] Connected to Telegram (polling mode)
2026-06-01 07:23:14 INFO ✓ telegram connected
2026-06-01 07:23:14 INFO Gateway running with 1 platform(s)
```

## What Did Not Work

- `hermes.cmd gateway setup` — wizard blocked waiting for stdin in bash context
- `hermes gateway status` (no .cmd) — routed to Windows system hermes, errored
- `cmd.exe /c "hermes.cmd gateway status 2>&1"` — output swallowed, no redirect capture
- hermes.cmd without full path in bash execute_code context — PATH not inherited

## What Worked

Using full POSIX path in execute_code terminal() calls:
```python
terminal("'/c/Users/user/AppData/Roaming/local/hermes-bin/hermes.cmd' gateway status")
```

## Non-Critical Issues Left

- HASS_URL=q in .env — HomeAssistant fails to connect, harmless
- Hermes 553 commits behind as of session date — update pending

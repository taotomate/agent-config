# Hermes Workspace Deploy — Session 2026-06-07

## What Was Done

Successfully deployed Hermes Workspace Web UI on localhost:3000, connecting to the gateway API on :8642.

### Steps Executed

1. Confirmed `API_SERVER_ENABLED=true` and `API_SERVER_HOST=0.0.0.0` already in `.env`
2. Discovered `API_SERVER_KEY` was missing — gateway refused to start API server
3. Generated key: `python -c "import secrets; print(secrets.token_urlsafe(32))"`
4. Added `API_SERVER_KEY` to `.env` with descriptive comment
5. Restarted gateway: `hermes.cmd gateway restart` — API server now listening on :8642
6. Attempted `hermes dashboard` — crashed with importlib.metadata TypeError (Python 3.11 bug)
7. Cloned repo into `D:\Engram_SDD\hermes-workspace\`
8. Created `.env` with `HERMES_API_URL`, `HERMES_API_TOKEN`, `HOST`, `PORT`, `COOKIE_SECURE`
9. `pnpm install` — 1253 packages (noted `pnpm approve-builds` warning for electron/esbuild)
10. `pnpm dev` — localhost:3000 responding 200 OK

### Final State

- Gateway API: `http://0.0.0.0:8642` (REST/SSE + Telegram)
- Workspace UI: `http://localhost:3000` (200 OK)
- Dashboard: NOT running (crashes on Python 3.11, not required for workspace)
- Repo: `D:\Engram_SDD\hermes-workspace\`

## Pitfalls Discovered

### API_SERVER_KEY is mandatory
Even on localhost, gateway refuses to start API server without it.
Log: `[Api_Server] Refusing to start: API_SERVER_KEY is required for the API server, including loopback-only binds on 0.0.0.0.`

### Dashboard crash (Python 3.11)
```
TypeError: Pair.__new__() missing 1 required positional argument: 'value'
```
Path: `importlib/metadata/__init__.py` line 102 and `_collections.py` line 30.
Non-blocking — workspace functions without dashboard. Possible fix: `pip install --force-reinstall importlib-metadata` or Python 3.12+.

### pnpm approve-builds warning
After install, electron/esbuild/unrs-resolver build scripts are blocked. Ignorable for web-only mode.

### Gateway already running conflict
`hermes gateway run` errors if a gateway is already active. Always use `hermes gateway restart` when reconfiguring.

## Workspace .env Template (Local Dev)

```env
# Hermes Agent API (gateway REST/SSE en :8642)
HERMES_API_URL=http://127.0.0.1:8642
HERMES_API_TOKEN=***
# Server
PORT=3000
HOST=127.0.0.1
# Dashboard (optional — sessions/skills browser)
HERMES_DASHBOARD_URL=http://127.0.0.1:9119
# Security — localhost sin HTTPS
COOKIE_SECURE=0
# HermesWorld (multiplayer hub)
VITE_HERMESWORLD_ENABLED=1
VITE_PLAYGROUND_WS_URL=wss://hermes-playground-ws.myaurora-agi.workers.dev/playground
VITE_PLAYGROUND_STATS_URL=https://hermes-playground-ws.myaurora-agi.workers.dev/stats
```

## Key Files

- Gateway `.env`: `D:\Engram_SDD\Hermes-Nous\hermes-data\.env` (API_SERVER_ENABLED, API_SERVER_KEY, API_SERVER_HOST)
- Workspace `.env`: `D:\Engram_SDD\hermes-workspace\.env` (HERMES_API_URL, HERMES_API_TOKEN)
- Gateway log: `D:\Engram_SDD\Hermes-Nous\hermes-data\logs\gateway.log`
- Source code (API server config): `hermes-agent/gateway/config.py` — reads API_SERVER_ENABLED, API_SERVER_KEY, API_SERVER_HOST, API_SERVER_PORT, API_SERVER_CORS_ORIGINS

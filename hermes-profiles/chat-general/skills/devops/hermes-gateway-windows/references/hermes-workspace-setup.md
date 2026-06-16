# Hermes Workspace — Web UI Setup

Repo: https://github.com/outsourc-e/hermes-workspace
Version: v2.3.0 (zero-fork — runs on vanilla NousResearch/hermes-agent)

## What It Provides

Chat (SSE streaming), memory/skills browser, file explorer + Monaco editor,
cross-platform PTY terminal, multi-agent dashboard with persona presets
(Sage/Trader/Builder/Scribe/Ops), Agent View, Conductor (mission dispatch),
Swarm Mode (tmux-backed workers with role-based dispatch), MCP catalog/marketplace,
Kanban TaskBoard, cost ledger, themes, PWA install.

## Prerequisites

- Node.js 22+ (Manu has v24.13.0 ✅)
- pnpm (Manu has 10.16.1 ✅)
- Hermes Agent gateway with API server enabled (see below)
- Hermes dashboard running on :9119

## Gateway Requirements (CRITICAL)

The workspace connects to TWO services:

1. **Gateway API** (:8642) — chat, completions, models
2. **Dashboard API** (:9119) — sessions, skills, memory, jobs, config

Both must be reachable. The gateway API requires explicit opt-in:

```
# In HERMES_HOME/.env (D:\Engram_SDD\Hermes-Nous\hermes-data\.env):
API_SERVER_ENABLED=true
API_SERVER_HOST=0.0.0.0   # listen on all interfaces (needed for workspace)
API_SERVER_KEY=<random-secret>  # ⚠️ MANDATORY — gateway refuses to start without it
```

### ⚠️ API_SERVER_KEY is required (not optional!)

The gateway **refuses to start the API server** if `API_SERVER_KEY` is missing,
even on localhost. See `references/api-server-key-requirement.md` for full details.

Generate a key:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Without `API_SERVER_ENABLED=true` + `API_SERVER_KEY`, the gateway does NOT serve :8642
and the workspace will show "Offline" / "Connection refused".

The dashboard is a separate process:
```bash
hermes dashboard   # starts on :9119
```

### Verification

```bash
curl -H "Authorization: Bearer <KEY>" http://127.0.0.1:8642/health
curl http://127.0.0.1:9119/api/status
```

## Installation (Attach to Existing Hermes Agent)

Since Hermes Agent is already installed, use the "attach" path:

```bash
git clone https://github.com/outsourc-e/hermes-workspace.git
cd hermes-workspace
pnpm install
cp .env.example .env

# Point at existing Hermes services
echo 'HERMES_API_URL=http://127.0.0.1:8642' >> .env
echo 'HERMES_DASHBOARD_URL=http://127.0.0.1:9119' >> .env

# Gateway auth (required when API_SERVER_KEY is set)
echo 'HERMES_API_TOKEN=<your-API-SERVER-key>' >> .env

pnpm dev   # starts on http://localhost:3000
```

## Portable Mode (No Gateway)

If you just want chat without sessions/memory/skills, point directly at any
OpenAI-compatible backend (Ollama, LM Studio, etc.):

```bash
HERMES_API_URL=http://127.0.0.1:11434 pnpm dev
```

Sessions, memory, skills show "Not Available" — expected in portable mode.

## Docker Compose Alternative

```bash
cp .env.example .env
# Set at least one provider key in .env
docker compose up --build
```

Opens gateway (:8642), dashboard (:9119), and workspace (:3000).

## Remote Access (Tailscale / LAN)

Set both URLs to the reachable address (not 127.0.0.1):

```bash
echo 'HERMES_API_URL=http://100.x.y.z:8642' >> .env
echo 'HERMES_DASHBOARD_URL=http://100.x.y.z:9119' >> .env
```

And in the gateway's env: `API_SERVER_HOST=0.0.0.0`

After workspace is running, URLs can also be updated from
Settings → Connection in the UI (persisted to `~/.hermes/workspace-overrides.json`).

## Ollama with Workspace

Works via custom_providers in config.yaml (already configured in this setup).
Make sure Ollama has CORS enabled:

```bash
OLLAMA_ORIGINS=* ollama serve
```

Use `http://127.0.0.1:11434/v1` (not `localhost`) as the base URL.

## Security Notes

- Fail-closed: refuses to bind non-loopback without `HERMES_PASSWORD`
- `HERMES_PASSWORD` required when `HOST ≠ 127.0.0.1`
- For plain-HTTP LAN: `COOKIE_SECURE=0` (else browsers drop session cookies)
- Path-traversal guard on file/memory routes
- CSP headers, rate limiting, HttpOnly+SameSite+Secure cookies

## Key Defaults

- Workspace UI: :3000 (override with `PORT=4000 pnpm dev`)
- Gateway API: :8642
- Dashboard: :9119

## See Also

- `references/api-server-key-requirement.md` — critical pitfall: API_SERVER_KEY mandatory

# Gateway Architecture — Key Clarification

## Gateway is NOT an HTTP Server

**Critical:** Hermes Gateway on Windows is **not** an HTTP web server. It does not listen on any port.

The Gateway is an **internal orchestrator**:
- Connects to Telegram via **long polling** (outbound to `api.telegram.org`)
- Dispatches tasks to Ollama/LLMs via `localhost:11434/v1`
- Manages cron jobs and agent lifecycle
- All connections are **outbound** — no inbound port needed

## Implications

- `netstat` will NOT show a "gateway port" like 3000
- Cloudflare Tunnel is **NOT** needed for Telegram to work
- Cloudflare Tunnel is only useful for custom HTTP endpoints (webhooks from other services, web UI, API)
- Telegram works as long as the PC has internet — no port forwarding, no tunnel required

## Gateway Config Settings

- `dispatch_interval_seconds: 60` — checks for pending tasks every 60s
- `gateway_auto_continue_freshness: 3600` — re-evaluates tasks every hour
- `gateway_timeout: 1800` — 30 min timeout per task
- `gateway_notify_interval: 180` — notifies every 3 minutes
- `base_url: http://localhost:11434/v1` — points to Ollama

## When to Use Cloudflare Tunnel

**Use for:**
- Custom webhooks from external services
- Web-based control panel accessible from mobile
- API endpoints for integrations
- n8n webhooks pointing to local machine

**Do NOT use for:**
- Telegram bot (uses long polling, no inbound needed)
- Ollama API (local only)
- LM Studio (local only)
- Any service that only makes outbound connections

## Verifying Telegram Connection

Check logs after starting gateway:
```
[Telegram] set_my_commands OK ...  (30 cmds registered)
[Telegram] Connected to Telegram (polling mode)
✓ telegram connected
Gateway running with 1 platform(s)
```

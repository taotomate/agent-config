# Cloudflare Tunnel — Hybrid Local + External Access

## When to Use

When you want Hermes Gateway running locally on your PC but accessible from the internet — for webhooks, Cron Jobs, or mobile access — without exposing your PC directly or needing a VPS.

## Why Cloudflare Tunnel

- No public IP or port forwarding needed (outbound-only connection)
- Free unlimited tunnels, no custom domain required (`*.trycloudflare.com`)
- Automatic HTTPS, DDoS protection included
- Alternative to ngrok (no rate limits on free tier) and Tailscale Funnel

## Setup Steps

### 1. Install cloudflared

Chocolatey may time out. Direct download is more reliable:

```bash
mkdir -p /c/Users/user/bin
curl -L -o /c/Users/user/bin/cloudflared.exe \
  "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe"
```

Verify:
```bash
/c/Users/user/bin/cloudflared.exe --version
```

### 2. Start Gateway + Tunnel

```bash
# Terminal 1: start Hermes gateway
hermes.cmd gateway start

# Terminal 2: create tunnel (replace 3000 with actual gateway port)
/c/Users/user/bin/cloudflared.exe tunnel --url http://localhost:3000
```

Cloudflare outputs a public URL like `https://random-name.trycloudflare.com`.

### 3. Use the URL

Set it as your Telegram webhook or any service endpoint that needs to reach your local gateway.

### 4. Make It Persistent

Create `C:\Users\user\bin\cloudflared-watchdog.bat`:

```bat
@echo off
:loop
"C:\Users\user\bin\cloudflared.exe" tunnel --url http://localhost:3000
timeout /t 5 /nobreak >nul
goto loop
```

Place it in the Windows Startup folder: `C:\Users\user\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\`

## Architecture

```
Hermes Gateway (localhost:3000) → Cloudflare Tunnel → https://name.trycloudflare.com → Internet
                                          ↓
                              Telegram / Webhooks / API calls
```

## Limitations

- **PC off = tunnel down.** For true 24/7 uptime, use a VPS. This is the "local but accessible" hybrid pattern.
- URL changes each tunnel restart unless you create a named tunnel (requires Cloudflare account).
- Free tier subdomains are random (`*.trycloudflare.com`). For a fixed domain, you need a Cloudflare-managed domain.
- **Not needed for Telegram:** Hermes uses long polling (outbound), not webhooks (inbound). Cloudflare Tunnel adds zero value for the Telegram bot itself. Only useful for custom HTTP endpoints.

## Alternatives

| Tool | Free Tier | Fixed URL | Notes |
|------|-----------|-----------|-------|
| Cloudflare Tunnel | ✅ Unlimited | ❌ Random (named tunnels need account) | Best overall |
| ngrok | ⚠️ Limited | ❌ Random on free | 40 conn/min limit |
| Tailscale Funnel | ✅ | ✅ | Needs Tailscale |
| LocalXpose | ⚠️ | ❌ | Less known |

## Status (2026-06-02)

- `cloudflared` installed at `C:\Users\user\bin\cloudflared.exe` (v2026.5.2)
- Not yet configured with a named tunnel — pending user decision on use case
- Decision deferred: user wants to clarify production goals before setting up persistent tunnel

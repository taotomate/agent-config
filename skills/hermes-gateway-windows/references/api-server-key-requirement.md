# API Server Key Requirement (Critical Pitfall)

**Discovered**: 2026-06-07 session

## The Problem

When `API_SERVER_ENABLED=true` is set in `.env` but `API_SERVER_KEY` is absent,
the gateway **refuses to start the API server** — even on localhost.

Log output:
```
[Api_Server] Refusing to start: API_SERVER_KEY is required for the API server,
including loopback-only binds on 0.0.0.0.
```

The gateway falls back to "1 platform (Telegram)" and the API server never binds :8642.

## The Fix

Generate a random key and add it to `.env`:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
# Output example: P-NGgqAvMiupagbudaNk47k_K-dYmP6MwWpRULKEeUg
```

```
API_SERVER_KEY=P-NGgqAvMiupagbudaNk47k_K-dYmP6MwWpRULKEeUg
```

Then: `hermes.cmd gateway restart`

## For Hermes Workspace

The workspace `.env` must carry the same key:
```
HERMES_API_TOKEN=P-NGgqAvMiupagbudaNk47k_K-dYmP6MwWpRULKEeUg
```

## Verification

```bash
netstat -ano | grep 8642 | grep LISTENING
curl -H "Authorization: Bearer <key>" http://127.0.0.1:8642/health
```

## Required Env Vars (complete set)

| Variable | Required | Default | Notes |
|---|---|---|---|
| API_SERVER_ENABLED | Yes | false | Must be "true", "1", or "yes" |
| API_SERVER_KEY | Yes | (none) | Bearer token; gateway refuses without it |
| API_SERVER_HOST | No | 127.0.0.1 | 0.0.0.0 for LAN/Tailscale access |
| API_SERVER_PORT | No | 8642 | Override if needed |
| API_SERVER_CORS_ORIGINS | No | (none) | Set for cross-origin workspace access |

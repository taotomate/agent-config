# Multi-Agent Architecture: Hermes + OpenCode + Antigravity CLI

**Last updated**: 2026-06-09

## Vision

Hermes Agent (OWL) as orchestrator, delegating coding tasks to specialized subagents:
- **Antigravity CLI** — Google's agentic coding CLI (uses Google's LLMs)
- **OpenCode** — Open-source terminal coding agent (uses OpenRouter or any provider)

Each subagent has its own LLM — OWL doesn't pay for their tokens.

## Architecture

```
Hermes Agent (OWL) — orchestrator
├── Antigravity CLI → subagente programador (LLM de Google)
├── OpenCode → subagente programador (LLM via OpenRouter)
└── Workers Kanban → subagentes efémeros por tarea
```

## ACP (Agent Communication Protocol)

Both OpenCode and Hermes support ACP:
- **Hermes**: `hermes acp` starts the ACP adapter server (see `acp_adapter/` in repo)
- **OpenCode**: Has ACP Support section in docs
- **Antigravity CLI**: NOT confirmed — needs testing

## Setup Status (Jun 2026)

| Component | Status | Notes |
|-----------|--------|-------|
| Hermes ACP server | ✅ Available | `hermes acp` command |
| OpenCode ACP client | ✅ Available | Docs confirm ACP support |
| Antigravity CLI ACP | ❓ Untested | User has it installed, needs testing |
| Kanban multi-modelo | ✅ Configured | 6 profiles, workers efémeros |

## Key Files

- Hermes ACP adapter: `acp_adapter/entry.py`, `acp_adapter/server.py`
- OpenCode docs: https://opencode.ai/docs
- Antigravity: https://antigravity.google/product/antigravity-cli

## Next Steps

1. Test Antigravity CLI — run it, check ACP support
2. Install OpenCode — `curl -fsSL https://opencode.ai/install | bash`
3. Configure OpenCode with OpenRouter model
4. Test ACP connection: Hermes as server, OpenCode/Antigravity as clients
5. Set up Kanban tasks that delegate to these subagents

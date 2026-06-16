# OpenCode Windows Configuration — Reference

## Tested: v1.4.0 on Windows 11 (Hermes host, 2026-06-05)

> **⚠️ Repo archived**: The opencode-ai/opencode GitHub repository was archived (read-only) on Sep 18, 2025. v1.4.0 is the last available version. No further updates expected. Consider this when evaluating long-term viability vs alternatives (aider, goose, etc.).

## Files
- Config: `~/.config/opencode/opencode.json`
- Auth: `~/.local/share/opencode/auth.json`
- DB: `~/.local/share/opencode/opencode.db`
- Binary: `C:\Users\user\AppData\Roaming\npm\opencode` (npm global install). In bash, `which opencode` resolves to `/c/Users/user/AppData/Roaming/npm/opencode`. Also accessible via `npx opencode`.

## Valid opencode.json Top-Level Keys (v1.4.0)
- `$schema`
- `agent`
- `mcp`
- `permission`
- `model`

**NOT valid:** `providers` — causes `Configuration is invalid` error.

## Pre-Existing Config (Do Not Overwrite)

On Hermes hosts, `opencode.json` may already contain:
- SDD agent definitions (sdd-orchestrator, sdd-apply, sdd-design, sdd-spec, sdd-tasks, sdd-verify, sdd-archive, sdd-explore, sdd-init, sdd-onboard, sdd-propose)
- MCP servers: Engram (local stdio), context7 (remote)
- Custom permissions (deny .env/.credentials reads, ask on git push/force push)
- Custom agent: "gentleman" (Senior Architect persona)

**Always back up before modifying:**
```bash
cp ~/.config/opencode/opencode.json ~/.config/opencode/opencode.json.bak
```

**Validate JSON after edits (python3 not available on this host):**
```bash
node -e "JSON.parse(require('fs').readFileSync(process.env.HOME+'/.config/opencode/opencode.json','utf8')); console.log('JSON valid ✅')"
```

## Provider Registration

### What Works
1. **Environment variables** — OpenCode auto-detects `OPENROUTER_API_KEY`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, etc.
2. **Interactive login** — `opencode providers login` (interactive picker)
3. **Auth JSON** — `~/.local/share/opencode/auth.json` with `{ "provider": { "type": "api", "key": "..." } }`

### What Doesn't Work
- `opencode auth login -p ollama` → `Unknown provider "ollama"`
- Adding `providers` key to `opencode.json` — causes `Configuration is invalid`
- Putting a URL in auth.json `key` field → `Malformed LM Studio API token`

## Command Reference (v1.4.0)

| Command | Purpose |
|---------|---------|
| `opencode providers list` | List configured providers & credentials |
| `opencode providers login` | Interactive provider login picker |
| `opencode providers logout` | Remove a configured provider |
| `opencode debug config` | Show full resolved config (incl. env-detected providers) |
| `opencode debug agent <name>` | Show agent config details |
| `opencode debug paths` | Show global paths (data, config, cache) |

**Note:** `opencode auth login` is legacy. Use `opencode providers` in v1.4.0.

## Hermes Host Quirks
- API keys in Hermes config appear as `***` — encrypted, not extractable by agent
- `python3` not on PATH — use `node -e "..."` for JSON validation
- `7z` not available — use `tar -czf` for compression
- `rsync` not available — use `cp -r` for directory copies
- `execute_code` scripts may need user approval on each run

## Error Reference

| Error | Cause | Fix |
|-------|-------|-----|
| `Configuration is invalid` + `Unrecognized key: "providers"` | `providers` key in opencode.json | Remove it; use env vars or auth.json |
| `Unknown provider "ollama"` | Ollama not built-in | Use OPENAI_API_KEY env var for Ollama's OpenAI-compatible API |
| `Malformed LM Studio API token` | URL in auth.json `key` field | Use actual API key or clear entry |
| `ProviderModelNotFoundError` | Provider not registered | Run `opencode providers list` and configure auth |

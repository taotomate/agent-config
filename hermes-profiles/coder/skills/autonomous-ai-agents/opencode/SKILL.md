---
name: opencode
description: "Delegate coding to OpenCode CLI (features, PR review)."
version: 1.3.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Coding-Agent, OpenCode, Autonomous, Refactoring, Code-Review]
    related_skills: [claude-code, codex, hermes-agent]
---

# OpenCode CLI

Use [OpenCode](https://opencode.ai) as an autonomous coding worker orchestrated by Hermes terminal/process tools. OpenCode is a provider-agnostic, open-source AI coding agent with a TUI and CLI.

## When to Use

- User explicitly asks to use OpenCode
- You want an external coding agent to implement/refactor/review code
- You need long-running coding sessions with progress checks
- You want parallel task execution in isolated workdirs/worktrees

## Prerequisites

- OpenCode installed: `npm i -g opencode-ai@latest` or `brew install anomalyco/tap/opencode`
- Auth configured: `opencode auth login` or set provider env vars (OPENROUTER_API_KEY, etc.)
- Verify: `opencode auth list` should show at least one provider
- Git repository for code tasks (recommended)
- `pty=true` for interactive TUI sessions

## Binary Resolution (Important)

Shell environments may resolve different OpenCode binaries. If behavior differs between your terminal and Hermes, check:

```
terminal(command="which -a opencode")
terminal(command="opencode --version")
```

If needed, pin an explicit binary path:

```
terminal(command="$HOME/.opencode/bin/opencode run '...'", workdir="~/project", pty=true)
```

## One-Shot Tasks

Use `opencode run` for bounded, non-interactive tasks:

```
terminal(command="opencode run 'Add retry logic to API calls and update tests'", workdir="~/project")
```

Attach context files with `-f`:

```
terminal(command="opencode run 'Review this config for security issues' -f config.yaml -f .env.example", workdir="~/project")
```

Show model thinking with `--thinking`:

```
terminal(command="opencode run 'Debug why tests fail in CI' --thinking", workdir="~/project")
```

Force a specific model:

```
terminal(command="opencode run 'Refactor auth module' --model openrouter/anthropic/claude-sonnet-4", workdir="~/project")
```

## Interactive Sessions (Background)

For iterative work requiring multiple exchanges, start the TUI in background:

```
terminal(command="opencode", workdir="~/project", background=true, pty=true)
# Returns session_id

# Send a prompt
process(action="submit", session_id="<id>", data="Implement OAuth refresh flow and add tests")

# Monitor progress
process(action="poll", session_id="<id>")
process(action="log", session_id="<id>")

# Send follow-up input
process(action="submit", session_id="<id>", data="Now add error handling for token expiry")

# Exit cleanly — Ctrl+C
process(action="write", session_id="<id>", data="\x03")
# Or just kill the process
process(action="kill", session_id="<id>")
```

**Important:** Do NOT use `/exit` — it is not a valid OpenCode command and will open an agent selector dialog instead. Use Ctrl+C (`\x03`) or `process(action="kill")` to exit.

### TUI Keybindings

| Key | Action |
|-----|--------|
| `Enter` | Submit message (press twice if needed) |
| `Tab` | Switch between agents (build/plan) |
| `Ctrl+P` | Open command palette |
| `Ctrl+X L` | Switch session |
| `Ctrl+X M` | Switch model |
| `Ctrl+X N` | New session |
| `Ctrl+X E` | Open editor |
| `Ctrl+C` | Exit OpenCode |

### Resuming Sessions

After exiting, OpenCode prints a session ID. Resume with:

```
terminal(command="opencode -c", workdir="~/project", background=true, pty=true)  # Continue last session
terminal(command="opencode -s ses_abc123", workdir="~/project", background=true, pty=true)  # Specific session
```

## Common Flags

| Flag | Use |
|------|-----|
| `run 'prompt'` | One-shot execution and exit |
| `--continue` / `-c` | Continue the last OpenCode session |
| `--session <id>` / `-s` | Continue a specific session |
| `--agent <name>` | Choose OpenCode agent (build or plan) |
| `--model provider/model` | Force specific model |
| `--format json` | Machine-readable output/events |
| `--file <path>` / `-f` | Attach file(s) to the message |
| `--thinking` | Show model thinking blocks |
| `--variant <level>` | Reasoning effort (high, max, minimal) |
| `--title <name>` | Name the session |
| `--attach <url>` | Connect to a running opencode server |

## Procedure

1. Verify tool readiness:
   - `terminal(command="opencode --version")`
   - `terminal(command="opencode auth list")`
2. For bounded tasks, use `opencode run '...'` (no pty needed).
3. For iterative tasks, start `opencode` with `background=true, pty=true`.
4. Monitor long tasks with `process(action="poll"|"log")`.
5. If OpenCode asks for input, respond via `process(action="submit", ...)`.
6. Exit with `process(action="write", data="\x03")` or `process(action="kill")`.
7. Summarize file changes, test results, and next steps back to user.

## PR Review Workflow

OpenCode has a built-in PR command:

```
terminal(command="opencode pr 42", workdir="~/project", pty=true)
```

Or review in a temporary clone for isolation:

```
terminal(command="REVIEW=$(mktemp -d) && git clone https://github.com/user/repo.git $REVIEW && cd $REVIEW && opencode run 'Review this PR vs main. Report bugs, security risks, test gaps, and style issues.' -f $(git diff origin/main --name-only | head -20 | tr '\n' ' ')", pty=true)
```

## Parallel Work Pattern

Use separate workdirs/worktrees to avoid collisions:

```
terminal(command="opencode run 'Fix issue #101 and commit'", workdir="/tmp/issue-101", background=true, pty=true)
terminal(command="opencode run 'Add parser regression tests and commit'", workdir="/tmp/issue-102", background=true, pty=true)
process(action="list")
```

## Session & Cost Management

List past sessions:

```
terminal(command="opencode session list")
```

Check token usage and costs:

```
terminal(command="opencode stats")
terminal(command="opencode stats --days 7 --models anthropic/claude-sonnet-4")
```

## Pitfalls

- Interactive `opencode` (TUI) sessions require `pty=true`. The `opencode run` command does NOT need pty.
- `/exit` is NOT a valid command — it opens an agent selector. Use Ctrl+C to exit the TUI.
- PATH mismatch can select the wrong OpenCode binary/model config.
- If OpenCode appears stuck, inspect logs before killing:
  - `process(action="log", session_id="<id>")`
- Avoid sharing one working directory across parallel OpenCode sessions.
- Enter may need to be pressed twice to submit in the TUI (once to finalize text, once to send).
- **Do NOT add `providers` key to `opencode.json`** — v1.4.0 doesn't recognize it and rejects the entire config. Use env vars or `opencode providers login` instead.
- **`opencode auth login -p ollama` fails** — Ollama is not a built-in provider in v1.4.0. Use `OPENAI_API_KEY` env var to leverage Ollama's OpenAI-compatible API.
- **Auth.json `key` field must be an API key, not a URL** — storing a server URL causes `Malformed LM Studio API token` errors.
- **Windows binary location**: OpenCode v1.4.0 installs to `C:\\Users\\user\\AppData\\Roaming\\npm\\opencode` via npm global. In bash, `which opencode` resolves to `/c/Users/user/AppData/Roaming/npm/opencode`. Also accessible via `npx opencode`.
- **Repo archived**: The opencode-ai/opencode GitHub repo was archived (read-only) on Sep 18, 2025. v1.4.0 is the last available version. No further updates expected. Consider this when evaluating long-term viability vs alternatives (aider, goose, etc.).
- **Pre-existing SDD config**: On Hermes hosts, `opencode.json` may already contain SDD agent definitions (sdd-orchestrator, sdd-apply, etc.), MCP servers (Engram, context7), and custom permissions. Always `opencode debug config` before modifying. Back up before any changes. On this host, `OPENROUTER_API_KEY` is in `D:\Engram_SDD\Hermes-Nous\hermes-data\.env` (encrypted) and referenced from `C:\Users\user\.gemini\antigravity\secrets.env` (also redacted in agent context). The key inventory is at `D:\Engram_SDD\Proj-Seguridad\api-inventory.md` but shows truncated values.

## Provider Configuration (Windows / Hermes Hosts)

### Config Location

OpenCode config lives at `~/.config/opencode/opencode.json`. It may already contain SDD agent definitions, MCP servers (e.g. Engram), and permissions — always read before overwriting. Back up first:
```bash
cp ~/.config/opencode/opencode.json ~/.config/opencode/opencode.json.bak
```

### Command Naming (v1.4.0)

v1.4.0 uses `opencode providers` (not `opencode auth`) for credential management:
- `opencode providers list` — list configured providers
- `opencode providers login` — interactive provider login
- `opencode providers logout` — remove a provider
- `opencode debug config` — show resolved configuration (including env-detected providers)

Older `opencode auth login` still works but `providers` is the canonical command group.

The `opencode.json` schema accepts: `$schema`, `agent`, `mcp`, `permission`, `model`.

**⚠️ The `providers` key is NOT valid in v1.4.0.** Adding it causes `Configuration is invalid` errors. Provider registration happens through auth, not config.

### Auth: LMStudio URL vs API Key

OpenCode's `auth.json` (`~/.local/share/opencode/auth.json`) expects an **API key**, NOT a server URL. LMStudio entries like `{"key": "http://192.168.1.15:1234"}` will cause `Malformed LM Studio API token` errors. Fix by clearing the entry or providing a real token.

### Hermes-Integrated Hosts: API Keys Are Encrypted

On Hermes Windows hosts, `OPENROUTER_API_KEY` and other secrets are stored in Hermes's encrypted credential pool. Values appear as `***` in config.yaml and **cannot be extracted by the agent** through file reads. Options:

1. **Ask the user** to paste the key (find it on the provider's dashboard, e.g. https://openrouter.ai/settings/keys for OpenRouter)
2. **Use environment variables** if they're available in the shell session
3. **Use Ollama local** — free, no rate limit, already configured on most Hermes hosts

### Adding Providers (Correct Approach for v1.4.0)

**Method 1 — Environment variables (recommended):**
Set env vars before running OpenCode. OpenCode auto-detects from environment:
- `OPENROUTER_API_KEY=sk-or-...`
- `OPENAI_API_KEY=ollama` (for Ollama's OpenAI-compatible API at `http://localhost:11434/v1`)
- `ANTHROPIC_API_KEY=...`
- `OLLAMA_API_KEY=ollama`

**Method 2 — Interactive login:**
```bash
opencode providers login
```
Note: The subcommand is `opencode providers login`, NOT `opencode auth login`. v1.4.0 uses the `providers` command group.

**Method 3 — Auth JSON (recognized providers only):**
Edit `~/.local/share/opencode/auth.json`:
```json
{
  "openrouter": {
    "type": "api",
    "key": "sk-or-..."
  }
}
```

**Note:** `opencode providers login -p ollama` returns `Unknown provider "ollama"` — Ollama is not a built-in provider. Ollama's OpenAI-compatible API at `http://localhost:11434/v1` can be used via `OPENAI_API_KEY` env var.

### Inspect Resolved Configuration

Use `opencode debug config` to see the full resolved config including auto-detected providers. This is the fastest way to debug provider/model issues:
```bash
opencode debug config
```

### Default Model

Set the default model in `opencode.json` using the `model` key:
```json
{
  "model": {
    "default": "ollama/qwen3-coder-30b"
  }
}
```
The provider portion (before `/`) must match a registered provider.

### JSON Validation

On Windows, `python3` may not be available. Use Node.js for JSON validation:
```bash
node -e "JSON.parse(require('fs').readFileSync(process.env.HOME+'/.config/opencode/opencode.json','utf8')); console.log('JSON valid ✅')"
```

## Auto-Commit Pattern

For long-running agent sessions, the model may forget to commit changes. Instead of relying on the agent's memory, use an infrastructure-level file watcher that auto-commits on change. See `references/auto-commit-pattern.md` for implementation (inotifywait for Linux/WSL, FileSystemWatcher for Windows/PowerShell).

Smoke test:

```
terminal(command="opencode run 'Respond with exactly: OPENCODE_SMOKE_OK'")
```

Success criteria:
- Output includes `OPENCODE_SMOKE_OK`
- Command exits without provider/model errors
- For code tasks: expected files changed and tests pass

## Rules

1. Prefer `opencode run` for one-shot automation — it's simpler and doesn't need pty.
2. Use interactive background mode only when iteration is needed.
3. Always scope OpenCode sessions to a single repo/workdir.
4. For long tasks, provide progress updates from `process` logs.
5. Report concrete outcomes (files changed, tests, remaining risks).
6. Exit interactive sessions with Ctrl+C or kill, never `/exit`.

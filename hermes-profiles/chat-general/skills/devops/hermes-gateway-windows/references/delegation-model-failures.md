# Delegation Model Failures — Telegram Silent Crash Pattern

## Problem

Telegram bot stops responding (no reply, no error shown to user) while the gateway process itself stays running.

## Root Cause

The `delegation.model` or `providers.openrouter_coding` config keys point to a free OpenRouter model (`:free` suffix) that has been removed or renamed by the provider. When the agent tries to spawn a subagent (for code tasks, search, or any tool-heavy work), the LLM call fails with HTTP 400 "invalid model ID". This crashes the **entire response**, not just the subagent — the user sees nothing.

The primary model (`model.default = openrouter/owl-alpha`) keeps working for direct Q&A. The crash only happens when the agent decides to delegate.

## Known Failed Models (as of 2026-06-02)

- `openrouter/qwen/qwen3-coder:free` — HTTP 400, model removed/renamed
- `openrouter/moonshotai/kimi-k2.6:free` — HTTP 400 (reported by Antigravity agent)

## Working Models (verified 2026-06-02)

- `openrouter/owl-alpha` — stable, primary
- `openrouter/meta-llama/llama-3.3-70b-instruct:free` — works for delegation

## Diagnostic Steps

1. Check gateway is running:
   ```bash
   hermes.cmd gateway status
   ```

2. Check if messages are arriving but not answered:
   ```bash
   tail -30 "D:\Engram_SDD\Hermes-Nous\hermes-data\logs\gateway.log"
   ```
   Look for inbound messages without corresponding `response ready` lines.

3. Check `delegation.model` and `providers.openrouter_coding`:
   ```bash
   hermes.cmd config get delegation.model
   hermes.cmd config get providers.openrouter_coding
   ```
   If either contains `:free` and points to qwen3-coder or kimi-k2.6, that's the problem.

4. Quick-test by sending a message that triggers delegation (e.g., "escribe un script en Python").

## Fix

Replace the failed model with a working free model:

```bash
hermes.cmd config set delegation.model "openrouter/meta-llama/llama-3.3-70b-instruct:free"
hermes.cmd config set providers.openrouter_coding "{\"base_url\":\"https://openrouter.ai/api/v1\",\"model\":\"meta-llama/llama-3.3-70b-instruct:free\",\"provider\":\"openrouter\"}"
hermes.cmd gateway restart
```

Wait 5 seconds, then verify Telegram reconnected in logs.

## Prevention

- **Avoid `:free` models for delegation** — they are the first to disappear without notice.
- If you must use `:free` models, have a known-good fallback ready.
- The `CHANGELOG_OWL.md` file in HERMES_HOME tracks which models have failed and when.
- When Telegram stops responding and the gateway is running, **always check delegation.model first** before investigating anything else.

## Changelog Reference

See `CHANGELOG_OWL.md` in HERMES_HOME for full incident history.

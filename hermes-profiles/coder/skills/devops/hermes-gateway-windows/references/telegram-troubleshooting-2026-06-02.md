# Telegram Troubleshooting Session — 2026-06-02 (Updated)

## Situation

User reported Telegram bot (`@System_Rootbot`) stopped responding after error message about invalid model when bot tried to delegate a coding task. Another agent (Antigravity) had previously modified `.env` and `config.yaml`. Those changes were already reverted by the user.

## What Antigravity's Report Claimed

The agent left a diagnostic file (`ANTIGRAVITY_LOG.md`) claiming:
1. `model.default` pointed to `openrouter/moonshotai/kimi-k2.6:free` (deleted model)
2. `delegation.model` pointed to `openrouter/qwen/qwen3-coder:free` (deleted model)
3. Both models returning HTTP 400, causing crash loop

## What Was Actually True

1. **`model.default`**: Was already `openrouter/owl-alpha` — Antigravity's claim was **false** (stale read or confusion with pre-revert state)
2. **`delegation.model`**: Was `openrouter/qwen/qwen3-coder:free` — correct. This model **was returning HTTP 400** (confirmed by user seeing an error message about invalid model when delegation was attempted)
3. **`providers.openrouter_coding`**: Also pointed to `qwen/qwen3-coder:free` — same broken model
4. **The real failure chain**: User sends message → bot processes it fine with owl-alpha → bot tries to delegate a coding subtask → subagent creation fails with HTTP 400 (invalid model) → the failure cascades and crashes the entire response → bot stops responding
5. **Last working message**: User saw an error message about "modelo invalido" and after that the bot was dead

## Key Lesson: Verify Agent Diagnostic Claims

**Always verify claims from other agents against actual system state before acting.** Agent-generated diagnostic reports can be:
- Based on stale/pre-revert state
- Confused about which config file they read
- Right about the general problem but wrong about the specific details

**Verification steps that should be done:**
1. Read `config.yaml` directly → verify model values
2. `hermes.cmd gateway status` → check if process is running
3. Check `logs/gateway.log` for actual errors
4. `hermes.cmd doctor` → validates config + connectivity

## Additional Findings

- `fallback_providers` in config.yaml is stored as a **serialized string** (single-quoted JSON), not a YAML list. This is a known broken state — `hermes config set` serializes lists as strings. Should be a proper YAML list of dicts.
- HomeAssistant connection failures in logs are harmless (placeholder `HASS_URL=q` in .env)
- `hermes doctor --fix` found nothing auto-fixable — all issues are optional (missing API keys for non-essential toolsets)
- **Free models on OpenRouter can be deleted/renamed without notice.** When a free model in `delegation.model` or `providers.*` disappears, it causes silent failures. Prefer meta-routers (`openrouter/auto`) or well-established free models (`meta-llama/llama-3.3-70b-instruct:free`) for delegation.

## Resolution

1. Changed `delegation.model` from `openrouter/qwen/qwen3-coder:free` to `openrouter/meta-llama/llama-3.3-70b-instruct:free`
2. Changed `providers.openrouter_coding` from `qwen/qwen3-coder:free` to `meta-llama/llama-3.3-70b-instruct:free`
3. Restarted gateway: `hermes.cmd gateway restart` → PID 4928
4. Verified Telegram reconnected: `[Telegram] Connected to Telegram (polling mode)` in logs
5. User confirmed bot was responsive again

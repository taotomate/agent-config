# Hermes config.yaml Editing Patterns

How to safely edit Hermes configuration when setting up providers and integrations.

## Key Insight: `hermes config set` vs `patch` tool

**`hermes config set` only works for top-level or simple keys.** It FAILS for:
- Nested keys with dots (e.g., `telegram.bot_token` → `ValueError: Invalid environment variable name`)
- Provider definitions under `providers:`
- Model fallback lists

**Use `patch` tool for config.yaml edits.** It handles the YAML structure correctly.

## Pattern: Adding a New Provider

Use `patch` with `mode: 'replace'` to insert a new provider block:

```yaml
# In config.yaml under providers:
    openrouter:
        api_key: <your-key-here>
        base_url: https://openrouter.ai/api/v1
        default_model: openrouter/owl-alpha
        models:
            - openrouter/owl-alpha
            - nvidia/nemotron-3-ultra-550b-a55b:free
            - qwen/qwen3-coder:free
        name: OpenRouter
```

## Pattern: Changing the Default Model

```yaml
model:
    api_key: openrouter
    base_url: https://openrouter.ai/api/v1
    default: openrouter/owl-alpha
    provider: openrouter
    fallback:
        - nvidia/nemotron-3-ultra-550b-a55b:free
        - qwen/qwen3-coder:free
```

## Pattern: Configuring Messaging (Telegram, etc.)

Messaging tokens go in `~/.hermes/.env`, NOT in `config.yaml`:

```bash
# In ~/.hermes/.env:
TELEGRAM_BOT_TOKEN=7705044944
TELEGRAM_ALLOWED_USERS=6391081685
TELEGRAM_HOME_CHANNEL=6391081685
```

**After editing `.env`, the gateway must be restarted from OUTSIDE the gateway process:**
```bash
hermes gateway restart
```
Running `hermes gateway restart` from inside the gateway is blocked to prevent restart loops.

## Free Tier OpenRouter Models (2026-06)

Best free models available on OpenRouter:
| Model | Context | Max Tokens |
|-------|---------|------------|
| `openrouter/owl-alpha` | 1M | 262K |
| `qwen/qwen3-coder:free` | 1M | 262K |
| `nvidia/nemotron-3-ultra-550b-a55b:free` | 1M | 65K |
| `nvidia/nemotron-3-super-120b-a12b:free` | 1M | 262K |
| `google/gemma-4-26b-a4b-it:free` | 262K | 32K |
| `google/gemma-4-31b-it:free` | 262K | 8K |
| `google/lyria-3-pro-preview` | 1M | 65K |

**Warning:** Free models have aggressive rate limits. `qwen3-coder:free` was rate-limited immediately in testing. `owl-alpha` is the most stable free option.

## Hermes Status Verification

Always verify current state before making changes:
```bash
hermes status 2>&1 | grep -E "Model|Provider|OpenRouter|Gateway|Messaging"
```
This shows: active model/provider, which API keys are loaded, gateway status, and messaging platform status. Use this BEFORE touching any config to avoid redundant changes.

# Ollama Fallback Provider Setup on Windows

## Configuring Ollama as Fallback for Hermes on Windows

Ollama runs locally at `http://localhost:11434`. Hermes can use it as a fallback provider when the primary provider (e.g. OpenRouter) fails.

### Check Installed Models

```bash
ollama list
```

### Configuration Steps

#### 1. Add Ollama models to `fallback_providers` in config.yaml

```bash
'/c/Users/user/AppData/Roaming/local/hermes-bin/hermes.cmd' config set fallback_providers '[
  {"provider":"ollama","model":"qwen3.6:latest","base_url":"http://localhost:11434/v1"},
  {"provider":"ollama","model":"gemma4:latest","base_url":"http://localhost:11434/v1"},
  {"provider":"ollama","model":"mistral-nemo-12b:latest","base_url":"http://localhost:11434/v1"}
]'
```

#### 2. Configure delegation (subagents) for parallel online execution

```bash
'/c/Users/user/AppData/Roaming/local/hermes-bin/hermes.cmd' config set delegation.model "openrouter/qwen/qwen3-coder:free"
'/c/Users/user/AppData/Roaming/local/hermes-bin/hermes.cmd' config set delegation.provider "openrouter"
'/c/Users/user/AppData/Roaming/local/hermes-bin/hermes.cmd' config set delegation.base_url "https://openrouter.ai/api/v1"
```

#### 3. Set `model.default` to a stable known-working model

```bash
'/c/Users/user/AppData/Roaming/local/hermes-bin/hermes.cmd' config set model.default "openrouter/owl-alpha"
```

#### 4. Ensure `model_catalog.providers.ollama` is set

```bash
'/c/Users/user/AppData/Roaming/local/hermes-bin/hermes.cmd' config set model_catalog.providers.ollama.api_key "ollama-local"
'/c/Users/user/AppData/Roaming/local/hermes-bin/hermes.cmd' config set model_catalog.providers.ollama.base_url "http://localhost:11434/v1"
'/c/Users/user/AppData/Roaming/local/hermes-bin/hermes.cmd' config set model_catalog.providers.ollama.context_length 32768
```

### Notes

- Ollama must be running (`ollama serve`) for fallbacks to work
- The `api_key` field is required but Ollama ignores it — use `"ollama"` or `"ollama-local"` as placeholder
- Model names must match exactly what `ollama list` shows (including `:latest` tag)
- `fallback_providers` is the modern key; `model.fallbacks` is legacy but also read
- Changes take effect on next `/reset` or gateway restart

## ⚠️ CRITICAL: How Fallback Actually Works (and Why It Doesn't)

### The #1 Pitfall: Fallback ≠ Model-Level Failover

`fallback_providers` and `model.fallbacks` **only activate when the entire provider is unreachable** (connection timeout, API down, DNS failure).

They do **NOT** activate when a specific model within a provider crashes, returns errors, or hangs mid-generation.

This means: if `openrouter/owl-alpha` starts returning 500 errors or hangs on specific prompts, Hermes will **NOT** automatically try the next fallback. It will hang/crash on that model.

### The OpenRouter Free Model Problem

Free models on OpenRouter (e.g. `moonshotai/kimi-k2.6:free`) are especially prone to:
- Rate limiting
- Capacity errors
- Unexpected hangs mid-generation

When this happens, the session crashes and the user must manually restore config from a local backup.

### The Solution: Use Meta-Routers Instead

| Meta-Router | Purpose | Why |
|-------------|---------|-----|
| `openrouter/auto` | General chat meta-router | Routes to best available model; if one fails, re-routes automatically |
| `openrouter/pareto-code` | Code-specific meta-router | Routes to best coding model by Artificial Analysis score; 2M context |

These handle model-level failures **internally** within OpenRouter, before Hermes ever sees an error. This is the correct resilience strategy, NOT fallback_providers.

**Do NOT rely on fallback_providers for model-level resilience inside a single provider.**

### Subagent Strategy: Online Parallel, Local Serial

When delegating subagents (`delegate_task`) in parallel:
- **Use online models (OpenRouter)** for subagents that run in parallel — they don't consume local RAM
- **Use local models (Ollama) serially, one at a time** — running 2-3 local models in parallel saturates PC RAM and freezes the system
- Configure `delegation.model` to point to an online model for this reason

## STT (Whisper) NumPy/Numba Fix on Windows

### Symptom
```
ImportError: Numba needs NumPy 2.2 or less. Got NumPy 2.3.
```

### Fix
```bash
/c/Users/user/AppData/Local/Programs/Python/Python313/python -m pip install "numpy<2.3" "numba>=0.59" --force-reinstall
```

### STT Language Setting
Leave `stt.local.language` empty for auto-detection. Do NOT force a language unless explicitly requested.

## User Language Preference

**Respond in the same language the user is speaking.** Do not translate their messages when quoting or referring to them. If they speak Spanish, respond in Spanish. Only switch languages when explicitly asked.

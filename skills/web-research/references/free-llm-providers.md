# Free LLM API Providers (2025-2026)

Discovered via GitHub topics, awesome-free-llm-apis repo, freellmpool, browser tool, and LLM proxy queries.
Last updated: 2026-06-09

## Provider APIs (First-Party)

| Provider | URL | Free Models | Rate Limits | OpenAI Compat | Notes |
|----------|-----|-------------|-------------|---------------|-------|
| Google Gemini | aistudio.google.com | 2.5 Pro, 2.0 Flash, 1.5 Flash, 1.5 Flash-8B | 15 RPM / 1,500 RPD (Flash) | ✅ | No EU/UK/CH |
| Mistral AI | console.mistral.ai | Small 3.1, Large 3, Ministral 8B, Codestral Mamba | 1 req/s / 1B tokens/month | ✅ | Most generous volume |
| Cohere | dashboard.cohere.com | Command A, Command R+, R, Aya Expanse 32B/8B | 20 RPM / 1,000 req/month | ⚠️ Partial | Trial keys |
| Zhipu AI | open.bigmodel.cn | GLM-4.7-Flash, GLM-4.5-Flash, GLM-4.6V-Flash | Undocumented | ✅ | Chinese, no published cap |

## Inference Providers (Third-Party Hosting)

| Provider | URL | Free Models | Rate Limits | Speed | Notes |
|----------|-----|-------------|-------------|-------|-------|
| Groq | console.groq.com | Llama 3.3 70B, Llama 4 Scout/Maverick, Gemma 2 9B, Kimi K2, QwQ 32B + 17 more | 30 RPM / 14,400 RPD / 6,000 TPM | 🟢 300-500 tok/s | LPU hardware |
| Cerebras | cloud.cerebras.ai | Llama 3.3 70B, Qwen3 235B, Llama 4 Scout, GPT-OSS-120B + 3 | 30 RPM / 60,000 TPM / 14,400 RPD | 🟢 Fast | Wafer-scale chip |
| OpenRouter | openrouter.ai | DeepSeek R1, Llama 3.3 70B, GPT-OSS-120B, Qwen3 Coder 480B + 27 (:free models) | 20 RPM / 200 RPD | 🟡 Medium | Routes to various backends |
| GitHub Models | github.com/marketplace/models | GPT-4o, Llama 3.3 70B, DeepSeek-R1, Phi-4, Mistral Large | 10-15 RPM / 50-150 RPD | 🟡 Medium | Includes GPT-4o free! |
| NVIDIA NIM | build.nvidia.com | Llama 3.3 70B, Mistral Large, Qwen3 235B, DeepSeek-R1 | 40 RPM (credit-based) | 🟡 Medium | Credits replenish |
| HuggingFace | huggingface.co | Llama 3.3 70B, Qwen2.5 72B, Mistral 7B, thousands more | $0.10/month credits | 🔴 Slow | Cold starts common |
| Cloudflare | dash.cloudflare.com | Various small models | 10K neurons/day | 🔴 Edge | Small models only |
| Together AI | together.ai | Llama 3 8B Instruct Lite, Llama 3.3 70B, Llama 4 Maverick/Scout | Free credits | 🟡 | Free credits on signup |
| Fireworks AI | fireworks.ai | Various | Free credits | 🟡 | Fast inference |
| Perplexity | perplexity.ai | Sonar models | Per-request pricing | 🟡 | API charges per request |

## Pool / Aggregator Solutions

| Project | URL | Description | Needs Key? |
|---------|-----|-------------|------------|
| freellmpool | github.com/0xzr/freellmpool | Pools 18+ providers behind one OpenAI-compatible endpoint. Auto-failover. Dashboard. | Some need no key (Pollinations, OVHcloud, Kilo Gateway) |
| OpenRouter AutoRouter | openrouter.ai | Auto-routes to free models as fallback | OpenRouter key |
| Pareto | (user mentioned) | Model selection/filtering layer | TBD |

## Key Insights

1. **GitHub Models gives GPT-4o free** — 10-15 RPM, 50-150 RPD
2. **Mistral gives 1 BILLION tokens/month free** — most generous by volume
3. **Cerebras competes with Groq** on speed (wafer-scale chip)
4. **Zhipu AI (China)** has flash models with no published limits
5. **freellmpool** needs NO API key for some providers — works out of the box
6. **Groq's 6,000 TPM limit** is too low for Hermes system prompts (~28K tokens/request)
7. **Google rate limit**: 15 RPM / 1,500 RPD (Flash), 2 RPM / 50 RPD (2.5 Pro)
8. **Perplexity is NOT reliably accessible** — Cloudflare blocks browser, OpenRouter returns 402, needs separate PPLX_API_KEY

## Model Categories for DB Classification

```
chat          → Full conversation, tool calling, 32K+ context
vision        → Image understanding
audio         → Whisper, TTS, transcription (KEEP — useful for translation tasks)
code          → Code-specialized models
fast-burst    → Groq/Cerebras: high speed, low TPM, for batch processing
micro-task    → Small context (4K-8K): classification, tagging (DON'T discard)
embedding     → Text embeddings
```

## Classification Strategy (Vía Negativa — User Approved)

Don't classify by theory — classify by survival:

```
New model → status="candidate" → assign tentative category
→ Use as priority in that category
→ If error → lower priority or change category
→ If fails N times → status="dead" or reclassify to "tool-only"
→ If works → status="active"
```

Track per model:
- `fail_count`: consecutive failures
- `last_error`: error code/message
- `last_tested`: timestamp
- `avg_latency_ms`: rolling average
- `tokens_consumed`: total tokens used in tests
- `category`: chat | vision | audio | code | fast-burst | micro-task | embedding
- `status`: candidate | active | degraded | dead
- `priority`: 1 (highest) to 5 (lowest)

## Token Telemetry (Proposed)

Track per request:
- `tokens_consumed`: tokens used
- `provider_used`: which provider responded
- `latency_ms`: response time
- `error_code`: if failed
- `free_tier_remaining`: estimated remaining free quota

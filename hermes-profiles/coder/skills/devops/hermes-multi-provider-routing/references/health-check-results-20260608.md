# Health Check Results — Post-Filtro de Capacidades (2026-06-08)

## Resumen

- 37 modelos free testeados
- 21 activos (pasaron health check HTTP 200)
- 16 inactivos (fallaron o no pasan filtro de capacidades)
- De los 21 activos: TODOS pasan filtro de ctx>=32K

## 21 Modelos Aptos Activos (por latencia)

| Modelo | Provider | Latencia | Contexto | Tool | Vision | Code | Categoría |
|--------|----------|----------|---------|------|--------|------|-----------|
| llama-3.1-8b-instant | groq | 118ms | 131K | ✓ | | | chat |
| llama-3.3-70b-versatile | groq | 132ms | 131K | ✓ | | | chat |
| nemotron-3-nano-30b | openrouter | 335ms | 256K | | | | lightweight |
| llama-3.3-70b-instruct | openrouter | 339ms | 131K | ✓ | | | chat |
| hermes-3-llama-3.1-405b | openrouter | 341ms | 131K | ✓ | | | agentic |
| gemma-4-26b-a4b-it | openrouter | 350ms | 262K | | ✓ | | general |
| nemotron-nano-9b-v2 | openrouter | 357ms | 128K | | | | lightweight |
| llama-3.2-3b-instruct | openrouter | 398ms | 131K | | | | lightweight |
| gpt-oss-20b | openrouter | 456ms | 131K | ✓ | | | general |
| gemini-2.5-flash | google | 477ms | 1M | ✓ | ✓ | | chat |
| gemini-2.5-flash-lite | google | 587ms | 1M | ✓ | | | chat |
| gpt-oss-120b | openrouter | 607ms | 131K | ✓ | | | agentic |
| qwen3-next-80b-a3b | openrouter | 668ms | 262K | | | | lightweight |
| nemotron-3-super-120b | openrouter | 736ms | 1M | | | | general |
| nemotron-3-ultra-550b | openrouter | 1125ms | 1M | | | | general |
| kimi-k2.6 | openrouter | 1140ms | 262K | ✓ | ✓ | ✓ | coding |
| qwen3-coder | openrouter | 1157ms | 1M | ✓ | | ✓ | coding |
| gemma-4-31b-it | openrouter | 3165ms | 262K | | ✓ | | multimodal |
| glm-4.5-air | openrouter | 3169ms | 131K | ✓ | | | general |
| openrouter/free | openrouter | 3341ms | 200K | | ✓ | | general |
| owl-alpha | openrouter | 5981ms | 1M | ✓ | | | agentic |

## 16 Modelos Descartados

### Por HTTP 404 (no endpoints en OpenRouter)
- `cognitivecomputations/dolphin-mistral-24b-venice-edition`
- `poolside/laguna-m.1`, `poolside/laguna-xs.2`
- `liquid/lfm-2.5-1.2b-instruct`, `liquid/lfm-2.5-1.2b-thinking`
- `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning`
- `nvidia/nemotron-3.5-content-safety`
- `nvidia/nemotron-nano-12b-v2-vl`

### Por HTTP 502 (provider error, recuperable)
- `google/lyria-3-clip-preview`, `google/lyria-3-pro-preview`

### Por HTTP 429 (rate limit Google, recuperable)
- `google/gemini-2.0-flash`, `gemini-2.0-flash-001`
- `google/gemini-2.0-flash-lite`, `gemini-2.0-flash-lite-001`
- `google/gemini-2.5-flash-image`

### Por HTTP 400 (no soporta texto)
- `google/gemini-2.5-flash-preview-tts` (modelo TTS)

### Por capacidad insuficiente (sin tool_calling, text-only)
- `nvidia/nemotron-3-nano-30b-a3b` (ctx 256K pero no tool calling)
- `nvidia/nemotron-nano-9b-v2` (ctx 128K, no tool calling)
- `meta-llama/llama-3.2-3b-instruct` (ctx 131K, no tool calling)
- `qwen/qwen3-next-80b-a3b-instruct` (ctx 262K, no tool calling)
- `nvidia/nemotron-3-super-120b` (ctx 1M, no tool calling)
- `nvidia/nemotron-3-ultra-550b` (ctx 1M, no tool calling)
- `openrouter/free` (ctx 200K, no tool calling)
- `google/gemma-4-26b-a4b-it` (ctx 262K, vision pero no tool calling)
- `google/gemma-4-31b-it` (ctx 262K, vision pero no tool calling)

### Nota importante sobre modelos sin tool_calling
Estos modelos responded correctamente (HTTP 200) pero no tienen capability de tool calling.
Para nuestro objetivo de agente autónomo, no sirven para hilos de ejecución.
Podrían usarse como "procesadores de lenguaje" puros (resumen, traducción, etc.) pero no como workers.

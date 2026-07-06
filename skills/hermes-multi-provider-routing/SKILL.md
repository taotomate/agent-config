---
name: hermes-multi-provider-routing
description: "Configurar Hermes con múltiples proveedores (cloud + local) usando perfiles separados para evitar saturar la PC y garantizar disponibilidad. Incluye lista de modelos gratuitos verificados, pitfalls de delegate_task y estrategia de fallback validada."
version: 2.0.0
author: OWL
model_tier: medium
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [hermes, multi-provider, ollama, openrouter, profiles, fallback, delegation]
---

## Execution Phases


**DRY-RUN RULE:** Before executing any destructive or external operation, first perform a dry-run to preview what will happen. Show the user what actions would be taken, then ask for confirmation before proceeding.
### 1. Preparation Phase
- Load references and verify prerequisites
- Resolve target scope

### 2. Action Phase
- Execute the main workflow (original content below preserves existing steps)

### 3. Verification Phase
- Verify output matches expected results

## Context & Triggers
**When to use this skill:**
- Triggers: "hermes-multi-provider-routing", "use hermes-multi-provider-routing"


# Hermes Multi-Provider Routing

Configurar Hermes para que use modelos cloud (OpenRouter) y locales (Ollama) de forma inteligente, sin saturar la PC.


## User Communication Preferences (Manu)

- **Directo y concreto** — no irse por las ramas, no explicar de más
- **Formato**: bullets y clave:valor, NUNCA tablas pipe (|)
- **Acción inmediata** — cuando pide algo, ejecutar, no planificar eternamente
- **Idioma**: siempre español
- **Proyectos**: separados por categoría, no por cronología
- **Identidad**: el agente es OWL, Hermes es el harness, el modelo es el motor

## Concepto clave: OWL vs Hermes

- **OWL** = el agente (nombre fijo, NO cambia con el modelo LLM). Identificación: "Hola, soy OWL. Corro sobre {modelo}."
- **Hermes** = el harness/sistema completo (gateway, workspace, skills, session DB, etc.)
- **Modelo** = el motor LLM que corra en cada momento
- Cuando hable del harness: "Hermes" a secas. Si hay ambigüedad: "el gateway", "el workspace", etc.

## Concepto key: Multi-provider

- **Perfil principal** (default): modelo cloud gratuito para chat general
- **Perfil local** (ollama): modelo local para tareas pesadas de código
- **Nunca correr 2+ modelos locales en paralelo** → se satura la RAM
- **Los modelos gratuitos tienen rate limits agresivos** → no confiar como único fallback

## Configuración del perfil Ollama

```bash
# 1. Crear perfil
hermes profile create ollama

# 2. Configurar modelo local
hermes -p ollama config set model.base_url "http://localhost:11434/v1"
hermes -p ollama config set model.default "qwen3.6:latest"
hermes -p ollama config set model.provider "ollama"
hermes -p ollama config set model.api_key "ollama-local"
```

## Usar el perfil Ollama para tareas de código

```bash
hermes -p ollama chat -q "Escribe una función Python que..."
hermes -p ollama chat -q "Revisa este código y sugiere mejoras" < archivo.py
```

## Delegación de subagentes

**IMPORTANTE:** `delegate_task` NO respeta `delegation.config` del config.yaml. Siempre usa el modelo del perfil activo.

Para delegar a un modelo específico, usar `hermes chat -q` directamente:

```bash
hermes -p ollama chat -q "Tarea de código compleja" &
```

---

## Base de Datos de Modelos (Multi-Proveedor)

**Path**: `D:\Engram_SDD\Proj-youtube-scraper-v2\openrouter_models.db`
**Esquema**: tabla `models` con 37 columnas (capabilities, health tracking, provider, pricing)
**Total**: 39 modelos (27 OpenRouter + 8 Google Gemini + 2 Groq + 2 DeepSeek)
**Activos verificados**: 21 de 37 free pasaron health check

### Esquema completo (FASE 1 completada)

```sql
CREATE TABLE models (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    provider TEXT NOT NULL DEFAULT 'openrouter',
    context_length INTEGER,
    max_output_tokens TEXT,
    input_modalities TEXT,
    output_modalities TEXT,
    supports_tool_calling INTEGER DEFAULT 0,
    supports_vision INTEGER DEFAULT 0,
    supports_reasoning INTEGER DEFAULT 0,
    supports_code INTEGER DEFAULT 0,
    supports_multilingual INTEGER DEFAULT 0,
    supports_streaming INTEGER DEFAULT 1,
    requests_per_minute TEXT,
    tokens_per_minute TEXT,
    latency_tier TEXT,
    prompt_price TEXT,
    completion_price TEXT,
    is_free INTEGER DEFAULT 1,
    description TEXT,
    category TEXT,
    notes TEXT,
    created TEXT,
    last_updated TEXT,
    last_tested TEXT,
    is_active INTEGER DEFAULT 1,
    test_status TEXT DEFAULT 'untested',
    test_latency_ms INTEGER,
    fail_count INTEGER DEFAULT 0,
    consecutive_fails INTEGER DEFAULT 0,
    last_error TEXT,
    last_success TEXT,
    times_used INTEGER DEFAULT 0,
    times_failed INTEGER DEFAULT 0,
    provider_model_id TEXT,
    endpoint_url TEXT,
    raw_json TEXT
);
```

### Migración completada (2026-06-08)

- Script SQL: `D:\Engram_SDD\Proj-youtube-scraper-v2\db_migration_models.sql`
- Se migraron los 27 modelos OpenRouter existentes al nuevo esquema
- Se poblamon con modelos de Groq (2), Google Gemini (8), DeepSeek (2)
- Health check script: `D:\Engram_SDD\Proj-youtube-scraper-v2\health_check.py`
- Populate script: `D:\Engram_SDD\Proj-youtube-scraper-v2\populate_models.py`

### Índices creados

```sql
CREATE INDEX idx_models_provider ON models(provider);
CREATE INDEX idx_models_is_free ON models(is_free);
CREATE INDEX idx_models_is_active ON models(is_active);
CREATE INDEX idx_models_category ON models(category);
CREATE INDEX idx_models_test_status ON models(test_status);
CREATE INDEX idx_models_latency_tier ON models(latency_tier);
```

---

## Health Check Results (2026-06-08)

**Script**: `D:\Engram_SDD\Proj-youtube-scraper-v2\health_check.py`
**Método**: POST a `/chat/completions` con prompt "Reply with exactly: OK", max_tokens=5, timeout 15s
**Resultado**: 21 passed / 16 failed de 37 modelos free testeados

### Modelos ACTIVOS verificados (por latencia)

| Modelo | Provider | Latencia | Contexto | Notas |
|--------|----------|----------|---------|-------|
| llama-3.1-8b-instant | groq | 118ms | 131K | Más rápido |
| llama-3.3-70b-versatile | groq | 132ms | 131K | Sólido |
| nemotron-3-nano-30b-a3b | openrouter | 335ms | 256K | |
| llama-3.3-70b-instruct | openrouter | 339ms | 131K | |
| hermes-3-llama-3.1-405b | openrouter | 341ms | 131K | |
| gemma-4-26b-a4b-it | openrouter | 350ms | 262K | Multimodal (img+txt+vid) |
| nemotron-nano-9b-v2 | openrouter | 357ms | 128K | |
| llama-3.2-3b-instruct | openrouter | 398ms | 131K | Ligero |
| gpt-oss-20b | openrouter | 456ms | 131K | OpenAI |
| gemini-2.5-flash | google | 477ms | 1M | Principal Google |
| gemini-2.5-flash-lite | google | 587ms | 1M | |
| gpt-oss-120b | openrouter | 607ms | 131K | OpenAI |
| qwen3-next-80b-a3b | openrouter | 668ms | 262K | |
| nemotron-3-super-120b | openrouter | 736ms | 1M | |
| nemotron-3-ultra-550b | openrouter | 1125ms | 1M | Pesado |
| kimi-k2.6 | openrouter | 1140ms | 262K | Coding + multimodal |
| qwen3-coder | openrouter | 1157ms | 1M | Mejor para código |
| gemma-4-31b-it | openrouter | 3165ms | 262K | Multimodal (img+txt+vid) |
| glm-4.5-air | openrouter | 3169ms | 131K | |
| openrouter/free | openrouter | 3341ms | 200K | Router automático free |
| owl-alpha | openrouter | 5981ms | 1M | Actual principal |

### Modelos FALIDOS (no usar)

**OpenRouter (no endpoints)**:
- `cognitivecomputations/dolphin-mistral-24b-venice-edition` — 404 no endpoints
- `poolside/laguna-m.1` — 404 no endpoints
- `poolside/laguna-xs.2` — 404 no endpoints
- `liquid/lfm-2.5-1.2b-instruct` — 404 no endpoints
- `liquid/lfm-2.5-1.2b-thinking` — 404 no endpoints
- `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning` — 404 no endpoints
- `nvidia/nemotron-3.5-content-safety` — 404 no endpoints
- `nvidia/nemotron-nano-12b-v2-vl` — 404 no endpoints
- `google/lyria-3-clip-preview` — 502 provider error
- `google/lyria-3-pro-preview` — 502 provider error

**Google (rate limit 429 — quota excedida)**:
- `gemini-2.0-flash` — 429 quota exceeded
- `gemini-2.0-flash-001` — 429 quota exceeded
- `gemini-2.0-flash-lite` — 429 quota exceeded
- `gemini-2.0-flash-lite-001` — 429 quota exceeded
- `gemini-2.5-flash-image` — 429 quota exceeded
- `gemini-2.5-flash-preview-tts` — 400 (no soporta text-to-text)

**Nota**: Los modelos de Google fallaron por quota excedida, no porque estén caídos. Volver a testear cuando Manu renueve créditos.

### Groq context_length fix

La API de Groq NO devuelve `context_length` (retorna 0). Valores correctos hardcodeados:
- `llama-3.1-8b-instant`: 131072
- `llama-3.3-70b-versatile`: 131072

---

## API Keys — Ubicación

**Archivo principal**: `C:\Users\user\.gemini\antigravity\secrets.env`
**Keys disponibles**:
- `GROQ_API_KEY_ANTIGRAVITY_MAA` — Groq ✅
- `GOOGLE_AI_STUDIO_KEY` — Google Gemini ✅
- `DEEPSEEK_API_KEY` — DeepSeek ⚠️ sin saldo
- `OPENROUTER_API_KEY` — OpenRouter ✅
- `TELEGRAM_BOT_TOKEN` — Telegram ✅
- `LM_STUDIO_API_KEY` + `LM_STUDIO_BASE_URL` — LM Studio ✅

**Keys en `.env` de Hermes** (`D:\Engram_SDD\Hermes-Nous\hermes-data\.env`):
- Solo OpenRouter, Telegram, Anthropic, HASS
- **NO están** las de Groq, Google, DeepSeek → cargar desde `secrets.env`

**Inventario completo**: `D:\Engram_SDD\Proj-Seguridad\api-inventory.md`
**Script de test**: `D:\Engram_SDD\Proj-Seguridad\test_keys.py` (usa `dotenv` para cargar secrets.env)

---

## Fallback Strategy

1. **Principal:** owl-alpha (OpenRouter) — chat general
2. **Si owl falla:** usar perfil ollama (`hermes -p ollama chat -q`)
3. **Si Ollama no está corriendo:** modelos gratuitos online (con rate limit)
4. **Último recurso:** modelos locales uno por vez en serie

## Estrategia recomendada (validada 2026-06-08)

| Prioridad | Modelo | Contexto | Uso |
|-----------|--------|----------|-----|
| 1 | owl-alpha | 1M | Principal, chat general |
| 2 | llama-3.3-70b-versatile (Groq) | 131K | Rápido, general |
| 3 | gemini-2.5-flash | 1M | Google, rate limit bajo |
| 4 | qwen3-coder | 1M | Código |
| 5 | kimi-k2.6 | 262K | Coding + multimodal |
| 6 | hermes-3-405b | 131K | General |
| Perfil Ollama | qwen3.6:latest | varies | Tareas pesadas de código |

**CUIDADO:** `openrouter/meta-llama/llama-3.3-70b-instruct:free` NO es ID válido. Correcto: `meta-llama/llama-3.3-70b-instruct:free` (sin prefijo `openrouter/`).

---

## Pitfalls conocidos

- `delegate_task` ignora `delegation.config` del config.yaml → usar perfiles separados con `hermes -p ollama chat -q`
- `delegate_task` intenta usar IDs inválidos con prefijo `openrouter/` — los IDs correctos NO llevan prefijo
- Modelos `:free` de OpenRouter se rate-liman fácilmente (429 al primer uso)
- El fallback SOLO salta si OpenRouter como servicio entero cae — no si un modelo individual crashea
- No correr 2-3 modelos locales en paralelo → se satura la RAM
- Groq API NO devuelve `context_length` → hay que hardcodearlo
- Google Gemini tiene quota muy baja en tier free → los 2.0-flash全盘 429
- `hermes config set` serializa listas como strings rotos → usar Python yaml.dump
- Perfiles creados con `hermes profile create` heredan skills del default pero tienen config.yaml propio
- **Workspace Web UI hereda model config del gateway** — arreglar config.yaml y `hermes gateway restart`
- Varios modelos listados como "free" en OpenRouter NO tienen endpoints funcionales (404) — verificar con health check

---

## Config YAML Pitfalls (fix patterns)

### `hermes config set` serializa listas como strings — ROTO

Los campos `fallback_providers`, `model.fallbacks`, y las entradas dentro de `providers.*` DEBEN ser listas/dicts YAML reales.

**Sintoma:** los fallbacks no se ejecutan; Ollama no aparece en `/provider`.

**Fix con Python yaml.dump:**

```python
import yaml
path = r'D:\Engram_SDD\Hermes-Nous\hermes-data\config.yaml'
with open(path, 'r') as f:
    cfg = yaml.safe_load(f)

cfg['fallback_providers'] = [
    {"provider": "openrouter", "model": "meta-llama/llama-3.3-70b-instruct:free"},
    {"provider": "ollama", "model": "qwen3.6:latest", "base_url": "http://localhost:11434/v1"},
]

cfg['model']['fallbacks'] = [
    {"provider": "openrouter", "model": "meta-llama/llama-3.3-70b-instruct:free"},
    {"provider": "ollama", "model": "qwen3.6:latest", "base_url": "http://localhost:11434/v1"},
    {"provider": "ollama", "model": "mistral-nemo-12b:latest", "base_url": "http://localhost:11434/v1"},
    {"provider": "ollama", "model": "gemma4:latest", "base_url": "http://localhost:11434/v1"},
]

cfg['providers']['ollama'] = {
    "name": "Ollama",
    "base_url": "http://localhost:11434/v1",
    "api_key": "ollama-local",
    "api_mode": "chat_completions",
}

with open(path, 'w') as f:
    yaml.dump(cfg, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

# Después: hermes gateway restart
```

### Ollama no aparece en el picker `/model` o `/provider`

```python
cfg['custom_providers'] = cfg.get('custom_providers', [])
ollama_exists = any(
    isinstance(e, dict) and '11434' in str(e.get('base_url', ''))
    for e in cfg['custom_providers']
)
if not ollama_exists:
    cfg['custom_providers'].append({
        "name": "Ollama",
        "base_url": "http://localhost:11434/v1",
        "api_key": "ollama-local",
        "model": "qwen3.6:latest",
    })
```

### Verificar que los fallbacks son listas reales

```python
import yaml
with open(path, 'r') as f:
    cfg = yaml.safe_load(f)
print(type(cfg['fallback_providers']))  # debe ser <class 'list'>, NO <class 'str'>
print(type(cfg['model']['fallbacks']))
print(type(cfg['providers']['ollama']))
```

---

## Multi-Modelo por Hilo de Conversación (objetivo Manu)

Manu quiere poder correr diferentes LLMs en diferentes hilos de conversación simultáneamente.

**Arquitectura acordada (2026-06-08)**:
- **OWL (orquestador)** = recibe mensaje → detecta tema → redirige al hilo/modelo correcto
- **OWL NO hace trabajo pesado** = solo coordina, muestra avances, comprime memoria
- **Cada worker responde con línea de identificación**: `[llama-3.3-70b] Respuesta...`
- **Token tracking doble**: el modelo reporta tokens al final de cada respuesta + OWL cuenta independientemente
- **Compresión**: la maneja Hermes nativamente (session compaction) cuando el contexto se llena
- **Dashboard**: Kanban para ver el estado de todos los hilos (arreglar sync del workspace dashboard después)

**Token tracking format** (cada modelo debe reportar al final de su respuesta):
```
TOKENS: P={prompt_tokens} C={completion_tokens} T={total_tokens} | TURNO={n} | ACUM={total_acumulado}
```
Si el modelo no puede calcular tokens exactos: estimar palabras × 1.33, marcar con `~`.
OWL también cuenta independientemente para verificar.

**Perfiles necesarios** (crear con `hermes profile create`):
- `default` → orquestador (owl-alpha) — YA EXISTE
- `ollama` → qwen3.6 — YA EXISTE (parado)
- `chat-general` → llama-3.3-70b-versatile (Groq)
- `chat-fast` → llama-3.1-8b-instant (Groq)
- `coder` → qwen3-coder (OpenRouter)
- `vision` → gemini-2.5-flash (Google)
- `research` → gemini-2.5-flash-lite (Google)

**Modelos descartados por capacidad insuficiente** (no pasan filtro: activo + ctx>=32K + tool_calling):
- 8 modelos con HTTP 404 (no endpoints en OpenRouter): dolphin-mistral, poolside/*, liquid/*, nemotron-3-nano-omni, nemotron-3.5-safety, nemotron-nano-vl
- 5 modelos Google con rate limit 429: gemini-2.0-flash, 2.0-flash-lite, 2.5-flash-image
- 1 modelo TTS no apto: gemini-2.5-flash-preview-tts
- 2 modelos con 502: lyria-3-clip, lyria-3-pro (recuperables)
- Modelos sin tool_calling: nemotron-3-nano, nemotron-nano-9b, llama-3.2-3b, qwen3-next-80b, gemma-4-26b, gemma-4-31b, openrouter/free

**Plan de trabajo (acordado 2026-06-08)**:

| Fase | Descripción | Estado |
|------|-------------|--------|
| FASE 1 | Extender esquema DB + poblar con más proveedores | ✅ COMPLETADO (39 modelos, 37 columnas) |
| FASE 2 | Health checker automático | ✅ COMPLETADO (21/37 activos verificados) |
| FASE 2b | Filtrar por capacidades mínimas | ✅ COMPLETADO (21 aptos, 16 descartados) |
| FASE 3 | Crear perfiles + token tracking + Kanban | 🔴 Pendiente (siguiente) |
| FASE 4 | Poblar metadata real (pricing, límites) | 🔴 Pendiente |
| FASE 5 | Auto-detección de fallos en uso real | 🔴 Pendiente |
| FASE 6 | Router dinámico por hilo | 🔴 Pendiente |
| FASE 7 | Arreglar sync del workspace dashboard | 🔴 Pendiente |

**Faltantes identificados**:
- Context_length de Groq (hardcodear: ambos 131072)
- Pricing real de OpenRouter (el endpoint `/models` lo tiene)
- Límites de rate limit por proveedor
- Verificar si Google Gemini recupera cuota en siguiente health check

---

## References

- [hermes-multi-provider-routing\references\hermes-multi-provider-routing\references\hermes-multi-provider-routing\references\openrouter-models-db.md](references/openrouter-models-db.md) — esquema DB, ejemplos de registros, scripts
- [hermes-multi-provider-routing\references\hermes-multi-provider-routing\references\hermes-multi-provider-routing\references\health-check-results-20260608.md](references/health-check-results-20260608.md) — resultados del primer health check completo
- [hermes-multi-provider-routing\references\hermes-multi-provider-routing\references\hermes-multi-provider-routing\references\openrouter-free-models.md](references/openrouter-free-models.md) — lista de modelos gratuitos, IDs inválidos conocidos
- [hermes-multi-provider-routing\references\hermes-multi-provider-routing\references\hermes-multi-provider-routing\references\config-yaml-pitfalls.md](references/config-yaml-pitfalls.md) — bugs de serialización YAML y resolución de providers
- [hermes-multi-provider-routing\references\hermes-multi-provider-routing\references\hermes-multi-provider-routing\references\telegram-commands.md](references/telegram-commands.md) — referencia rápida de comandos de Telegram


## Guardrails (Critical Rules)
- **NEVER** execute destructive operations without explicit user confirmation
- **ALWAYS** verify target exists before operating
- **ALWAYS** handle errors gracefully — skip with warning, don't crash


# OpenRouter Models DB — Esquema y Plan de Trabajo

## DB Actual

**Path**: `D:\Engram_SDD\Proj-youtube-scraper-v2\openrouter_models.db`
**Tabla**: `models`
**Registros**: 39 modelos (27 OpenRouter + 8 Google Gemini + 2 Groq + 2 DeepSeek)
**Activos verificados**: 21 de 37 free

## Esquema (FASE 1 COMPLETADO)

37 columnas organizadas en grupos:

- **Identificación**: id, name, provider, provider_model_id
- **Capacidades**: context_length, max_output_tokens, input_modalities, output_modalities, supports_tool_calling, supports_vision, supports_reasoning, supports_code, supports_multilingual, supports_streaming
- **Performance**: requests_per_minute, tokens_per_minute, latency_tier
- **Costo**: prompt_price, completion_price, is_free
- **Metadata**: description, category, notes, created, last_updated
- **Health**: last_tested, is_active, test_status, test_latency_ms, fail_count, consecutive_fails, last_error, last_success
- **Uso**: times_used, times_failed
- **Proveedor**: endpoint_url, raw_json

## Scripts

| Script | Path | Propósito |
|--------|------|-----------|
| Migración SQL | `db_migration_models.sql` | Crea esquema expandido, migra datos, crea índices |
| Populate | `populate_models.py` | Pobla con modelos de Groq, Google, DeepSeek vía API |
| Health check | `health_check.py` | Testea todos los modelos free, registra latencia y status |

## Fases del proyecto

| Fase | Descripción | Estado |
|------|-------------|--------|
| FASE 1 | Extender esquema DB + poblar con más proveedores | ✅ COMPLETADO |
| FASE 2 | Health checker automático | ✅ COMPLETADO |
| FASE 3 | Poblar metadata real (pricing, límites) | 🔴 Pendiente |
| FASE 4 | Auto-detección de fallos en uso real | 🔴 Pendiente |
| FASE 5 | Router dinámico por hilo | 🔴 Pendiente |

## Consultas útiles

```python
import sqlite3
conn = sqlite3.connect(r'D:\Engram_SDD\Proj-youtube-scraper-v2\openrouter_models.db')

# Modelos activos por proveedor
SELECT provider, COUNT(*) FROM models WHERE is_active=1 AND is_free=1 GROUP BY provider;

# Modelos más rápidos
SELECT id, test_latency_ms, context_length FROM models WHERE is_active=1 ORDER BY test_latency_ms;

# Modelos con tool calling
SELECT id, provider, test_latency_ms FROM models WHERE supports_tool_calling=1 AND is_active=1;
```

## Notas

- La DB vive en el proyecto del YouTube Scraper v2 por conveniencia, pero es un proyecto independiente
- Groq API NO devuelve context_length → hardcodear manualmente
- Google Gemini tiene quota muy baja en tier free → la mayoría fallan con 429
- Varios modelos OpenRouter listados como "free" NO tienen endpoints funcionales (404)
- Para ejecutar scripts: `cd D:\Engram_SDD\Proj-youtube-scraper-v2 && python <script>.py`

# Config YAML Pitfalls — Hermes Windows

Detalle tecnico de los bugs de serializacion YAML encontrados el 2026-06-02.

## Problema 1: `hermes config set` serializa listas como strings

### Campos afectados

- `fallback_providers` — debe ser lista de dicts `[{provider, model, base_url}]`
- `model.fallbacks` — igual que arriba
- `custom_providers` — debe ser lista de dicts
- `providers.*` (cada entry) — debe ser dict, no string JSON

### Por que pasa

`hermes config set KEY VAL` usa un serializador interno que convierte listas Python a strings escapados. Ejemplo:

```yaml
# Lo que ESCRIBE hermes config set (ROTO):
fallback_providers: '[{"provider":"ollama","model":"qwen3.6:latest"}]'

# Lo que Hermes NECESITA:
fallback_providers:
  - provider: ollama
    model: qwen3.6:latest
```

Cuando Hermes lee el string, `yaml.safe_load()` lo parsea como un string, no como una lista. El codigo que verifica `isinstance(cfg['fallback_providers'], list)` falla silenciosamente.

### Funciones afectadas

- `hermes_cli.config.get_compatible_custom_providers()` — ignora entries que no sean dict
- `hermes_cli.main._named_custom_provider_map()` — ignora `providers.*` que no sean dict
- `hermes_cli.inventory.load_picker_context()` — `user_providers` debe ser dict
- `list_authenticated_providers()` — no incluye providers mal formateados

### Fix

Siempre usar Python `yaml.dump` para escribir estos campos:

```python
import yaml
path = r'D:\Engram_SDD\Hermes-Nous\hermes-data\config.yaml'
with open(path, 'r') as f:
    cfg = yaml.safe_load(f)

# Verificar tipos
assert isinstance(cfg['fallback_providers'], list), "fallback_providers es string, no lista"
assert isinstance(cfg['model']['fallbacks'], list), "model.fallbacks es string, no lista"
assert isinstance(cfg['providers'].get('ollama'), dict), "providers.ollama es string, no dict"

# Si alguno falla, reasignar con tipos correctos y reescribir
with open(path, 'w') as f:
    yaml.dump(cfg, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
```

## Problema 2: Ollama no aparece en el picker `/model`

### Causa raiz

Ollama local (`provider: ollama`) se resuelve internamente a `custom` via `_PROVIDER_ALIASES`:
```python
# hermes_cli/models.py linea 1138
"ollama": "custom",  # bare "ollama" = local; use "ollama-cloud" for cloud
```

El picker `/model` muestra:
1. `CANONICAL_PROVIDERS` (lista hardcoded — NO incluye `ollama`, solo `ollama-cloud`)
2. `custom_providers` de config.yaml (los que agrego el usuario)
3. `providers` de config.yaml (si son dicts validos)

Si `providers.ollama` es un string, `_named_custom_provider_map` lo ignora (`isinstance(raw_entry, dict)` falla).
Si `custom_providers` no tiene entrada para Ollama, no aparece en el picker.

### Solucion completa (3 partes)

```python
# 1. providers.ollama como dict
cfg['providers']['ollama'] = {
    "name": "Ollama",
    "base_url": "http://localhost:11434/v1",
    "api_key": "ollama-local",
    "api_mode": "chat_completions",
}

# 2. custom_providers con entrada Ollama
if 'custom_providers' not in cfg or not isinstance(cfg['custom_providers'], list):
    cfg['custom_providers'] = []
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

# 3. fallback_providers como lista real
cfg['fallback_providers'] = [
    {"provider": "ollama", "model": "qwen3.6:latest", "base_url": "http://localhost:11434/v1"},
    {"provider": "ollama", "model": "mistral-nemo-12b:latest", "base_url": "http://localhost:11434/v1"},
    {"provider": "ollama", "model": "gemma4:latest", "base_url": "http://localhost:11434/v1"},
    {"provider": "ollama", "model": "llama3-8b:latest", "base_url": "http://localhost:11434/v1"},
]
```

Despues de escribir, reiniciar gateway para que tome la config nueva.

## Problema 3: Fallback no salta cuando OpenRouter se queda sin creditos

### Comportamiento de Hermes

El fallback automático (`fallback_providers`) solo se activa cuando el proveedor principal es inalcanzable (error de red, 401, 403, timeout). Si OpenRouter devuelve un error de credits (ej. 402 Payment Required) como respuesta valida de la API, Hermes NO salta al fallback — muestra el error al usuario.

Los fallbacks funcionan en serie: si el primero falla, prueba el segundo, etc.

### Orden recomendado para fallbacks Ollama

qwen3.6 (mejor modelo) > mistral-nemo-12b > gemma4 > llama3-8b > hermes3-8b

En `fallback_providers` (todos los disponibles) y `model.fallbacks` (solo los 3 mejores).

## Verificacion rapida

```python
import yaml
path = r'D:\Engram_SDD\Hermes-Nous\hermes-data\config.yaml'
with open(path, 'r') as f:
    cfg = yaml.safe_load(f)

checks = {
    'fallback_providers is list': isinstance(cfg.get('fallback_providers'), list),
    'model.fallbacks is list': isinstance(cfg.get('model', {}).get('fallbacks'), list),
    'providers.ollama is dict': isinstance(cfg.get('providers', {}).get('ollama'), dict),
    'custom_providers is list': isinstance(cfg.get('custom_providers'), list),
    'model.default': cfg.get('model', {}).get('default', 'NOT SET'),
    'model.provider': cfg.get('model', {}).get('provider', 'NOT SET'),
}
for k, v in checks.items():
    print(f"  {k}: {v}")
```

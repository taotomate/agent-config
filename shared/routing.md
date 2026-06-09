# Routing de herramientas y modelos

## Agente vs Script
- Si la tarea es predecible y repetible → script en `execution/`
- Si la tarea necesita decisión o tiene pasos variables → agente
- Si el script no existe:
  1. Crealo en `execution/nombre_tarea.py`
  2. Creá su `test_nombre_tarea.py`
  3. Verificá que pasa el test antes de ejecutar
- El modelo se usa para generar el script, no para ejecutar la tarea

## Modelos por capa

### L1 — Planificación / Arquitectura
- Principal: Gemini Pro / Opus
- Fallback: Sonnet
- Cuando: diseño, arquitectura, análisis complejo

### L2 — Orquestación / Decisiones
- Principal: Gemini Flash / Sonnet
- Fallback: Haiku
- Cuando: routing de tareas, manejo de errores, coordinación

### L3 — Ejecución
- Principal: script Python en `execution/`
- Fallback: modelos locales (Ollama / LM Studio) o free tier
- Modelos pagos solo si los anteriores no alcanzan

## Cambio de modelo por fallo
Si un modelo genera errores repetidos en un tipo de tarea específico,
consultá `directives/errors_learned.md` para ver el historial
y reasignalo a una capa o tarea donde tenga mejor rendimiento.


<!-- youtube-scraper: processed -->

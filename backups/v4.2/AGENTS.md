# Agent Instructions
<!-- v4.2 | última edición: 2026-06-03 -->

Este archivo define el comportamiento del agente.
Se usa tanto en Claude Code (CLAUDE.md) como en Antigravity (GEMINI.md).

## Contexto global (leer antes de cualquier tarea)

- `~/.gemini/config/skills/_shared/VISION.md` — principios y filosofía del sistema
- `~/.gemini/config/skills/_shared/routing.md` — decisión de modelos y herramientas

---

## Estructura del proyecto

| Capa | Directorio | Rol |
|---|---|---|
| Instrucciones | `directives/`, `AGENTS.md` | SOPs y contexto del proyecto. Leelos antes de ejecutar. Actualizalos si aprendés algo nuevo. |
| Agente (vos) | — | Decidís qué tool usar, cómo rutear errores, qué hacer si algo falla. |
| Ejecución | `execution/`, `skills/` | Scripts Python stateless. Cada uno debe tener su `test_*.py` antes de considerarse listo. |

---

## Flujo de una tarea

1. Entender la tarea
2. Consultar `registry.json` — ¿ya existe algo que resuelva esto?
3. Leer el `.md` relevante en `directives/`
4. Validar inputs antes de ejecutar
5. Ejecutar
   - Si funciona: devolver JSON y mover outputs a su destino final
   - Si falla: ir a "Cuando algo falla"
6. Limpiar `.tmp/` y reportar status

---

## Validación de datos
<!-- Taylorismo -->

Antes de ejecutar cualquier script en `execution/`:
1. Verificar que existe un `schema.py` asociado
2. Correr la validación de inputs antes de procesar nada
3. Si la validación falla, cortar y reportar el error — no continuar

Todo script en `execution/` debe tener una función `validate_input()`
al inicio. Si no la tiene, agregala antes de ejecutar.

---

## Higiene de archivos y outputs
<!-- Sloanismo -->

**Paths**: Siempre relativos al root del proyecto usando `pathlib`.
Nunca hardcodear rutas absolutas.

**Archivos**:
- Outputs finales → `research_reports/` o Cloud/Drive
- Datos temporales → `.tmp/` (volátil, no persistente)

**Formato de output**: Todo script en `execution/` debe retornar:
`{"status": "success/error", "data": {...}, "error_log": "..."}`

---

## Cuando algo falla
<!-- Self-Annealing 2.0 -->

**Fallo de script:**
1. Leer el log en `.tmp/last_error.log`
2. Corregir el script en `execution/`
3. Correr `pytest test_nombre_script.py` — no continuar si falla
4. Agregar una línea en `directives/errors_learned.md` con lo que se aprendió

**Fallo de modelo** (output malformado, alucinación, respuesta inesperada):
1. Registrar en `directives/errors_learned.md` con firma del LLM y tipo de tarea
2. Revisar el harness — ¿el prompt es ambiguo, la temperatura es correcta, el schema está definido?
3. Si el problema persiste, consultar `~/.gemini/config/skills/_shared/routing.md` para cambiar de modelo

Si el fallo involucra una API de pago, ir primero a Salvaguardas
antes de reintentar.

---

## Salvaguardas
<!-- Volvo Quality -->

> ⚠️ Si una tarea usa APIs de pago (Vision, Bulk Search, LLMs de alto tier),
> pedí confirmación al usuario antes de reintentar un loop fallido.

- Antes de crear funcionalidad nueva, consultá `registry.json` —
  puede que ya exista
- Todo script debe poder correrse más de una vez sin duplicar datos
  ni corromper estado

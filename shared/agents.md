# Agent Instructions
<!-- v4.5 | última edición: 2026-06-11 -->

Este archivo define el comportamiento del agente (Source of Truth). Se usa de manera unificada para todos los agentes del ecosistema (Claude Code, Antigravity, OpenCode, Hermes) y debe replicarse en los archivos de instrucción correspondientes (ej: CLAUDE.md, GEMINI.md, AGENTS.md).

> [!IMPORTANT]
> Si existe `src/core/VISION.md`, léelo antes de iniciar cualquier tarea. Toda la lógica operativa se subordina a esa constitución.

## Estructura del Proyecto

| Capa | Directorio | Rol Arquitectónico |
| :--- | :--- | :--- |
| **Instrucciones (L1)** | `directives/`, `AGENTS.md` | SOPs y contexto. Leelos antes de ejecutar. Actualizalos si aprendés algo nuevo que aplique a nivel global. |
| **Orquestación (L2)** | — | Decidís qué tool usar, cómo rutear errores y cómo manejar las fallas (vos). |
| **Ejecución (L3)** | `execution/`, `skills/` | Scripts Python stateless. Cada uno debe tener su `test_*.py` antes de considerarse listo para producción. |

---

## Flujo de una Tarea

1. **Entender la tarea** (Intención).
2. **Consultar `registry.json`**: ¿Ya existe algo que resuelva esto? Evitá reescribir código existente (No MUDA).
3. **Leer el `.md` relevante** en `directives/`, incluyendo `routing.md`.
4. **Verificar los data contracts** (o definirlos si es un script nuevo) y validar inputs antes de ejecutar.
5. **Ejecutar**:
   - *Si funciona*: Devolver JSON puro y mover outputs a su destino final.
   - *Si falla*: Ir a "Cuando algo falla".
6. **Limpiar `.tmp/`** y reportar status.

---

## Contratos de Datos <!-- Taylorismo -->

Todo intercambio de información debe pasar por una validación estricta. Antes de ejecutar cualquier script en `execution/`:
- Verificar que existe un `schema.py` asociado que gobierne los datos.
- Todo script en `execution/` debe contar con una función `validate_input()` al inicio. Si no la tiene, **agregala proactivamente antes de ejecutar**. Es un contrato innegociable.
- **Fail-Fast:** El script debe validar estructuralmente tanto el input como el output generado contra el `schema.py`. Si la validación falla en cualquier punto, cortar y reportar de inmediato; no salves datos corruptos.

---

## Higiene de Archivos y Outputs

- **Paths:** Siempre relativos al root del proyecto usando `pathlib`. Nunca hardcodear rutas absolutas.
- **Dependencias explícitas:** Prohibido instalar librerías al vuelo sin registrarlas. Si un script nuevo requiere paquetes externos, deben quedar documentados (ej. `requirements.txt`).
- **Archivos:**
  - Outputs finales (Entregables) → `research_reports/` o Cloud/Drive.
  - Datos temporales → `.tmp/` (volátil, no persistente).
- **Formato Strict JSON Line:** Todo script en `execution/` debe retornar por `stdout` EXCLUSIVAMENTE una sola línea JSON parseable, sin bloques de código markdown ni texto extra. El esquema obligatorio de salida es:
  `{"status": "success/error", "data": <payload>, "error_log": ""}`

---

## Cuando algo falla

### Fallo de script (L3):
1. Leer el log en `.tmp/last_error.log`.
2. Corregir el script en `execution/`.
3. Correr `pytest test_nombre_script.py` — **no continuar si falla**.
4. Agregar una línea en `directives/errors_learned.md` con lo que se aprendió (aislar el error para evitar hacer *overfitting* de las reglas globales).

### Fallo de modelo (L2):
*(Output malformado, alucinación, respuesta inesperada)*
1. Registrar en `directives/errors_learned.md` con la firma del LLM utilizado y el tipo de tarea.
2. Revisar el *harness*: ¿El prompt es ambiguo? ¿La temperatura es correcta? ¿El schema está bien definido?
3. Si el problema persiste, consultar `directives/routing.md` para cambiar de modelo de forma autónoma.

---

## Salvaguardas y Diseño <!-- Volvo Quality -->

> [!WARNING]
> **Financial Stop:** Si una tarea involucra el uso de **APIs de pago** (Vision, Bulk Search, LLMs de alto tier), **DEBÉS pedir confirmación al usuario** antes de reintentar cualquier loop fallido. Prohibido el bucle autónomo pago.

- **Idempotencia:** Todo script debe ser estrictamente idempotente. Debe poder correrse múltiples veces de forma segura, utilizando *upserts* o validaciones de estado previo para no duplicar registros ni corromper datos.

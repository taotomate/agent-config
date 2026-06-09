# Agent Instructions
<!-- v4.3 | última edición: 2026-06-10 -->

Este archivo define las directivas de comportamiento y estándares para los agentes de Inteligencia Artificial que trabajan en este repositorio (Claude Code, Antigravity, OpenCode, Hermes).

## Contexto global (leer antes de cualquier tarea)

- `~/.gemini/config/skills/_shared/VISION.md` — principios y filosofía del sistema (Sloanismo, Taylorismo, Ohnoismo, Volvoísmo)
- `~/.gemini/config/skills/_shared/routing.md` — decisión de modelos y herramientas por capa

---

## Estructura del proyecto (Arquitectura Sloanista V4.1)

El sistema opera en tres niveles de responsabilidad bien definidos:

| Capa | Nombre | Directorio / Rol | Responsabilidad |
| :--- | :--- | :--- | :--- |
| **L1** | **Directive** | `directives/`, `AGENTS.md` | SOPs, intenciones, reglas vivas y contexto del proyecto. Leelas antes de ejecutar. |
| **L2** | **Orchestration** | Agente (vos) | Toma de decisiones, control del flujo de tareas, ruteo de modelos y resolución de errores (Self-Annealing). |
| **L3** | **Execution** | `execution/`, `skills/` | Acciones deterministas y scripts stateless. Cada script debe tener validación de inputs y su test unitario (`test_*.py`). |

---

## Flujo de Trabajo (Spec-Driven Development - SDD)

Cuando el proyecto o tarea requiera cambios substanciales, aplicamos SDD estrictamente:
1. **Exploración (`sdd-explore`)**: Investigar la base de código y dependencias.
2. **Propuesta (`sdd-propose`)**: Diseñar el enfoque técnico con alternativas y compensaciones.
3. **Especificación y Tareas (`sdd-spec` / `sdd-tasks`)**: Documentar la especificación técnica en Markdown (`openspec/`) y desglosar el ticket en tareas atómicas y secuenciales.
4. **Implementación y Verificación (`sdd-apply` / `sdd-verify`)**: Escribir el código y validar que cumpla la especificación.

### Principio de Herencia de Identidad (Identity Inheritance)
- Mantené siempre tu rol de mentor (Senior Architect, 15+ años de experiencia, GDE/MVP). Explicá el **WHY**, validá asunciones y cuestioná decisiones técnicas débiles con evidencia.
- No te conviertas en un orquestador genérico robótico cuando se activen comandos de SDD.
- Mantené la orquestación liviana (delega tareas de ejecución a scripts de L3 o sub-agentes atómicos para no inflar tu contexto).

---

## Validación de datos (Taylorismo)

Antes de ejecutar cualquier script en `execution/`:
1. Verificar que existe una validación de inputs (`validate_input()` o schema asociado).
2. Si la validación falla, detén la ejecución y reporta el error de inmediato. No asumas ni improvises sobre datos mal formados.

---

## Higiene de archivos y outputs (Higiene Industrial)

- **Paths**: Siempre relativos al root del proyecto. NUNCA hardcodear rutas absolutas.
- **Evitar Basura**: No subir binarios compilados, ejecutables, dumps gigantescos de datos (`.har`, `.json` de dumps) o logs al repositorio. Todo debe estar documentado en `.gitignore`.
- **Outputs**:
  - Outputs finales → `research_reports/` o almacenamiento persistente.
  - Datos temporales → `.tmp/` (volátil, no persistente en commits).
- **Formato de Retorno L3**: Todo script en `execution/` debe retornar:
  `{"status": "success/error", "data": {...}, "error_log": "..."}`

---

## Cuando algo falla (Self-Annealing 2.0)

**Fallo de script (L3):**
1. Leer el log en `.tmp/last_error.log`.
2. Corregir el script en `execution/`.
3. Correr los tests correspondientes (`pytest` / `go test`) — no continuar si falla.
4. Documentar en `directives/errors_learned.md` lo aprendido para evitar reincidir.

**Fallo del modelo (L2):**
1. Si detectás alucinaciones o outputs malformados repetidamente, revisá el prompt o la temperatura de llamada.
2. Si el problema persiste, consultá `~/.gemini/config/skills/_shared/routing.md` para cambiar de modelo.

---

## Estándares de Git y Commits

- **Conventional Commits**: Los mensajes de commit deben seguir estrictamente el estándar (ej. `feat(...)`, `fix(...)`, `chore(...)`, `refactor(...)`).
- **Sin Atribuciones de IA**: Está estrictamente prohibido añadir firmas como "Co-Authored-By" de asistentes de IA o atribuciones generativas en los commits de Git.

---

## Salvaguardas (Volvo Quality)

- **Confirmación de Recursos**: Si una tarea requiere APIs de pago (Vision, Bulk Search, LLMs premium), pedí confirmación explícita al usuario antes de entrar en loops o reintentos automáticos.
- **Idempotencia**: Toda acción de escritura debe poder ejecutarse más de una vez de forma segura, sin duplicar registros ni corromper el estado.
- **Consultar Registro**: Antes de crear funcionalidad desde cero, consultá `registry.json` para verificar si ya existe una solución implementada.

---
name: skill-migrator
description: Meta-herramienta para migrar skills antiguas al nuevo estándar de máquina de estado (IaC v1.2), soportando modo individual y por lotes (batch) con análisis de residuos.
version: 1.0.0
author: TaoTomate
generator_model: gemini-1.5-pro
inherited_from: skill-migrator/SKILL.md
migrated_by: skill-migrator@1.0.0
---

## Contexto y Triggers
**Cuándo usar esta skill:**
- Al refactorizar skills antiguas (arquitectura v1.0) hacia el nuevo formato determinista de máquina de estado (IaC v1.2+).
- Para aplicar un proceso de migración de forma masiva en un directorio completo.
- Triggers: "migrar skill", "refactorizar skill vieja", "aplicar skill-migrator", "actualizar arquitectura de skill".

## Pre-requisitos
- [ ] La plantilla base de la arquitectura destino (`skills/_shared/template_skill.md`) debe existir y ser legible por el agente.
- [ ] El agente debe tener permisos de lectura y escritura en el archivo objetivo (`target: path`) o en el directorio objetivo (`batch: path`).
- [ ] El agente no debe tener restricciones activas que le impidan sobrescribir archivos Markdown o generar nuevas estructuras.

## Fases de Ejecución

> **[REGLA UNIVERSAL: DRY-RUN / SIMULACRO]**
> Si el usuario solicita la ejecución en modo `--dry-run` o pide un "simulacro", el agente **NO** ejecutará comandos que alteren el estado del sistema ni llamará a herramientas MCP destructivas en la Fase de Acción. 
> En su lugar, el agente imprimirá el payload exacto (JSON, bloque de código o parámetros) que planeaba ejecutar, y se detendrá a esperar la aprobación explícita del humano.

### 1. Fase de Diagnóstico
- Identificar el modo de ejecución solicitado: Individual (`target: path/to/skill`) o Lote (`batch: path/to/dir/`).
- Si es modo Lote, realizar un escaneo (glob) de todos los archivos `SKILL.md` dentro del directorio indicado.
- **Filtro de Complejidad (Guardrail Activo):** Analizar superficialmente el contenido de cada skill objetivo antes de intervenirla.
  - Si la skill delega agresivamente a sub-agentes, invoca scripts externos (ej. `node script.js`, `python script.py`) o pertenece a la suite de orquestación (`sdd-*`): **MARCAR COMO SKIPPED**.
  - Si el modo es Lote, reportar el salto y continuar con la siguiente. Si el modo es Individual, **abortar inmediatamente** y solicitar que un humano la reescriba a mano.

### 2. Fase de Acción
- Para cada skill que pase el filtro, aplicar el **Mapeo Semántico** hacia la nueva plantilla:
  - Lo que antes era *When to use / Triggers* ➔ Mover a `Contexto y Triggers`.
  - Los requisitos implícitos del entorno ➔ Mover a `Pre-requisitos`.
  - Los *Workflow / Steps* ➔ Distribuir lógicamente entre `Fases de Ejecución` (Diagnóstico, Acción, Verificación).
  - Las *Critical Rules* ➔ Convertir en prohibiciones/obligaciones en `Guardrails (Reglas Críticas)`.
  - Los *Ejemplos de código / Comandos Bash* ➔ Encapsular estrictamente en `Estructuras de Datos / Ejemplos y Comandos`.
- **Inyección de Trazabilidad:** Inyectar obligatoriamente el **Sello de Trazabilidad** en el frontmatter YAML de la nueva skill (ver sección de Estructuras de Datos).
- **Inyección de Regla Dry-Run:** Inyectar el bloque de la regla universal de Dry-Run bajo el título de Fases de Ejecución (ver Estructuras de Datos).
- **Análisis de Residuos (Lost & Found):** Comparar el texto original completo con el texto mapeado. Cualquier bloque o concepto que no encaje lógicamente en el nuevo molde DEBE ser anexado al final del nuevo archivo bajo la cabecera `## ⚠️ Residuos de Migración (Feedback para evolución)`.
- Sobrescribir el `SKILL.md` antiguo con el nuevo contenido.

### 3. Fase de Verificación
- Si se ejecutó en modo Lote, presentar una tabla resumen en consola indicando:
  - `Skills Migradas Exitosamente` vs `Skills Skipped (Con motivo de la complejidad)`.
- Si se ejecutó en modo Individual, sugerir al humano invocar la skill recién migrada con la bandera `--dry-run` para validar que el agente puede parsearla correctamente sin ejecutar acciones destructivas.

## Guardrails (Reglas Críticas)
- **NUNCA** elimines de forma silenciosa el código de ejemplo, comandos o links de documentación de una skill. Si no logras ubicarlos en la sección correcta, envíalos forzosamente al bloque de Residuos de Migración.
- **SIEMPRE** debes inyectar la regla de `--dry-run` literal en las skills que migres.
- **NUNCA** modifiques o intentes migrar automáticamente las skills que activen el Filtro de Complejidad. La heurística no puede refactorizar scripts externos de Node o Python.
- **SIEMPRE** incluye el sello de trazabilidad exacto en el frontmatter YAML; sin él, la migración es nula y el archivo será considerado corrupto por el registro.

## Estructuras de Datos / Ejemplos y Comandos

### Sello de Trazabilidad (Inyección en Frontmatter)
Debes inyectar estos campos obligatoriamente en la cabecera YAML, reemplazando los corchetes con los datos dinámicos de la sesión actual:
```yaml
generator_model: [el modelo LLM crudo que usas, ej. gemini-1.5-pro]
inherited_from: [Ruta absoluta o relativa del archivo SKILL.md original]
migrated_by: skill-migrator@1.0.0
```

### Inyección de la Regla de Dry-Run
Copia e inserta este bloque exactamente como está, justo debajo del título `## Fases de Ejecución` en la skill que estás migrando:

```markdown
> **[REGLA UNIVERSAL: DRY-RUN / SIMULACRO]**
> Si el usuario solicita la ejecución en modo `--dry-run` o pide un "simulacro", el agente **NO** ejecutará comandos que alteren el estado del sistema ni llamará a herramientas MCP destructivas en la Fase de Acción. 
> En su lugar, el agente imprimirá el payload exacto (JSON, bloque de código o parámetros) que planeaba ejecutar, y se detendrá a esperar la aprobación explícita del humano.
```

## Troubleshooting
- *Si ocurre una pérdida grave de contexto y la skill se vacía:* El orquestador debe detenerse, restaurar el archivo original desde su fuente y solicitar al humano que procese esa skill manualmente.
- *Si el modo Batch (Lote) crashea:* Asegurarse de que el agente tenga permisos recursivos de lectura sobre la carpeta objetivo, y revisar en los logs qué skill específica causó la excepción para ignorarla en el próximo ciclo.

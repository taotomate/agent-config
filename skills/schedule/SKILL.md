---
name: schedule
description: 'Migrated skill: schedule'
version: 1.0.0
author: unknown
generator_model: unknown
model_tier: medium
inherited_from: D:\todas-las-skills-llm\skills\schedule\SKILL.md
migrated_by: skill-optimizer@3.2.0
---

## Context & Triggers
**When to use this skill:**
- Triggers: "schedule", "use schedule", "create scheduled task", "update scheduled task", "list scheduled tasks"
- Decidir primero si el usuario quiere **crear una nueva** tarea programada o **modificar una existente**.


## Execution Phases


### 1. Fase de Selección (Nueva o Modificación)
Determinar la intención:
- Si es modificación/pausa/resumen de una tarea existente: saltar a la **Fase 2a**.
- Si es creación de una nueva tarea: saltar a la **Fase 2b**.

### 2a. Actualizar una tarea existente
- Utilizar `list_scheduled_tasks` si se necesita buscar el ID de la tarea (`taskId`).
- Llamar a la herramienta `update_scheduled_task` con el `taskId` correspondiente. (Nota: Si la sesión actual fue lanzada por una tarea programada, el ID de la tarea actual se encuentra en el atributo `name` de la etiqueta `<scheduled-task name="...">` en el encabezado de la conversación).

### 2b. Crear una nueva tarea (Destilar sesión actual)
1. **Analizar la sesión**: Identificar el objetivo principal y destilarlo en un prompt autónomo repetible. El prompt debe ser imperativo y auto-contenido (no hacer referencia a "esta sesión", "lo anterior", etc.).
2. **Elegir taskName**: Nombre descriptivo corto en formato kebab-case (ej. `daily-inbox-summary`).
3. **Definir la programación**: Determinar la fecha/hora única (`fireAt`) o recurrente (`cronExpression`). Proponer una si el usuario no la especificó.
4. **Lanzar la creación**: Llamar a `create_scheduled_task`.

## Guardrails (Critical Rules)
- **NEVER** execute destructive operations without explicit user confirmation
- **ALWAYS** verify target exists before operating
- **ALWAYS** handle errors gracefully — skip with warning, don't crash

## Data Structures / Examples & Commands

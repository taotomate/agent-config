---
name: skill-creator
description: >
  Creates new AI service skills following the Service Skills spec.
  Trigger: When user asks to create a new skill, add service instructions, or document patterns for AI.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, WebFetch, WebSearch, Task
generator_model: gemini-1.5-pro
inherited_from: skill-creator/SKILL.md
migrated_by: skill-migrator@1.0.0
---

## Contexto y Triggers
**Cuándo usar esta skill:**
- Un patrón es utilizado repetidamente y la AI requiere instrucciones explícitas.
- Las convenciones específicas del proyecto difieren de las prácticas generales recomendadas.
- Los flujos de trabajo complejos requieren instrucciones paso a paso.
- Cuando los árboles de decisión pueden ayudar a la AI a elegir el enfoque correcto.

## Pre-requisitos
- [ ] La skill no debe existir ya (verificar en `skills/`).
- [ ] El patrón debe ser reusable, no una tarea ad-hoc o aislada.

## Fases de Ejecución

> **[REGLA UNIVERSAL: DRY-RUN / SIMULACRO]**
> Si el usuario solicita la ejecución en modo `--dry-run` o pide un "simulacro", el agente **NO** ejecutará comandos que alteren el estado del sistema ni llamará a herramientas MCP destructivas en la Fase de Acción. 
> En su lugar, el agente imprimirá el payload exacto (JSON, bloque de código o parámetros) que planeaba ejecutar, y se detendrá a esperar la aprobación explícita del humano.

### 1. Fase de Diagnóstico
- Evaluar si realmente se necesita una skill: Si la documentación ya existe, crear una referencia. Si es trivial, no crear la skill.
- Determinar el nombre siguiendo la nomenclatura (`{technology}`, `{project}-{component}`, `{action}-{target}`).

### 2. Fase de Acción
- Escribir el `SKILL.md` principal usando la plantilla.
- Incluir patrones críticos claros, ejemplos de código mínimos y comandos copy-paste.
- Decidir la ubicación de archivos accesorios: `assets/` para templates o esquemas JSON; `references/` para referencias locales de documentación.

### 3. Fase de Verificación
- Asegurar que el frontmatter está completo (identificador en lowercase, descripción con triggers, versión, autor).
- Agregar la nueva skill al registro `CONSTITUTION.md` usando la tabla de habilidades.

## Guardrails (Reglas Críticas)
- **NUNCA** agregues una sección de "Keywords" (el agente busca en el frontmatter, no en el body).
- **NUNCA** uses URLs web en `references/`, debes usar paths locales exclusivamente.
- **NUNCA** dupliques contenido de documentación ya existente; utiliza enlaces y referencias.
- **SIEMPRE** asegúrate de comenzar con los patrones más críticos y usar tablas para árboles de decisión.

## Estructuras de Datos / Ejemplos y Comandos

### Nomenclatura de Skills
- **Genérica:** `{technology}` (ej. `pytest`, `typescript`)
- **Específica de proyecto:** `{project}-{component}` (ej. `myapp-api`)
- **De flujo de trabajo:** `{action}-{target}` (ej. `skill-creator`, `jira-task`)

### Estructura de Directorios
```text
skills/{skill-name}/
├── SKILL.md              # Obligatorio - archivo principal
├── assets/               # Opcional - templates, schemas
└── references/           # Opcional - links a documentación local
```

### Plantilla Básica SKILL.md
```markdown
---
name: {skill-name}
description: {Qué hace y cuándo invocarlo (triggers)}
version: "1.0.0"
author: {tu-nombre}
---
## Contexto y Triggers
## Pre-requisitos
## Fases de Ejecución
## Guardrails (Reglas Críticas)
## Estructuras de Datos / Ejemplos y Comandos
```

### Registro en CONSTITUTION.md
```markdown
| `{skill-name}` | {Description} | [SKILL.md](skills/{skill-name}/SKILL.md) |
```

## ⚠️ Residuos de Migración (Feedback para evolución)
*(Toda la información ha sido mapeada satisfactoriamente)*

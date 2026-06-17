---
name: skill-registry
description: Crea o actualiza el registro de skills compactas (skill-registry.md) escaneando las skills disponibles e indexando convenciones del proyecto.
version: 1.1.0
author: TaoTomate
generator_model: gemini-1.5-pro
inherited_from: skill-registry/SKILL.md
migrated_by: skill-migrator@1.0.0
---

## Contexto y Triggers
**Cuándo usar esta skill:**
- Después de instalar o eliminar skills en el entorno del usuario o proyecto.
- Al configurar un proyecto nuevo (como parte integrada de `sdd-init`).
- Cuando el humano pida explícitamente "actualizar skills", "update registry" o "skill registry".

## Pre-requisitos
- [ ] El agente orquestador debe tener permisos de lectura en el file system para escanear directorios de configuración globales y locales.
- [ ] Debe existir capacidad para escribir en el directorio raíz del proyecto (`.atl/`).

## Fases de Ejecución

> **[REGLA UNIVERSAL: DRY-RUN / SIMULACRO]**
> Si el usuario solicita la ejecución en modo `--dry-run` o pide un "simulacro", el agente **NO** ejecutará comandos que alteren el estado del sistema ni llamará a herramientas MCP destructivas en la Fase de Acción. 
> En su lugar, el agente imprimirá el payload exacto (JSON, bloque de código o parámetros) que planeaba ejecutar, y se detendrá a esperar la aprobación explícita del humano.

### 1. Fase de Diagnóstico
- Escanear de forma recursiva buscando archivos `SKILL.md` en ubicaciones globales (ej. `~/.gemini/skills/`, `~/.claude/skills/`, `~/.config/opencode/skills/`) y ubicaciones locales del proyecto (ej. `{project-root}/.service/skills/`).
- Escanear la raíz del proyecto buscando archivos de convención (ej. `CONSTITUTION.md`, `CLAUDE.md`, `.cursorrules`).
- Si se encuentra un archivo índice de convenciones (`CONSTITUTION.md`), leerlo para extraer todas las rutas de archivos referenciadas en él.

### 2. Fase de Acción
- Extraer los metadatos de las skills encontradas (`name` y `trigger`) leyendo el frontmatter de cada archivo `SKILL.md`.
- Generar un bloque de **Compact Rules** para cada skill, extrayendo únicamente las restricciones accionables y saltándose el ruido.
- Formatear todo el resultado en tablas Markdown (Ver la sección Estructuras de Datos).

### 3. Fase de Verificación
- Escribir obligatoriamente el resultado compilado en el archivo `{project-root}/.atl/skill-registry.md`.
- Si la herramienta `mem_save` está disponible (Integración MCP de Engram), invocarla para persistir el contenido del registro en memoria persistente usando el `topic_key: "skill-registry"`.
- Mostrar un resumen conciso en consola indicando cuántas skills de usuario y cuántas convenciones de proyecto fueron indexadas.

## Guardrails (Reglas Críticas)
- **SIEMPRE** ignora y salta los directorios `sdd-*`, `_shared` y `skill-registry` durante el escaneo. No contienen "skills de código accionables", sino protocolos meta del orquestador. Inyectarlas gastaría tokens inútilmente.
- **NUNCA** excedas las 15 líneas por cada bloque de "Compact Rules". Deben ser directivas estrictas ("Hacer X", "Nunca Y"), sin tutoriales, explicaciones de motivación, ni ejemplos de código largos.
- **SIEMPRE** escribe el archivo físico `.atl/skill-registry.md`, independientemente de si la persistencia en la base de datos Engram falla, no existe, o está deshabilitada.

## Estructuras de Datos / Ejemplos y Comandos

### Formato Esperado para "Compact Rules"
*Ejemplo para una skill de React 19:*
```markdown
### react-19
- No uses useMemo/useCallback — React Compiler maneja la memoización automáticamente.
- Usa el hook use() para promesas/contexto.
- Server Components por defecto, usa 'use client' solo para hooks de estado/interactividad.
- `ref` ahora es un prop regular, no uses forwardRef.
```

### Formato Final del Archivo `skill-registry.md`
El archivo final generado debe verse así:

```markdown
# Skill Registry
**Uso exclusivo del Delegador.**

## User Skills
| Trigger | Skill | Path |
|---------|-------|------|
| "crear PR" | branch-pr | ~/.gemini/skills/branch-pr/SKILL.md |

## Compact Rules

### branch-pr
- Rule 1
- Rule 2

## Project Conventions
| File | Path | Notes |
|------|------|-------|
| CONSTITUTION.md | /path/to/CONSTITUTION.md | Index |
```

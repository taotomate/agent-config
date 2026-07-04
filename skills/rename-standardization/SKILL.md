---
name: rename-standardization
description: 'Migrated skill: rename-standardization'
version: 1.0.0
author: unknown
generator_model: unknown
model_tier: medium
inherited_from: D:\todas-las-skills-llm\skills\rename-standardization\SKILL.md
migrated_by: skill-optimizer@3.2.0
---

## Context & Triggers
**When to use this skill:**
- Triggers: "rename-standardization", "use rename-standardization", "rename component", "rename file"
- Purpose: Garantizar la integridad de la arquitectura eliminando términos genéricos ("Service", "Manager") y asegurando que cada componente tenga un nombre que describa su **Función Computacional** exacta.


## Execution Phases


### 1. Fase de Auditoría (Pre-Rename)
Antes de realizar cualquier cambio:
- **Grep Exhaustivo**: Buscar todas las ocurrencias exactas y difusas del nombre antiguo (`OldName`) en `src/`, `tests/`, y `openspec/`.
- **Mapeo de Dependencias**: Listar todos los archivos que importan el componente.
- **Justificación Técnica**: El agente DEBE escribir una breve nota explicando por qué el nuevo nombre (`NewName`) es superior y más preciso (ej: "Se cambia `ReportGenerator` a `DossierProducer` porque su salida es un documento estructurado de conocimiento, no un simple reporte de datos").

### 2. Fase de Ejecución (Atómica)
- **Cambio de Archivo**: Renombrar el archivo físico (usar `ren` o `mv`).
- **Actualización de Código**: Corregir la definición de la clase/función y todos los imports en un solo batch.
- **Actualización de Artefactos**: Sincronizar `specs.md`, `design.md` y `task.md` de la feature relacionada.

### 3. Fase de Limpieza (Post-Rename)
- **Búsqueda de "Zombies"**: Correr un grep final por el `OldName`. El resultado DEBE ser cero en el código fuente.
- **Sincronización de Memoria**: Llamar a `mem_save` con tipo `decision` o `architecture` para registrar el cambio y su justificación.

## Guardrails (Critical Rules)
- **PROHIBIDO**: Usar `Service`, `Manager`, `Controller`, `Helper`, `Utility` en los nombres de los componentes.
- **NEVER** execute destructive operations without explicit user confirmation
- **ALWAYS** verify target exists before operating
- **ALWAYS** handle errors gracefully — skip with warning, don't crash

## Data Structures / Examples & Commands

### Ontología de Nombres (Gentleman Standards)

| Categoría | Sufijo / Patrón | Responsabilidad |
| :--- | :--- | :--- |
| **Pipeline** | `*Pipeline` | Flujo lineal de datos entre múltiples etapas. |
| **Engine** | `*Engine` | Lógica de dominio pura y pesada (ej. `ClassificationEngine`). |
| **Extractor** | `*Extractor` | Especialista en sacar datos de fuentes crudas (ej. `TranscriptExtractor`). |
| **Orchestrator** | `*Orchestrator` | Coordina otros componentes para cumplir un objetivo de alto nivel. |
| **Dispatcher** | `*Dispatcher` | Encargado de la salida de datos o persistencia (IO). |
| **Tool** | `*Tool` | Funcionalidad atómica delegable (ej. `GrepTool`). |



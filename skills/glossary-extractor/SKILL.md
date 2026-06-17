---
name: glossary-extractor
description: Proceso especializado para la extracción técnica de vocabulario, jerga de arquitectura y conceptos metodológicos. Genera archivos MOC para Obsidian.
version: 1.0.0
author: TaoTomate
generator_model: gemini-1.5-pro
inherited_from: glossary-extractor/SKILL.md
migrated_by: skill-migrator@1.0.0
---

## Contexto y Triggers
**Cuándo usar esta skill:**
- Invocación a pedido o cuando se discuten conceptos metodológicos y técnicos de arquitectura.
- Al generar archivos MOC (Map of Content) para Obsidian con metadata JSON oculta.

## Pre-requisitos
- [ ] Debe existir la ruta de destino: `D:\Voveda\20_Atlas\21_MOCs`.

## Fases de Ejecución

> **[REGLA UNIVERSAL: DRY-RUN / SIMULACRO]**
> Si el usuario solicita la ejecución en modo `--dry-run` o pide un "simulacro", el agente **NO** ejecutará comandos que alteren el estado del sistema ni llamará a herramientas MCP destructivas en la Fase de Acción. 
> En su lugar, el agente imprimirá el payload exacto (JSON, bloque de código o parámetros) que planeaba ejecutar, y se detendrá a esperar la aprobación explícita del humano.

### 1. Fase de Diagnóstico
- Aplicar estrategia de MAXIMUM RECALL: Identificar herramientas de infraestructura (API, librerías, ej. TypeScript, Obsidian API), metodología (patrones como MOC, Atomic Notes) y teoría subyacente.
- Si hay dudas sobre la simplicidad de un término, **INCLUIRLO**. La densidad de recuerdo tiene prioridad.
- Unificación de Alias: Verificar si términos distintos significan lo mismo para consolidarlos usando el campo `aliases`.

### 2. Fase de Acción
- Generar el contenido del glosario en Markdown siguiendo el esquema Zettelkasten MOC.
- El cuerpo (BODY) debe contener una lista de `[[Term Name]]`: Definición breve.
- Incrustar el bloque JSON oculto al final del archivo para el procesamiento automatizado.

### 3. Fase de Verificación
- Guardar el archivo en `D:\Voveda\20_Atlas\21_MOCs` con la nomenclatura correcta: `Glossary_[Project/Topic]_[YYYY-MM-DD]_[HHMM].md`.

## Guardrails (Reglas Críticas)
- **NO** infantilizar las definiciones, mantener siempre un alto rigor técnico.
- **NO** ignorar términos "simples" de infraestructura (ej. nombres de APIs o lenguajes base).
- **SIEMPRE** usar la marca de tiempo HHMM en el nombre de archivo para evitar colisiones.
- **NUNCA** alterar las llaves "title", "content" o "aliases" del bloque JSON estructurado.

## Estructuras de Datos / Ejemplos y Comandos

### Estructura JSON Oculta para Obsidian
El archivo generado debe finalizar con este bloque oculto (envuelto en comentarios de Obsidian `%%`):

```html
%%
JSON_GLOSSARY_START
[
  {
    "title": "Term Name",
    "content": "Dense, technical, and precise definition (no infantilization).",
    "aliases": ["synonym1", "synonym2"],
    "tags": ["#architecture", "#workflow"]
  }
]
JSON_GLOSSARY_END
%%
```

## ⚠️ Residuos de Migración (Feedback para evolución)
*(Toda la información ha sido mapeada satisfactoriamente)*

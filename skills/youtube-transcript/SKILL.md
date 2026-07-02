---
model_tier: inherited
name: youtube-transcript
description: >
  Capacidad para extraer transcripciones de videos de YouTube usando Playwright.
  Ideal para alimentar el Zettelkasten o procesar contenido de video.
  Trigger: "extraer transcripción", "bajar subtítulos youtube", "youtube transcript".
---

## Execution Phases



**DRY-RUN RULE:** Before executing any destructive or external operation, first perform a dry-run to preview what will happen. Show the user what actions would be taken, then ask for confirmation before proceeding.
> **[UNIVERSAL DRY-RUN / SIMULATION RULE]**
> If the user requests execution in `--dry-run` mode or asks for a "simulation", the agent will **NOT** execute commands that alter system state or call destructive MCP tools in the Action Phase.
> Instead, the agent will print the exact payload (JSON, code block, or parameters) it planned to execute, and will wait for explicit human approval.
### 1. Preparation Phase
- Load references and verify prerequisites
- Resolve target scope

### 2. Action Phase
- Execute the main workflow (original content below preserves existing steps)

### 3. Verification Phase
- Verify output matches expected results

## Context & Triggers
**When to use this skill:**
- TODO: Add specific triggers for this skill
- Triggers: "youtube-transcript", "use youtube-transcript"




## Prerequisites
- [ ] Read access to target files/directories
- [ ] Write access for auto-fix operations


## Propósito

Esta skill permite al agente automatizar la extracción de transcripciones de YouTube de forma robusta, manejando la carga dinámica de la interfaz.

## Flujo de Trabajo (Patterns)

### 1. Extracción de Transcripción
Para obtener la transcripción de un video, el agente debe seguir estos pasos en Playwright:
1. Navegar a la URL del video.
2. Hacer click en `#expand` para abrir la descripción.
3. Buscar y clickear el botón `ytd-video-description-transcript-section-renderer button` ("Mostrar transcripción").
4. Esperar a que el panel `ytd-transcript-renderer` sea visible.
5. Scrapear los segmentos usando `ytd-transcript-segment-renderer` o `macro-markers-panel-item-view-model`.

### 2. Estándar de Salida
La salida debe ser un JSON o Markdown con:
- `timestamp`: Tiempo del segmento.
- `text`: Texto hablado.

## Scripts Incluidos

- `extract.ts`: Script de Playwright para ejecución rápida.

## Notas Técnicas
- YouTube hace A/B testing constante de su UI. Si los selectores fallan, se debe re-explorar el DOM usando el `browser_subagent`.
- El botón de transcripción NO aparece si el video no tiene subtítulos disponibles.


## Guardrails (Critical Rules)
- **NEVER** execute destructive operations without explicit user confirmation
- **ALWAYS** verify target exists before operating
- **ALWAYS** handle errors gracefully — skip with warning, don't crash


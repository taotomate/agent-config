---
name: experimental-compress
description: >
  Motor experimental de Destilación Continua. Soporta dos modos principales a pedido del usuario: 
  'status' (para ver el progreso de los chunks procesados en segundo plano) y 'reduce' (para 
  inyectar el SOTA Sync Point en el hilo actual).
  Trigger: "prueba compress", "distill experimental", "telemetria de destilacion".
metadata:
  version: "3.0"
author: TaoTomate
generator_model: gemini-1.5-pro
inherited_from: experimental-compress/SKILL.md
migrated_by: skill-migrator@1.0.0
---

## Contexto y Triggers
**Cuándo usar esta skill:**
- Cuando el usuario pide ver el progreso de los chunks procesados en segundo plano (`'status'`).
- Cuando se requiere inyectar el SOTA Sync Point en el hilo actual (`'reduce'`).
- Triggers: "prueba compress", "distill experimental", "telemetria de destilacion".

## Pre-requisitos
- [ ] Acceso de ejecución al script `D:\Engram_SDD\Proj-Distill\distill_experimental.py`.
- [ ] Tener acceso al ID real de la conversación actual (`<conversation_id>`).

## Fases de Ejecución

> **[REGLA UNIVERSAL: DRY-RUN / SIMULACRO]**
> Si el usuario solicita la ejecución en modo `--dry-run` o pide un "simulacro", el agente **NO** ejecutará comandos que alteren el estado del sistema ni llamará a herramientas MCP destructivas en la Fase de Acción. 
> En su lugar, el agente imprimirá el payload exacto (JSON, bloque de código o parámetros) que planeaba ejecutar, y se detendrá a esperar la aprobación explícita del humano.

### 1. Fase de Diagnóstico
- Identificar la intención del usuario basándose en el trigger: ¿Es una consulta de telemetría (Status Check) o una ejecución manual de la compresión (SOTA Injection)?

### 2. Fase de Acción
- **Si es Status Check (Telemetría):**
  - Ejecutar el script en modo status (ver sección Comandos).
- **Si es SOTA Injection (Manual):**
  - Ejecutar primero el script en modo `map-only` apuntando a esta conversación para procesar sus chunks pendientes. Puede ser Mapeo Completo o Parcial.
  - Ejecutar inmediatamente después el script en modo `reduce` para generar el dossier consolidado, incluso si no se mapeó todo el hilo.

### 3. Fase de Verificación
- **Para Status Check:** Leer el stdout de la consola y mostrar el reporte de hilos procesados y pendientes, formateándolo limpiamente en el chat.
- **Para SOTA Injection:** El script en modo `reduce` devolverá un JSON. Extraer el campo `summary` (UX Sync). Escupir el contenido *exacto* de ese `summary` en el chat de inmediato.

## Guardrails (Reglas Críticas)
- **SIEMPRE** debes usar el ID real de este chat al reemplazar `<conversation_id>`.
- **NUNCA** resumas ni escondas en un artefacto el contenido del `summary` devuelto en el modo `reduce`. Debes imprimirlo exactamente como viene; esto sirve como el ancla de memoria.
- **SIEMPRE** ejecuta la fase de `reduce` después del `map-only` para inyecciones manuales.

## Estructuras de Datos / Ejemplos y Comandos

### Comandos de Ejecución

**Status Check (Telemetría):**
```bash
python D:\Engram_SDD\Proj-Distill\distill_experimental.py --mode status
```

**SOTA Injection - Mapeo Completo:**
```bash
python D:\Engram_SDD\Proj-Distill\distill_experimental.py --mode map-only --conversation-id <conversation_id>
```

**SOTA Injection - Mapeo Parcial (Panorámica Rápida):**
```bash
python D:\Engram_SDD\Proj-Distill\distill_experimental.py --mode map-only --conversation-id <conversation_id> --max-chunks 5
```

**SOTA Injection - Reducción (Dossier Consolidado):**
```bash
python D:\Engram_SDD\Proj-Distill\distill_experimental.py --mode reduce --conversation-id <conversation_id>
```
*(Nota: Si hay un modelo de map/reduce específico configurado, se puede añadir `--map-models <modelo>` o `--reduce-model <modelo>` respectivamente a los comandos).*

## ⚠️ Residuos de Migración (Feedback para evolución)
*(Toda la información ha sido mapeada satisfactoriamente, adaptando las lógicas de scripts externos a los nuevos Guardrails y Fases)*

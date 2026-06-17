---
name: conversation-distillation
description: >
  Realiza una destilación técnica de alto nivel (Senior Architect mode), priorizando el 
  "Qué" y el "Para qué". Filtra el ruido técnico y las idas y vueltas, consolidando 
  solo las decisiones finales y su justificación arquitectónica.
  Trigger: "destilar hilo", "destilación técnica", "extraer contexto", "crear dossier".
metadata:
  version: "3.0"
author: TaoTomate
generator_model: gemini-1.5-pro
inherited_from: conversation-distillation/SKILL.md
---

## Contexto y Triggers
**Cuándo usar esta skill:**
- Cuando el usuario pide destilar, resumir o crear un dossier arquitectónico de la conversación actual.
- Triggers: "destilar hilo", "destilación técnica", "extraer contexto", "crear dossier".

## Pre-requisitos
- [ ] Acceso de ejecución al script `D:\Engram_SDD\Proj-Distill\distill.py`.
- [ ] Tener el ID real de la conversación actual (`<conversation_id>`).
- [ ] El usuario debe especificar un `<topic_name>` o deberás derivarlo del contexto principal de la sesión.

## Fases de Ejecución

> **[REGLA UNIVERSAL: DRY-RUN / SIMULACRO]**
> Si el usuario solicita la ejecución en modo `--dry-run` o pide un "simulacro", el agente **NO** ejecutará comandos que alteren el estado del sistema ni llamará a herramientas MCP destructivas en la Fase de Acción. 
> En su lugar, el agente imprimirá el payload exacto (JSON, bloque de código o parámetros) que planeaba ejecutar, y se detendrá a esperar la aprobación explícita del humano.

### 1. Fase de Diagnóstico
- Identificar el `<topic_name>` a destilar de acuerdo con la conversación, o preguntar al usuario si no es evidente.
- Extraer la intención principal ("Para qué"): el dossier DEBE centrarse en el propósito original.

### 2. Fase de Acción
- **Delegate to Unified Distiller**: Ejecutar la herramienta central de destilación en la nube (Groq):
  ```bash
  python D:\Engram_SDD\Proj-Distill\distill.py --conversation-id <conversation_id> --topic <topic_name> --force-provider groq
  ```
- El script procesará automáticamente la conversación en capas, construirá referencias, preservará trade-offs y escribirá el archivo en `C:\Users\user\.gemini\antigravity\knowledge\`, además de persistirlo en Engram.

### 3. Fase de Verificación
- Leer el output o revisar el archivo markdown generado.
- **Artifact Creation**: Crear un artefacto markdown (`.md`) para presentarle al usuario el contenido devuelto por el script, de modo que pueda revisarlo y validarlo.

## Guardrails (Reglas Críticas)
- **Philosophy - Intent over Noise:** No listar cambios mecánicos, sino explicar decisiones y trade-offs ("Se eligió X porque Y"). Descartar idas y vueltas de debugging.
- **For Future Self:** El contenido debe estar escrito asumiendo que alguien retomará el proyecto en 6 meses sin necesidad de releer el chat original.
- **Output Identity:** El artefacto debe comenzar obligatoriamente con `Distilled by: Cloud LLM via Antigravity`.
- **Absolute Paths:** Las rutas de archivos referenciadas deben ser SIEMPRE absolutas.
- **Mermaid Diagrams:** Son requeridos para visualizar decisiones de arquitectura dentro del dossier.

## Estructuras de Datos / Ejemplos y Comandos

**Comando de Ejecución (Cloud Distillation):**
```bash
python D:\Engram_SDD\Proj-Distill\distill.py --conversation-id <conversation_id> --topic <topic_name> --force-provider groq
```

## ⚠️ Residuos de Migración (Feedback para evolución)
*(Migrado exitosamente desde v2.0 a IaC v1.2, manteniendo las filosofías de "Noise Cancellation" y "Purpose First" intactas)*

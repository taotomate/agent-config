---
name: conversation-distillation
description: >
  Realiza una destilación técnica de alto nivel (Senior Architect mode), priorizando el 
  "Qué" y el "Para qué". Filtra el ruido técnico y las idas y vueltas, consolidando 
  solo las decisiones finales y su justificación arquitectónica.
  Trigger: "destilar hilo", "destilación técnica", "extraer contexto", "crear dossier".
metadata:
  version: "2.0"
---

## Philosophy: Intent over Noise

- **PURPOSE FIRST**: El alma del dossier es la intención inicial del usuario. Si el dossier no explica el "Para qué", falló.
- **DECISION LOGGING**: No listamos cambios, explicamos decisiones. "Se eligió X porque Y (trade-off)".
- **NOISE CANCELLATION**: Las idas y vueltas de debugging o errores de sintaxis se descartan. Solo queda la solución final robusta.
- **FOR FUTURE SELF**: Escribir pensando en que el "Yo del Futuro" necesita retomar el proyecto en 6 meses sin releer el chat.

## Unified Execution Protocol (v3.0)

1. **Delegate to Unified Distiller**: Run the central distillation tool using the cloud provider:
   `python D:\Engram_SDD\Proj-Distill\distill.py --conversation-id <conversation_id> --topic <topic_name> --force-provider groq`
2. **Review Output**: The script will automatically process the conversation in layers, build references, preserve trade-offs, write the markdown file to `C:\Users\user\.gemini\antigravity\knowledge\`, and save it to Engram.
3. **Artifact Creation**: Create a markdown artifact with the full content returned by the script.

## Output Requirements
- **Identity**: Start with `Distilled by: Cloud LLM via Antigravity`.
- **Absolute Paths**: Mandatory for all file references.
- **Mermaid Diagrams**: Required for architecture visualization.



<!-- youtube-scraper: processed -->

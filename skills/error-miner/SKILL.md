---
name: error-miner
description: >
  Analiza la transcripción del hilo buscando intervenciones manuales o desvíos del protocolo, y los anexa objetivamente al error_log.md usando un mecanismo stateless de append.
  Trigger: "minar errores", "cerrar hilo y minar", "postmortem", "auditar historial".
license: Apache-2.0
metadata:
  author: TaoTomate
  generator_model: gemini-1.5-pro
  version: "1.0"
  inherited_from: custom local architecture
---

## When to Use

- Al final de una sesión de trabajo donde el humano tuvo que intervenir para corregir una alucinación o un desvío del protocolo.
- Cuando el usuario explícitamente pide auditar o minar el historial en busca de errores.

## Critical Patterns (Anti-Sesgo y Estructura)

- **Objetividad Absoluta:** Prohibido usar sesgos defensivos de LLM (ej. no digas "prompt ambiguo" o "el usuario engañó"). Describí la falla técnica tal cual fue: qué comando se omitió, qué regla se violó o por qué no se siguió el ruteo estricto.
- **Stateless Append:** No leas el archivo de log para buscar el último ID. Generá un ID basado en el timestamp actual (`YYYYMMDDHHMMSS`).
- **No reescribir el archivo:** Usa SIEMPRE comandos de append (`>>` en bash o `Add-Content` en PowerShell) para inyectar el bloque de markdown al final del `D:\TaoTomate.Dots\agent-config\shared\global_error_log.md`.

## Estructura del Log

Cada nuevo error anexado debe tener este bloque exacto:

```markdown
## Error #{YYYYMMDDHHMMSS}
- **Proyecto / Workspace:** [Nombre del proyecto o repositorio donde ocurrió el fallo, ej: Proj-Reestructura-AGENTS]
- **Fase Activa:** [Qué estaba haciendo el agente. Ej: Orquestación L1, sdd-explore, sdd-apply, etc.]
- **Modelo:** [Nombre del modelo LLM que falló, ej: gemini-1.5-pro, claude-3.5-sonnet]
- **Contexto de la falla:** [Comando original o intención del usuario. Literal, sin adjetivar]
- **Regla Violada:** [Qué protocolo, archivo o directiva se ignoró]
- **Acción Errónea:** [Qué intentó hacer el agente en vez de seguir la regla]
- **Causa Raíz:** [Fallo técnico o sesgo arquitectónico. Ej: Priorización del "helpful" bias sobre la "compliance", falta de lectura del registry]
- **Resolución:** [Cómo intervino el usuario o cómo se corrigió]
```

## Commands

Para anexar el error en PowerShell de forma limpia (asegúrate de adaptar el timestamp y los campos):

```powershell
$timestamp = Get-Date -Format "yyyyMMddHHmmss"
$logPath = "D:\TaoTomate.Dots\agent-config\shared\global_error_log.md"
$content = @"

## Error #$timestamp
- **Proyecto / Workspace:** ...
- **Fase Activa:** ...
- **Modelo:** ...
- **Contexto de la falla:** ...
- **Regla Violada:** ...
- **Acción Errónea:** ...
- **Causa Raíz:** ...
- **Resolución:** ...
"@

Add-Content -Path $logPath -Value $content -Encoding UTF8
```

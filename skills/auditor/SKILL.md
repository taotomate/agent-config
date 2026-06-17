---
name: auditor
description: Protocolo de recuperación y análisis ante fallos del sistema o violaciones de guardrails.
version: 1.0.0
author: TaoTomate
generator_model: gemini-1.5-pro
inherited_from: auditor/SKILL.md
migrated_by: skill-migrator@1.0.0
---

## Contexto y Triggers
**Cuándo usar esta skill:**
- Cuando un script o comando en ejecución devuelve un error `exit code != 0`.
- Cuando un proceso de validación o linting falla espectacularmente.
- Cuando el agente violó un guardrail definido en la skill activa.

## Pre-requisitos
- Acceso de lectura a los logs de error (ej. `.tmp/last_error.log`, `.atl/error_log.md`, o salida de consola).

## Fases de Ejecución

> **[REGLA UNIVERSAL: DRY-RUN / SIMULACRO]**
> Si el usuario solicita la ejecución en modo `--dry-run` o pide un "simulacro", el agente **NO** ejecutará comandos que alteren el estado del sistema ni llamará a herramientas MCP destructivas en la Fase de Acción. 
> En su lugar, el agente imprimirá el payload exacto (JSON, bloque de código o parámetros) que planeaba ejecutar, y se detendrá a esperar la aprobación explícita del humano.

### 1. Captura (Snapshot)
Extrae el error exacto y el contexto (últimos comandos ejecutados o tokens de salida). No intentes adivinar el error.

### 2. Análisis (Mismatch Report)
Compara el error ocurrido con la Skill que se estaba ejecutando:
- ¿Faltó un parámetro?
- ¿Se violó una restricción de la sección `Guardrails`?
- ¿El entorno no cumple los `Pre-requisitos`?

### 3. Categorización y Acción
Clasifica el error y actúa en consecuencia:
- **LogicError (Recuperable):** El código o prompt tiene un bug subsanable. *Acción:* Aplica el parche y re-ejecuta. Registra el aprendizaje en `directives/errors_learned.md`.
- **ContextOverflow (Falla del LLM):** El agente perdió el hilo de ejecución o alucinó. *Acción:* Limpiar contexto, resumir estado y reintentar con un prompt más acotado.
- **SystemError (Falla fatal):** Error de permisos, caída de red, falta de dependencias crónicas. *Acción:* Suspender la ejecución y escalar al Arquitecto humano.

## Guardrails
- **NO** intentes aplicar parches iterativos ciegos (más de 3 reintentos sin éxito indica fallo fatal).
- **SIEMPRE** documenta la causa raíz antes de proponer y aplicar la solución.

## Ejemplos y Comandos
N/A - Esta skill dicta un proceso de razonamiento y orquestación cognitiva, no comandos de terminal específicos.

## Troubleshooting
Si el auditor mismo falla al intentar leer los logs, abortar todas las operaciones, crear un archivo `FATAL_CRASH.md` y solicitar intervención manual.

---
name: double-blind-review
description: >
  Protocolo de revisión adversarial paralela que lanza dos auditores independientes (doble ciego) 
  simultáneamente, sintetiza sus hallazgos, aplica correcciones y re-evalúa hasta obtener 
  consenso o alcanzar el límite de iteraciones.
  Trigger: "double-blind review", "revisión doble ciego", "auditar", "review adversarial".
metadata:
  version: "3.0"
author: TaoTomate
generator_model: gemini-1.5-pro
inherited_from: double-blind-review/SKILL.md
---

## Contexto y Triggers
**Cuándo usar esta skill:**
- Cuando el usuario solicita "double-blind review", "revisión doble ciego", "auditar", "review adversarial".
- Después de implementaciones significativas antes de un merge.
- Cuando se requiere una revisión de alta confianza sobre código, características o arquitectura.
- Cuando un solo revisor podría pasar por alto casos extremos (edge cases).

## Pre-requisitos
- [ ] Conocer el archivo(s) o componente específico a auditar (`<absolute_path_to_code_file>`).
- [ ] Disponibilidad del script de ejecución local: `skills/double-blind-review/scripts/audit_runner.js`.

## Fases de Ejecución

> **[REGLA UNIVERSAL: DRY-RUN / SIMULACRO]**
> Si el usuario solicita la ejecución en modo `--dry-run` o pide un "simulacro", el agente **NO** ejecutará comandos que alteren el estado del sistema ni llamará a herramientas MCP destructivas en la Fase de Acción. 
> En su lugar, el agente imprimirá el comando exacto (JSON, bloque de código o parámetros) que planeaba ejecutar, y se detendrá a esperar la aprobación explícita del humano.

### 1. Fase de Diagnóstico (Skill Resolution & Scope)
- Confirmar el *target* específico (archivo o ruta) a revisar. Si no está claro, preguntar al usuario antes de proceder.
- Consultar el registry (`.atl/skill-registry.md` o engram) para hacer match con habilidades del proyecto basadas en extensión de archivo o framework, y construir un bloque de `## Project Standards (auto-resolved)` si aplica. (Estos se pasan en los criterios personalizados si es necesario).

### 2. Fase de Acción (Parallel Blind Review)
- El **orquestador NUNCA hace la revisión de código por sí mismo**. Debe ejecutar el script local `audit_runner.js` que se encarga de instanciar a los auditores en paralelo, inyectar los estándares y sintetizar.
- Ejecutar el comando Node apuntando al archivo objetivo.

### 3. Fase de Verificación (Verdict Synthesis & Iteration)
- El script `audit_runner.js` escupirá un reporte en Markdown con la síntesis de los dos auditores.
- Mostrar la tabla de veredictos tal cual la generó el runner al usuario.
- Si hay problemas detectados (Confirmed CRITICALs o Real WARNINGs), **PREGUNTAR** al usuario: "¿Arreglo los issues confirmados?".
- **Fase de Corrección y Re-evaluación**: Si el usuario dice que SÍ, delegar los arreglos en una iteración (aplicar los fixes en los archivos de forma estricta). Luego de corregir, VOLVER a lanzar el protocolo de auditoría `audit_runner.js` para re-evaluar. Repetir hasta obtener `VERDICT: APPROVED ✅` o hasta que el usuario decida frenar (`ESCALATED ⚠️`).

## Guardrails (Reglas Críticas)
- **Bloqueo Absoluto**: NO hacer "git push" ni "git commit" luego de arreglar problemas SIN ANTES hacer la re-evaluación paralela completa y obtener `VERDICT: APPROVED`.
- **Clasificación de Warnings**:
  - `WARNING (real)`: Causa bug, pérdida de datos o hueco de seguridad en prod.
  - `WARNING (theoretical)`: Requiere condiciones hiper rebuscadas o corruptas. Solo se reporta como INFO, NO bloquea el veredicto ni se corrige forzosamente.
- **Convergencia**: En la Ronda 2, solo se re-evalúa si quedaron `CRITICALs` confirmados. Warnings reales confirmados se arreglan sin re-lanzar auditoría, y los sugeridos/teóricos no se tocan. Esto evita ciclos infinitos.

## Estructuras de Datos / Ejemplos y Comandos

**Comando de Ejecución del Runner Local:**
```bash
# Ejecutar auditoría doble ciego completa en un archivo:
node skills/double-blind-review/scripts/audit_runner.js --codePath <absolute_path_to_code_file> [options]

# Opciones disponibles:
#  --customCriteria "Custom review guidelines"   Inyectar estándares y reglas específicas
#  --localUrl "http://localhost:1234/v1"         URL custom proxy Local
#  --cloudUrl "http://localhost:5678/v1"         URL custom proxy Cloud
```

## ⚠️ Residuos de Migración (Feedback para evolución)
*(Migrado a IaC v1.2. Se condensa la inmensa cantidad de prompts de auditoría en la invocación estricta al `audit_runner.js` que maneja el loop deterministicamente, trasladando el control de los "agentes delegados" a la herramienta automatizada)*

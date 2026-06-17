---
name: [nombre-de-la-skill]
description: [Descripción breve de 1 o 2 líneas]
version: 1.0.0
author: [Tu Nombre]
---

## Contexto y Triggers
**Cuándo usar esta skill:**
- Detalla los escenarios específicos donde el orquestador debe invocar esta skill.
- *Ejemplo: "Cuando el usuario pida crear un ticket en GitHub o reportar un bug".*

## Pre-requisitos
Lista de condiciones de entorno que deben cumplirse **antes** de empezar.
- [ ] Herramienta instalada (ej. `gh cli`).
- [ ] Directorios específicos existentes.
- [ ] Variables de entorno configuradas.

## Fases de Ejecución
Desglosa el proceso en pasos deterministas. No dejes espacio para la improvisación.

> **[REGLA UNIVERSAL: DRY-RUN / SIMULACRO]**
> Si el usuario solicita la ejecución en modo `--dry-run` o pide un "simulacro", el agente **NO** ejecutará comandos que alteren el estado del sistema ni llamará a herramientas MCP destructivas en la Fase de Acción. 
> En su lugar, el agente imprimirá el payload exacto (JSON, bloque de código o parámetros) que planeaba ejecutar, y se detendrá a esperar la aprobación explícita del humano.

### 1. Fase de Diagnóstico
- Qué investigar o leer antes de actuar (ej. leer `.clauderules` o verificar duplicados).
### 2. Fase de Acción
- Los comandos o modificaciones a realizar sobre el código o sistema.
### 3. Fase de Verificación
- Cómo probar objetivamente que la acción fue exitosa (ej. correr `npm test`, validar JSON contra un schema).

## Guardrails (Reglas Críticas)
Restricciones innegociables para el modelo de IA.
- **NO** [Comportamiento prohibido o asunción peligrosa].
- **SIEMPRE** [Regla estricta a seguir obligatoriamente].

## Estructuras de Datos / Ejemplos y Comandos
Provee contexto rico para el LLM para evitar alucinaciones de formato.
- Ejemplos de comandos (`bash` o scripts).
- Formatos esperados (JSON schemas, plantillas Markdown exactas).
- Árbol de decisión (Decision Tree) si la lógica tiene ramificaciones complejas.

## Troubleshooting
Guía de recuperación rápida para errores comunes y específicos de esta skill.
- *Si ocurre [Error X], la causa probable es [Causa Y]. Ejecuta [Comando Z] para resolverlo.*

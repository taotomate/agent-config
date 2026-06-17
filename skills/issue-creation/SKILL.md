---
name: issue-creation
description: Issue creation workflow for Agent Teams Lite using the GitHub MCP Server.
version: 1.2.0
author: TaoTomate
generator_model: gemini-1.5-pro
inherited_from: issue-creation/SKILL.md
migrated_by: skill-migrator@1.0.0
---

## Contexto y Triggers
**Cuándo usar esta skill:**
- Creación de un GitHub issue (bug report o feature request).
- Ayudar a un colaborador a reportar un issue.
- Triage o aprobación de issues como mantenedor.

## Pre-requisitos
- [ ] Servidor MCP de GitHub configurado y habilitado.
- [ ] El repositorio destino tiene las plantillas `.github/ISSUE_TEMPLATE/bug_report.yml` y `.github/ISSUE_TEMPLATE/feature_request.yml`.

## Fases de Ejecución

> **[REGLA UNIVERSAL: DRY-RUN / SIMULACRO]**
> Si el usuario solicita la ejecución en modo `--dry-run` o pide un "simulacro", el agente **NO** ejecutará comandos que alteren el estado del sistema ni llamará a herramientas MCP destructivas en la Fase de Acción. 
> En su lugar, el agente imprimirá el payload exacto (JSON, bloque de código o parámetros) que planeaba ejecutar, y se detendrá a esperar la aprobación explícita del humano.

### 1. Fase de Diagnóstico
- Ejecutar una búsqueda de issues existentes usando la herramienta MCP `search_issues` para asegurar que no sea un duplicado.
- Determinar si el requerimiento es un Bug, Feature o Pregunta. (Si es Pregunta, derivar a Discussions y abortar la skill).

### 2. Fase de Acción
- Extraer del usuario toda la información requerida según el tipo de issue (ver sección Estructuras de Datos).
- Construir el cuerpo del issue (Markdown string) respetando estrictamente el formato de los campos esperados.
- Invocar la herramienta MCP `create_issue` con el owner, repo, title y body correspondientes.

### 3. Fase de Verificación
- Confirmar que la herramienta MCP devuelve un código de éxito y el número del nuevo issue.
- Si el repositorio está configurado con auto-labels, verificar internamente que el ciclo se completó (ej. `status:needs-review`).

## Guardrails (Reglas Críticas)
- **NO** crear issues en blanco; SIEMPRE usar la estructura Markdown definida por las plantillas `.yml` del repositorio objetivo.
- **NO** redirigir preguntas a issues; SIEMPRE mandarlas a [Discussions](https://github.com/Gentleman-Programming/agent-teams-lite/discussions).
- **SIEMPRE** priorizar el uso del servidor MCP nativo por sobre la ejecución de comandos `gh` en terminal.

## Estructuras de Datos / Ejemplos y Comandos

### Plantilla de Formato: Bug Report
Cuando armes el parámetro `body` para la herramienta MCP `create_issue`, inyecta este Markdown estricto:

```markdown
### Pre-flight Checks
- [x] I have searched existing issues and this is not a duplicate
- [x] I understand this issue needs status:approved before a PR can be opened

### Bug Description
[Descripción clara del error]

### Steps to Reproduce
1. [Paso 1]
2. [Paso 2]

### Expected Behavior
[Lo que debía pasar]

### Actual Behavior
[Lo que pasó, incluye logs en formato bloque de código]

### Operating System
[OS]

### Agent / Client
[Cliente usado]
```

### Plantilla de Formato: Feature Request
Cuando armes el parámetro `body` para la herramienta MCP `create_issue`, usa este Markdown estricto:

```markdown
### Pre-flight Checks
- [x] I have searched existing issues and this is not a duplicate
- [x] I understand this issue needs status:approved before a PR can be opened

### Problem Description
[El punto de dolor que esto resuelve]

### Proposed Solution
[Cómo debería funcionar desde la perspectiva del usuario]

### Affected Area
[Scripts, Skills, Docs, etc.]
```

### Ejemplo de invocación MCP (Representación JSON)
El agente debe estructurar la llamada a la herramienta MCP `create_issue` similar a esto:
```json
{
  "owner": "Gentleman-Programming",
  "repo": "agent-teams-lite",
  "title": "fix(scripts): error de auth en github mcp",
  "body": "### Pre-flight Checks\n- [x] I have searched..."
}
```

## Troubleshooting
- *Si la herramienta MCP devuelve un error de timeout o credenciales inválidas:* El usuario debe revisar la configuración de sus tokens (`GITHUB_PERSONAL_ACCESS_TOKEN`) en el archivo config de MCP.
- *Si el MCP no está disponible:* Abortar e invocar la skill `auditor`, no intentes recurrir al `gh cli` de la terminal a menos que el humano lo ordene explícitamente.

---
name: branch-pr
description: >
  PR creation workflow for Agent Teams Lite following the issue-first enforcement system.
  Trigger: When creating a pull request, opening a PR, or preparing changes for review.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "2.0"
generator_model: gemini-1.5-pro
inherited_from: branch-pr/SKILL.md
migrated_by: skill-migrator@1.0.0
---

## Contexto y Triggers
**Cuándo usar esta skill:**
- Creación de un pull request para cualquier cambio.
- Preparar un branch para ser subido y evaluado.
- Ayudar a un contribuidor a abrir un PR.

## Pre-requisitos
- [ ] Debe existir un issue aprobado con la etiqueta `status:approved` vinculado.
- [ ] El código debe estar localmente modificado o listo para commitear.

## Fases de Ejecución

> **[REGLA UNIVERSAL: DRY-RUN / SIMULACRO]**
> Si el usuario solicita la ejecución en modo `--dry-run` o pide un "simulacro", el agente **NO** ejecutará comandos que alteren el estado del sistema ni llamará a herramientas MCP destructivas en la Fase de Acción. 
> En su lugar, el agente imprimirá el payload exacto (JSON, bloque de código o parámetros) que planeaba ejecutar, y se detendrá a esperar la aprobación explícita del humano.

### 1. Fase de Diagnóstico
- Verificar que el issue a enlazar tenga la etiqueta `status:approved`.

### 2. Fase de Acción
- Crear un branch siguiendo la nomenclatura: `type/description`.
- Implementar los cambios utilizando commits convencionales.
- Ejecutar `shellcheck` en los scripts modificados.
- Abrir el PR utilizando el PR template correspondiente del repositorio.
- Agregar exactamente UNA etiqueta de tipo `type:*`.

### 3. Fase de Verificación
- Esperar a que las comprobaciones automáticas pasen en el repositorio.

## Guardrails (Reglas Críticas)
- **SIEMPRE** vincula un issue aprobado a CADA pull request, no hay excepciones.
- **SIEMPRE** agrega exactamente UNA etiqueta `type:*` al PR.
- **NUNCA** hagas push ni asumas que el merge es posible sin que las validaciones automáticas pasen.
- **NUNCA** utilices `Co-Authored-By` de asistentes AI en los commits.

## Estructuras de Datos / Ejemplos y Comandos

### Nomenclatura de Branch
Expresión regular estricta: `^(feat|fix|chore|docs|style|refactor|perf|test|build|ci|revert)\/[a-z0-9._-]+$`
**Formato:** `type/description` (ej. `feat/user-login`, `fix/zsh-glob-error`).

### Formato de PR Body
```markdown
Closes #<issue-number>

| File | Change |
|------|--------|
| `path/to/file` | What changed |

- [x] Scripts run without errors: `shellcheck scripts/*.sh`
- [x] Manually tested the affected functionality
- [x] Skills load correctly in target agent
```
*(Debe usarse el `.github/PULL_REQUEST_TEMPLATE.md`)*

### Conventional Commits
Regex: `^(build|chore|ci|docs|feat|fix|perf|refactor|revert|style|test)(\([a-z0-9\._-]+\))?!?: .+`
**Formato:** `type(scope): description` o `type: description` (el `!` indica breaking change).

### Comandos de Ejecución
```bash
git checkout -b feat/my-feature main
shellcheck scripts/*.sh
git push -u origin feat/my-feature
gh pr create --title "feat(scope): description" --body "Closes #N"
gh pr edit <pr-number> --add-label "type:feature"
```

## ⚠️ Residuos de Migración (Feedback para evolución)
*(Toda la información ha sido mapeada satisfactoriamente)*

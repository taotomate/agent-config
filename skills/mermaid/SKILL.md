---
model_tier: inherited
name: mermaid
description: Render Mermaid diagrams as SVG or ASCII art using beautiful-mermaid. Use when users need to create flowcharts, sequence diagrams, state diagrams, class diagrams, or ER diagrams. Supports both graphical SVG output and terminal-friendly ASCII/Unicode output.
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
- Triggers: "mermaid", "use mermaid"



> **⚠️ Platform note — read before running any command.** The shell snippets in this skill are written for **macOS / Linux** (bash/zsh). Always check which OS you are on first. On **Windows** do **not** run them verbatim — the underlying tool/CLI commands are usually cross-platform, but the surrounding shell syntax is not. Translate it to PowerShell before running:
>
> | bash (macOS / Linux) | PowerShell (Windows) |
> | --- | --- |
> | `a && b` | run as two steps, or `a; if ($?) { b }` |
> | `cat <<'EOF' \| tool …` (heredoc) | write the text to a temp file, then pipe/pass that file to the tool |
> | `VAR=$(cmd)` … `$VAR` | `$VAR = cmd` … `$VAR` |
> | `cmd > /dev/null` | `cmd > $null` |
> | `… \| grep PAT` | `… \| Select-String PAT` |
> | `… \| jq …` | `… \| ConvertFrom-Json`, then read the fields |
> | `python3 x.py` | `python x.py` (or `py x.py`) |
> | `~/dir`, `/tmp` | `$env:USERPROFILE\dir`, `$env:TEMP` |
> | `cp` / `mkdir -p` / `rm -rf` | `Copy-Item` / `New-Item -ItemType Directory -Force` / `Remove-Item -Recurse -Force` |
>
> If a command has no obvious Windows equivalent, prefer the built-in file/HTTP tools over raw shell.

# Mermaid Diagram Renderer

Render Mermaid diagrams using `beautiful-mermaid` library. Supports 5 diagram types with dual output modes.


## Prerequisites
- [ ] Read access to target files/directories
- [ ] Write access for auto-fix operations


## Quick Start

> Dependencies (`beautiful-mermaid`) auto-install on first run.

### SVG Output (Default)

```bash
# From file
npx tsx scripts/render.ts diagram.mmd --output diagram.svg

# From stdin
echo "graph LR; A-->B-->C" | npx tsx scripts/render.ts --stdin --output flow.svg
```

### ASCII Output (Terminal)

```bash
# ASCII art for terminal display
npx tsx scripts/render.ts diagram.mmd --ascii

# Pipe directly
echo "graph TD; Start-->End" | npx tsx scripts/render.ts --stdin --ascii
```

Output example:

```
┌───────┐     ┌─────┐
│ Start │────▶│ End │
└───────┘     └─────┘
```

## Supported Diagrams

| Type      | Syntax            | Best For                |
| --------- | ----------------- | ----------------------- |
| Flowchart | `graph TD/LR`     | Processes, decisions    |
| Sequence  | `sequenceDiagram` | API calls, interactions |
| State     | `stateDiagram-v2` | State machines          |
| Class     | `classDiagram`    | OOP design              |
| ER        | `erDiagram`       | Database schemas        |

## Theming (SVG only)

```bash
npx tsx scripts/render.ts diagram.mmd --theme github-dark --output out.svg
```

Use invalid theme name to see available themes list (e.g., `--theme ?`)

## Resources

- `scripts/render.ts` - Main rendering script
- `references/syntax.md` - Mermaid syntax quick reference


## Guardrails (Critical Rules)
- **NEVER** execute destructive operations without explicit user confirmation
- **ALWAYS** verify target exists before operating
- **ALWAYS** handle errors gracefully — skip with warning, don't crash


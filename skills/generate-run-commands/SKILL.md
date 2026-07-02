---
model_tier: inherited
name: generate-run-commands
description: Generate or modify run commands for the current session. Use when the user wants to set up or update run commands that appear in the session's Run button.
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
- Triggers: "generate-run-commands", "use generate-run-commands"


<!-- Customize this skill and select save to override its behavior. Delete that copy to restore the built-in behavior. -->

# Generate Run Commands

Help the user set up run commands for the current Agent Session workspace. Run commands appear in the session's Run button in the title bar.


## Prerequisites
- [ ] Read access to target files/directories
- [ ] Write access for auto-fix operations


## Understanding the task schema

A run command is a `tasks.json` task with:
- `"inAgents": true` — required: makes the task appear in the Agents run button
- `"runOptions": { "runOn": "worktreeCreated" }` — optional: auto-runs the task whenever a new worktree is created (use for setup/install commands)

```json
{
  "tasks": [
    {
      "label": "Install dependencies",
      "type": "shell",
      "command": "npm install",
      "inAgents": true,
      "runOptions": { "runOn": "worktreeCreated" }
    },
    {
      "label": "Start dev server",
      "type": "shell",
      "command": "npm run dev",
      "inAgents": true
    }
  ]
}
```

## Decision logic

**First, read the existing `.vscode/tasks.json`** to check for existing run commands (`inAgents: true` tasks).

**If run commands already exist:** treat this as a modify request — ask the user what they'd like to change (add, remove, or update a command).

**If no run commands exist:** try to infer the right commands from the workspace:
- Check `package.json`, `Makefile`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `.nvmrc`, or other project files to understand the stack and common commands.
- If it's clear what the setup command is (e.g., `npm install`, `pip install -r requirements.txt`), add it with `"runOptions": { "runOn": "worktreeCreated" }` — no need to ask.
- If it's clear what the primary run/dev command is (e.g., `npm run dev`, `cargo run`), add it with just `"inAgents": true`.
- **Only ask the user** if the commands are ambiguous (e.g., multiple equally valid options, no recognizable project structure, or the project uses a non-standard setup).

## Writing the file

Always write to `.vscode/tasks.json` in the workspace root. If the file already exists, merge — do not overwrite unrelated tasks.

After writing, briefly confirm what was added and how to trigger it from the Run button.


## Guardrails (Critical Rules)
- **NEVER** execute destructive operations without explicit user confirmation
- **ALWAYS** verify target exists before operating
- **ALWAYS** handle errors gracefully — skip with warning, don't crash


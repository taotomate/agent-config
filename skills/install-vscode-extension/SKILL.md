---
model_tier: inherited
name: install-vscode-extension
description: 'How to install a VS Code extension from an extension ID. Useful when the user wants to add new capabilities to their VS Code environment by installing extensions.'
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
- Triggers: "install-vscode-extension", "use install-vscode-extension"



# Installing VS Code extensions

1. VS Code extensions are identified by their unique extension ID, which typically follows the format `publisher.extensionName`. For example, the Python extension by Microsoft has the ID `ms-python.python`.
2. To install a VS Code extension, you need to use the VS Code command `workbench.extensions.installExtension` and pass in the extension ID. The args are of the format:
```
[extensionId, { enable: true, installPreReleaseVersion: boolean }]
```
> NOTE: install the pre-release version of the extension if the user explicitly mentions it or if the current environment is VS Code Insiders. Otherwise, install the stable version.
3. Run that command via the `copilot_runVscodeCommand` tool. Make sure to pass the `skipCheck` argument as true to avoid checking if the command exists, as we know it does.

## Prerequisites
- [ ] Read access to target files/directories
- [ ] Write access for auto-fix operations



## Guardrails (Critical Rules)
- **NEVER** execute destructive operations without explicit user confirmation
- **ALWAYS** verify target exists before operating
- **ALWAYS** handle errors gracefully — skip with warning, don't crash


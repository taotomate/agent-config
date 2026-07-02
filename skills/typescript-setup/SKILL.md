---
model_tier: inherited
name: typescript-setup
description: How to set up a new TypeScript project
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
- Triggers: "typescript-setup", "use typescript-setup"



To set up a new repo with TypeScript, follow these steps unless you have reason to deviate from them:

 * `npm install --save-dev typescript@latest` (or use the user's package manager of choice)
 * Run `npx tsc --init` to create a `tsconfig.json` file
 * Read the tsconfig.json it generates and make the edits suggested in that file:
   * If running server-side or local scripts, add `node` to `types` and `npm install --save-dev @types/node`
   * Set `rootDir` to `src` and `outDir` to `dist`
   * If using vite, esbuild, or similar bundlers, set `moduleResolution` to `bundler`
     * If you have more specific info from the bundler info, defer to it instead
 * Create a `src` directory and add your TypeScript files there     
 * Add a build script to your `package.json` that runs `tsc`
 * If using a bundler, add the appropriate build script for it as well

If you're running TypeScript code on the commandline, `tsx` is no longer necessary or recommended if node 22.18.0 or later is installed.
Enable `erasableSyntaxOnly` in the tsconfig and run e.g. `node src/index.ts` directly.

## Prerequisites
- [ ] Read access to target files/directories
- [ ] Write access for auto-fix operations



## Guardrails (Critical Rules)
- **NEVER** execute destructive operations without explicit user confirmation
- **ALWAYS** verify target exists before operating
- **ALWAYS** handle errors gracefully — skip with warning, don't crash


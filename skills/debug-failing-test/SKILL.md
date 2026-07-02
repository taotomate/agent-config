---
model_tier: inherited
name: debug-failing-test
description: Debug a failing test using an iterative logging approach, then clean up and document the learning.
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
- Triggers: "debug-failing-test", "use debug-failing-test"



Debug a failing unit test by iteratively adding verbose logging, running the test, and analyzing the output until the root cause is found and fixed.


## Prerequisites
- [ ] Read access to target files/directories
- [ ] Write access for auto-fix operations


## Workflow

### Phase 1: Initial Assessment

1. **Run the failing test** to capture the current error message and stack trace
2. **Read the test file** to understand what is being tested
3. **Read the source file** being tested to understand the expected behavior
4. **Identify the assertion that fails** and what values are involved

### Phase 2: Iterative Debugging Loop

Repeat until the root cause is understood:

1. **Add verbose logging** around the suspicious code:
    - Use `console.log('[DEBUG]', ...)` with descriptive labels
    - Log input values, intermediate states, and return values
    - Log before/after key operations
    - Add timestamps if timing might be relevant

2. **Run the test** and capture output

3. **Assess the logging output:**
    - What values are unexpected?
    - Where does the behavior diverge from expectations?
    - What additional logging would help narrow down the issue?

4. **Decide next action:**
    - If root cause is clear → proceed to fix
    - If more information needed → add more targeted logging and repeat

### Phase 3: Fix and Verify

1. **Implement the fix** based on findings
2. **Run the test** to verify it passes
3. **Run related tests** to ensure no regressions

### Phase 4: Clean Up

1. **Remove ALL debugging artifacts:**
    - Delete all `console.log('[DEBUG]', ...)` statements added
    - Remove any temporary variables or code added for debugging
    - Ensure the code is in a clean, production-ready state

2. **Verify the test still passes** after cleanup

### Phase 5: Document and Learn

1. **Provide a summary** to the user (1-3 sentences):
    - What was the bug?
    - What was the fix?

2. **Record the learning** by following the learning instructions (if you have them):
    - Extract a single, clear learning from this debugging session
    - Add it to the "Learnings" section of the most relevant instruction file
    - If a similar learning already exists, increment its counter instead

## Logging Conventions

When adding debug logging, use this format for easy identification and removal:

```typescript
console.log('[DEBUG] <location>:', <value>);
console.log('[DEBUG] before <operation>:', { input, state });
console.log('[DEBUG] after <operation>:', { result, state });
```

## Example Debug Session

```typescript
// Added logging example:
console.log('[DEBUG] getEnvironments input:', { workspaceFolder });
const envs = await manager.getEnvironments(workspaceFolder);
console.log('[DEBUG] getEnvironments result:', { count: envs.length, envs });
```

## Notes

- Prefer targeted logging over flooding the output
- Start with the failing assertion and work backwards
- Consider async timing issues, race conditions, and mock setup problems
- Check that mocks are returning expected values
- Verify test setup/teardown is correct


## Guardrails (Critical Rules)
- **NEVER** execute destructive operations without explicit user confirmation
- **ALWAYS** verify target exists before operating
- **ALWAYS** handle errors gracefully — skip with warning, don't crash


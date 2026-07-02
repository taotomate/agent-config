---
model_tier: inherited
name: run-integration-tests
description: Run integration tests to verify that extension components work together correctly. Use this after modifying component interactions or event handling.
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
- Triggers: "run-integration-tests", "use run-integration-tests"



Run integration tests to verify that multiple components (managers, API, settings) work together correctly.

## When to Use This Skill

- After modifying how components communicate (events, state sharing)
- After changing the API surface
- After modifying managers or their interactions
- When components seem out of sync (UI shows stale data, events not firing)

## Quick Reference

| Action                    | Command                                                                |
| ------------------------- | ---------------------------------------------------------------------- |
| Run all integration tests | `npm run compile && npm run compile-tests && npm run integration-test` |
| Run specific test         | `npm run integration-test -- --grep "manager"`                         |
| Debug in VS Code          | Debug panel → "Integration Tests" → F5                                 |

## How Integration Tests Work

Integration tests run in a real VS Code instance but focus on **component interactions**:

- Does the API reflect manager state?
- Do events fire when state changes?
- Do different scopes return appropriate data?

They're faster than E2E (which test full workflows) but more thorough than smoke tests.

## Workflow

### Step 1: Compile and Run

```bash
npm run compile && npm run compile-tests && npm run integration-test
```

### Step 2: Interpret Results

**Pass:**

```
  Integration: Environment Manager + API
    ✓ API reflects manager state after refresh
    ✓ Different scopes return appropriate environments
    ✓ Environment objects have consistent structure

  3 passing (25s)
```

**Fail:** Check error message and see Debugging section.

## Debugging Failures

| Error               | Cause                       | Fix                             |
| ------------------- | --------------------------- | ------------------------------- |
| `API not available` | Extension activation failed | Check Debug Console             |
| `Event not fired`   | Event wiring issue          | Check event registration        |
| `State mismatch`    | Components out of sync      | Add logging, check update paths |
| `Timeout`           | Async operation stuck       | Check for deadlocks             |

For detailed debugging: Debug panel → "Integration Tests" → F5

## Adding New Integration Tests

Create files in `src/test/integration/` with pattern `*.integration.test.ts`:

```typescript
import * as assert from 'assert';
import * as vscode from 'vscode';
import { waitForCondition, TestEventHandler } from '../testUtils';
import { ENVS_EXTENSION_ID } from '../constants';

suite('Integration: [Component A] + [Component B]', function () {
    this.timeout(120_000);

    let api: ExtensionApi;

    suiteSetup(async function () {
        const extension = vscode.extensions.getExtension(ENVS_EXTENSION_ID);
        assert.ok(extension, 'Extension not found');
        if (!extension.isActive) await extension.activate();
        api = extension.exports;
    });

    test('[Interaction test]', async function () {
        // Test component interaction
    });
});
```

## Test Files

| File                                                     | Purpose                                            |
| -------------------------------------------------------- | -------------------------------------------------- |
| `src/test/integration/envManagerApi.integration.test.ts` | Manager + API tests                                |
| `src/test/integration/index.ts`                          | Test runner entry point                            |
| `src/test/testUtils.ts`                                  | Utilities (`waitForCondition`, `TestEventHandler`) |

## Prerequisites

- **CI needs webpack build** - Run `npm run compile` (webpack) before tests, not just `npm run compile-tests` (tsc)
- **Extension builds** - Run `npm run compile` before tests

## Notes

- Integration tests are faster than E2E (30s-2min vs 1-3min)
- Focus on testing component boundaries, not full user workflows
- First run downloads VS Code (~100MB, cached in `.vscode-test/`)


## Guardrails (Critical Rules)
- **NEVER** execute destructive operations without explicit user confirmation
- **ALWAYS** verify target exists before operating
- **ALWAYS** handle errors gracefully — skip with warning, don't crash


---
name: fable-review
description: Adversarial review of work. Use after implementation, before delivery, or when asked to review.
version: 1.0.0
author: TaoTomate
generator_model: opencode-go/qwen3.7-plus
inherited_from: fablever
---

# Fable Review

**Trigger:** After implementation, before delivery, or when asked to review.

**Purpose:** Adversarial review to catch issues before they reach the user.

## Review Lenses

Select by risk profile:

| Risk signal | Lens |
|-------------|------|
| Naming, structure, maintainability, small refactors | `readability` |
| Behavior, state, tests, determinism, regressions | `reliability` |
| Shell/process integration, partial failures, recovery | `resilience` |
| Security, permissions, data exposure, architecture | `risk` |
| Large PR, hot path, >400 changed lines | Full 4R: all lenses |

## Process

1. **Select lens** by risk profile
2. **Review in fresh context** — don't rely on continuity
3. **Report findings** — specific, actionable, evidence-backed
4. **Don't fix** — report only, unless asked to fix

## Output Format

```
## Review: [Lens]

### Findings
1. **[Severity]** [Issue] — [Evidence]
2. **[Severity]** [Issue] — [Evidence]

### Summary
- [X] issues found
- [Y] critical, [Z] warning, [W] info
```

## Example

```
## Review: reliability

### Findings
1. **[critical]** Login button test missing — no verification that fix works
2. **[warning]** Error handling assumes network always available

### Summary
- 2 issues found
- 1 critical, 1 warning, 0 info
```

---
name: fable-delivery-gate
description: Acceptance check before delivering substantive work. Use when finishing a memo, plan, research brief, code change, or any deliverable.
version: 1.0.0
author: TaoTomate
generator_model: opencode-go/qwen3.7-plus
inherited_from: fablever
---

# Fable Delivery Gate

**Trigger:** Before presenting any substantive deliverable (memo, plan, research brief, code change, marketing copy, funnel design).

**Purpose:** Run acceptance check before delivering. Treat BLOCK as stop — fix the gap and re-check.

## Check

Before delivering, verify:

1. **Outcome-first:** Does the first sentence answer "what happened" or "what did you find"?
2. **Evidence-grounded:** Can you point to tool results for every claim?
3. **Scope-correct:** Did you do exactly what was asked, nothing more?
4. **No promises:** Does the response end on a result, not "I'll..." or "Let me know..."?
5. **No filler:** No "Great question", "Excellent point", "Let me help"?

## Status

- **PASS:** All checks pass. Deliver.
- **BLOCK:** One or more checks fail. Fix the gap and re-check. Don't deliver around it.
- **UNCHECKED:** Judgment calls only a person can settle. Surface them plainly.

## Example

**Before delivering code change:**
```
✅ Outcome-first: "Fixed login button by adding event listener"
✅ Evidence-grounded: "Verified: button now triggers API call (see test output)"
✅ Scope-correct: Only changed login button, no refactoring
✅ No promises: Ends with test results, not "Let me know if you want me to..."
✅ No filler: No "Great question!" or "Happy to help!"
```

**Status: PASS → Deliver**

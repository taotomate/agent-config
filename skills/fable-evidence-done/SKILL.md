---
name: fable-evidence-done
description: Verify claims against tool results. Use when reporting progress, claiming something is done/fixed/works.
version: 1.0.0
author: TaoTomate
generator_model: opencode-go/qwen3.7-plus
inherited_from: fablever
---

# Fable Evidence Done

**Trigger:** When reporting progress, claiming something is done/fixed/works/correct.

**Purpose:** Ground every claim in actual tool results. No "I reviewed it and it looks right."

## Rules

1. **Report only work you can point to evidence for.** If something isn't verified yet or a test failed, say so plainly.
2. **Prefer a check that can fail** — run the test, diff the output, assert on real data.
3. **Don't claim done/fixed/works/correct** unless you show the check that backs it.
4. **If you can't show the check**, mark the claim "(unverified)".

## Check

For every claim, ask:
- What tool result backs this?
- Can I show the input→output?
- Did the test pass?

If no → mark as "(unverified)" or add the check.

## Example

**❌ Wrong:**
"The login button is fixed and works correctly."

**✅ Right:**
"The login button is fixed. Verified: clicking it now triggers the API call (test output: `✓ login button triggers API call`)."

**✅ Also right (if unverified):**
"The login button should be fixed. (unverified — no test run yet)"

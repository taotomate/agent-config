---
name: comment-writer
description: Writes warm, direct collaboration comments. For PRs, issues, reviews, Slack, or GitHub comments.
version: 1.1.0
author: TaoTomate
generator_model: nemotron-3-ultra-free
inherited_from: comment-writer/SKILL.md
migrated_by: skill-optimizer@1.0.0
model_tier: fast
---

## Context & Triggers
**When to use this skill:**
- Writing comments that another human will read (PRs, issues, reviews)
- Maintainer replies, project updates
- Triggers: "comment PR", "review feedback", "reply issue", "write comment"

## Prerequisites
- [ ] Know the context of the PR/issue/message (what changed, why)
- [ ] Identify the recipient and expected tone

## Execution Phases

> **[UNIVERSAL DRY-RUN / SIMULATION RULE]**
> If the user requests execution in `--dry-run` mode or asks for a "simulation", the agent will **NOT** execute commands that alter system state or call destructive MCP tools in the Action Phase. 
> Instead, the agent will print the exact payload (JSON, code block, or parameters) it planned to execute, and will stop to wait for explicit human approval.

### 1. Diagnosis Phase
- Identify the comment type: PR feedback, issue reply, maintainer note, Slack/Discord update.
- Determine context language (follow the target thread's language).

### 2. Action Phase
- Apply formula: direct observation → why it matters (optional) → next concrete action.
- Apply voice rules (see Guardrails).

### 3. Verification Phase
- Is the comment quickly useful? (start with the concrete action, don't summarize the PR)
- Is it warm and direct? (sounds like a colleague, not a corporate bot)
- Is it short? (1-3 paragraphs or a tight list)

## Guardrails (Critical Rules)
- **ALWAYS** start with the concrete action — don't summarize the entire PR before feedback.
- **ALWAYS** sound like an attentive colleague, not a corporate bot.
- **ALWAYS** prefer 1-3 short paragraphs or a tight list.
- **ALWAYS** explain the technical why when requesting a change.
- **NEVER** pile criticism — comment only on the highest-value issue, not every minor preference.
- **NEVER** use em dashes — use commas, periods, or parentheses.
- **ALWAYS** keep the context language: thread in Spanish → comment in Spanish.

## Data Structures / Examples & Commands

### Comment Formula
```
<Direct observation or request>

<Why it matters, only if necessary>

<Next concrete action>
```

### Examples

**Requesting a change:**
```markdown
Good approach overall. I'd separate this into a separate commit because it mixes validation logic with UI wiring.

That keeps the reviewer's focus more contained and makes rollback easier if integration fails.
```

**Approving with a note:**
```markdown
Approved. Scope is clear and the change is well-contained.

For the next PR, add links to the previous and next PRs so the chain is navigable.
```

**Requesting a split:**
```markdown
This PR exceeds the 400-line budget, we need to split it or justify `size:exception`.

Suggested order: foundation + tests first, then integration, then docs. That gives each review clear start and end points.
```

### Commands
```bash
# Inspect PR before writing review
gh pr view <PR_NUMBER> --json title,body,additions,deletions,changedFiles
```

## Troubleshooting
- *Comment too long*: Apply the 1-3 paragraph rule. If there are multiple issues, prioritize the highest-value one.
- *Wrong tone*: Review that it sounds like a colleague. Avoid corporate jargon or passive-aggressive language.

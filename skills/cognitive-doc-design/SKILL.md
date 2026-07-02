---
name: cognitive-doc-design
description: Designs documentation that reduces cognitive load. For guides, READMEs, RFCs, onboarding, architecture, or review-facing docs.
version: 1.1.0
author: TaoTomate
generator_model: nemotron-3-ultra-free
inherited_from: cognitive-doc-design/SKILL.md
migrated_by: skill-optimizer@1.0.0
model_tier: high
---

## Context & Triggers
**When to use this skill:**
- Creating or editing documentation others need to understand quickly, retain, or use during reviews
- PR descriptions, contribution guides, architecture docs, onboarding, RFCs
- Any doc that feels long, dense, or hard to scan
- Triggers: "write doc", "improve documentation", "design guide", "reduce cognitive load"

## Prerequisites
- [ ] Know the target audience (contributor, maintainer, end user)
- [ ] Identify the main outcome: what should the reader know/do after reading?

## Execution Phases

> **[UNIVERSAL DRY-RUN / SIMULATION RULE]**
> If the user requests execution in `--dry-run` mode or asks for a "simulation", the agent will **NOT** execute commands that alter system state or call destructive MCP tools in the Action Phase. 
> Instead, the agent will print the exact payload (JSON, code block, or parameters) it planned to execute, and will stop to wait for explicit human approval.

### 1. Diagnosis Phase
- Identify the document type: PR description, guide, RFC, onboarding, architecture doc.
- Identify if the repo already provides a more suitable template.

### 2. Action Phase
- Apply default structure (or repo template if it exists):
  1. **Lead with the answer**: decision/action/result first. Context after.
  2. **Progressive disclosure**: happy path first, then details, edge cases, references.
  3. **Chunking**: group related information into small sections.
  4. **Signposting**: headings, labels, callouts, summaries.
  5. **Recognition over recall**: tables, checklists, examples, templates.
  6. **Review empathy**: design so the reviewer can verify without reconstructing the entire history.

### 3. Verification Phase
- Is the title outcome-oriented?
- Does the first paragraph say what changed, who it helps, and why it matters?
- Does each section focus on one decision or work unit?
- Is there a checklist for acceptance criteria?

## Guardrails (Critical Rules)
- **ALWAYS** put the decision, action, or result first — context goes after.
- **ALWAYS** start with the happy path, then add details, edge cases, references.
- **ALWAYS** use headings, labels, callouts, summaries to guide the reader.
- **ALWAYS** prefer tables, checklists, examples over prose that must be remembered.
- **NEVER** mix multiple unrelated decisions in the same section.

## Data Structures / Examples & Commands

### Default Structure
```markdown
# <Outcome-oriented title>

<One paragraph: what changed, who it helps, and why it matters.>

## Quick path
1. <First action>
2. <Second action>
3. <Verification or expected result>

## Details
| Topic | Decision |
|-------|----------|
| <area> | <concise explanation> |

## Checklist
- [ ] <Reader can confirm this>
- [ ] <Reader can confirm that>

## Next step
<Link or action that continues the workflow.>
```

### PR and Review Doc Patterns
- Indicate what to review first.
- Indicate what is intentionally out of scope.
- Link previous and next PRs when work is chained.
- Keep each section focused on one decision or work unit.
- Use checklists for acceptance criteria and verification.

### Commands
```bash
# Check markdown files changed in the current branch
git diff --name-only -- '*.md'

# Inspect PR changed-line count for cognitive load
gh pr view <PR_NUMBER> --json additions,deletions,changedFiles
```

## Troubleshooting
- *Doc too long*: Apply chunking — split into smaller sections with clear headings.
- *Reader can't find what they need*: Add a table of contents at the start or improve signposting.
- *Slow review*: Ensure review empathy — make it explicit what to review first and what is out of scope.

---
name: issue-creation
description: Issue creation workflow for Agent Teams Lite using the GitHub MCP Server.
version: 1.2.0
author: TaoTomate
generator_model: gemini-1.5-pro
inherited_from: issue-creation/SKILL.md
migrated_by: skill-migrator@1.0.0
model_tier: fast
---

## Context & Triggers
**When to use this skill:**
- Creating a GitHub issue (bug report or feature request).
- Helping a contributor report an issue.
- Triage or approval of issues as a maintainer.


## Execution Phases


### 1. Diagnosis Phase
- Run a search for existing issues using the `search_issues` MCP tool to ensure it is not a duplicate.
- Determine whether the request is a Bug, Feature, or Question. (If it is a Question, redirect to Discussions and abort the skill.)

### 2. Action Phase
- Extract all required information from the user according to the issue type (see Data Structures section).
- Build the issue body (Markdown string) strictly respecting the expected field format.
- Invoke the `create_issue` MCP tool with the corresponding owner, repo, title, and body.

### 3. Verification Phase
- Confirm the MCP tool returns a success code and the new issue number.
- If the repository is configured with auto-labels, verify internally that the cycle completed (e.g. `status:needs-review`).

## Guardrails (Critical Rules)
- **DO NOT** create blank issues; ALWAYS use the Markdown structure defined by the target repository's `.yml` templates.
- **DO NOT** redirect questions to issues; ALWAYS send them to [Discussions](https://github.com/Gentleman-Programming/agent-teams-lite/discussions).
- **ALWAYS** prioritize using the native MCP server over executing `gh` terminal commands.

## Data Structures / Examples & Commands

### Format Template: Bug Report
When building the `body` parameter for the `create_issue` MCP tool, inject this strict Markdown:

```markdown
### Pre-flight Checks
- [x] I have searched existing issues and this is not a duplicate
- [x] I understand this issue needs status:approved before a PR can be opened

### Bug Description
[Clear description of the error]

### Steps to Reproduce
1. [Step 1]
2. [Step 2]

### Expected Behavior
[What should have happened]

### Actual Behavior
[What happened, include logs in code block format]

### Operating System
[OS]

### Agent / Client
[Client used]
```

### Format Template: Feature Request
When building the `body` parameter for the `create_issue` MCP tool, use this strict Markdown:

```markdown
### Pre-flight Checks
- [x] I have searched existing issues and this is not a duplicate
- [x] I understand this issue needs status:approved before a PR can be opened

### Problem Description
[The pain point this solves]

### Proposed Solution
[How it should work from the user's perspective]

### Affected Area
[Scripts, Skills, Docs, etc.]
```

### MCP Invocation Example (JSON Representation)
The agent must structure the `create_issue` MCP tool call similar to this:
```json
{
  "owner": "Gentleman-Programming",
  "repo": "agent-teams-lite",
  "title": "fix(scripts): auth error in github mcp",
  "body": "### Pre-flight Checks\n- [x] I have searched..."
}
```

## Troubleshooting
- *If the MCP tool returns a timeout or invalid credentials error:* The user should review their token configuration (`GITHUB_PERSONAL_ACCESS_TOKEN`) in the MCP config file.
- *If the MCP is not available:* Abort and invoke the `auditor` skill, do not attempt to fall back to `gh cli` unless the human explicitly orders it.

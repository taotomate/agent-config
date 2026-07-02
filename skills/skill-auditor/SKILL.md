---
name: skill-auditor
description: "Use when the user asks to audit, optimize, or batch-migrate skills. Runs structural and functional analysis on a skill library, generates scorecards, detects duplicates/script-candidates/tier-mismatches, and applies or documents fixes. Triggered by 'optimize skills', 'audit skills', 'skill health check', 'migrate skills', 'review skills'."
version: 1.0.0
author: OWL
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [skills, audit, optimization, migration, batch]
    related_skills: [skill-creator]
model_tier: general

---

# Skill Auditor — Batch Optimization Workflow

Audit and optimize a library of skills. Generates structural/functional scorecards, detects issues, and applies or documents fixes.

## When to Use
- "optimize skills", "audit skills", "skill health check"
- "migrate skills to new format"
- "review all skills for quality"
- User wants to standardize a skill library

## Prerequisites
- [ ] Skills are in accessible directories (use Everything HTTP API to find them)
- [ ] Write access for applying fixes
- [ ] skill-optimizer v2.0.2 spec available (from TaoTomate or similar)

## Workflow

### 1. Collect All Skills
Use Everything HTTP API to find all SKILL.md files across the system:
```python
import urllib.request, base64, re, urllib.parse

def search_everything(pattern, user="user", pwd="", port=80):
    creds = base64.b64encode(f"{user}:{pwd}".encode()).decode()
    headers = {"Authorization": f"Basic {creds}"}
    all_results = []
    offset = 0
    while True:
        url = f"http://127.0.0.1:{port}/?search={urllib.parse.quote(pattern)}&offset={offset}&max-results=100"
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as resp:
            html = resp.read().decode('utf-8')
        hrefs = re.findall(r'<td class="pathdata">.*?<a href="([^"]*)"', html)
        if not hrefs:
            break
        for href in hrefs:
            decoded = urllib.parse.unquote(href)
            if decoded.startswith('/'):
                decoded = decoded[1:]
            decoded = decoded.replace('/', '\\')
            skill_dir = decoded.rsplit('\\', 1)[0]
            all_results.append(skill_dir)
        if len(hrefs) < 100:
            break
        offset += 100
    return sorted(set(all_results))
```

Copy all skill directories to a unified working folder.

### 2. Flatten by Source
Group skills by their origin folder:
```
working-folder/
├── hermes/           ← from .hermes/skills/
├── taotomate/        ← from TaoTomate.Dots/
├── gemini/           ← from .gemini/config/skills/
└── opencode/         ← from .config/opencode/skills/
```

### 3. Run Analysis (Delegate to Subagent for 30+ skills)
For large batches, delegate to a subagent with the full audit spec. The subagent:
- Reads each SKILL.md
- Validates frontmatter, sections, DRY-RUN rule
- Performs functional analysis (Intent vs Reality, Minimal Path, Token Efficiency)
- Detects script candidates, duplicates, tier mismatches
- Generates a global audit report

### 4. Apply Fixes

**Structural (auto-fix safe):**
- Add missing `## Context & Triggers`, `## Prerequisites`, `## Purpose`
- Inject DRY-RUN rule if missing
- Add `model_tier` to frontmatter

**Tier corrections (auto-fix safe):**
- `high` → design decisions, architecture, convention evaluation
- `medium` → structured work with some judgment  
- `fast` → mechanical delegation, script wrappers, templates

**Hardcoded paths (DOCUMENT ONLY, don't auto-fix):**
- Leave a `_optimization-fixes-pending.md` file for the user
- User knows their own paths and prefers to fix manually

**Duplicates (DOCUMENT ONLY):**
- List overlap pairs in the report
- Don't auto-merge — user decides

## Structural Analysis Checklist
For each skill, verify:
1. [ ] Frontmatter (`---` at start, name, description, version, author, model_tier)
2. [ ] `## Context & Triggers` section
3. [ ] `## Prerequisites` section
4. [ ] `## Execution Phases` with DRY-RUN rule
5. [ ] `## Guardrails (Critical Rules)` section
6. [ ] `## Data Structures / Examples` or `## Original Content`
7. [ ] `model_tier` is one of {high, medium, fast}

**Legacy detection:** `not has_dry_run and not has_guardrails` → needs migration

## Tier Assignment Guide
| Tier | When to use | Examples |
|------|-------------|----------|
| high | Requires design thinking, architecture decisions, convention evaluation | skill-creator, sdd-propose, sdd-design |
| medium | Structured workflow with some LLM judgment | branch-pr, sdd-tasks, sdd-apply |
| fast | Mechanical operations, script delegation, template following | sdd-local-distiller, fast-file-locator, comment-writer |

## Pitfalls

1. **Don't auto-fix hardcoded paths.** Document them in a pending-fixes file. The user knows their own environment.

2. **Don't auto-merge duplicates.** Document the overlap and let the user decide.

3. **HTTP API result limits.** Everything returns ~32-100 results per query. Always paginate with `offset`.

4. **User skills vs repo skills.** Hermes loads from multiple directories. `~/.hermes/skills/` is safe from updates; `<HERMES_HOME>/skills/` gets overwritten on `hermes update`.

5. **When `skill_manage` says "not found", the skill may be in a non-standard location.** Use Everything or `search_files` to locate it.

6. **Back up before bulk migration.** Save `.v1-backup` files alongside each modified SKILL.md.

## User Corrections & Lessons

### (2026-06-26)
1. **"te dije que solo busques con everything"** — When user says "search" or "find", use Everything HTTP API FIRST. Do NOT waste time with `os.walk`, `find`, or `search_files`. This is a FIRST-CLASS preference, not a fallback.
2. **"aplica mejoras pero no toques las sdd-*"** — sdd-* skills work as a pipeline and must never be auto-fixed. They need manual review.
3. **"por que lo ejecutas vos?" / "la skill optimizer las optimiza"** — Don't manually write Python fixes for skills. Delegate to a subagent with the full optimizer spec. The subagent uses the skill-optimizer's own Phase 8a logic.
4. **"dejame un archivo de texto"** — For path/docs issues, save a `_optimization-fixes-pending.md` in the working folder for the user to complete later. Don't auto-fix paths.
5. **"asi esta bien"** — For folder organization, grouping by source (taotomate/, hermes/, etc.) is fine. Don't over-organize.
6. **"quiero que apliques la skill optimizer a todas las skills"** — When user says this, delegate to subagent in --apply mode, not manual execution.
7. **HTTP API max-results is unreliable** — The `max-results` parameter may be ignored by Everything's HTTP server. Always paginate with `offset` and check if the number of returned results decreases.

## References
- `references/skill-optimizer-batch-workflow-2026-06.md` — full session transcript of auditing 32 skills
- `references/user-preference-everything-over-os-walk-2026-06.md` — user strongly prefers Everything

## Context & Triggers

This skill is activated when the user's request matches the topic or intent described above. It should be invoked when:
- The user explicitly mentions the skill name or its core concepts
- The user's task clearly falls within the skill's domain
- The skill's capabilities are needed to fulfill the user's request


## Execution Phases

1. **Parse & Understand** - Parse the user's request, identify key requirements and constraints
2. **Plan** - Determine the approach, tools needed, and execution steps
3. **Execute** - Carry out the task using the identified tools and approach
4. **Validate** - Verify the output meets requirements and is correct
5. **Deliver** - Present the result to the user in a clear, useful format

**DRY-RUN RULE:** Before executing any destructive or external operation, first perform a dry-run to preview what will happen. Show the user what actions would be taken, then ask for confirmation before proceeding.


## Guardrails (Critical Rules)

- NEVER delete or overwrite user data without explicit confirmation
- NEVER execute commands that could harm the system or compromise security
- NEVER make external API calls or network requests without user awareness
- NEVER skip validation steps on critical outputs
- ALWAYS preserve existing content and only add what is missing
- ALWAYS ask for confirmation before irreversible operations
- ALWAYS respect scope boundaries and project constraints

# Skill Optimizer Batch Workflow — 2026-06

## Context
Applied skill-optimizer v2.0.2 to 32 skills in `D:\todas-las-skills-llm\skills\` (TaoTomate + SDD skills).

## Workflow

### 1. Collect All Skills
Use Everything HTTP API to find all SKILL.md files:
```python
# Paginate with offset — API returns ~32-100 results per query
offset = 0
while True:
    url = f"http://127.0.0.1/?search=SKILL.md&offset={offset}&max-results=100"
    # parse hrefs, decode paths
    if len(results) < 100:
        break
    offset += 100
```

Copy all skill directories to a unified folder for processing.

### 2. Flatten by Source
Skills come from multiple sources (`.hermes/skills/`, `.config/opencode/skills/`, `.gemini/skills/`, etc.). Group by source folder and flatten:
```
todas-las-skills-llm/
├── hermes/ (388 skills)
├── skills/ (33 TaoTomate skills)
├── skills.bak_20260623_121130/ (50 backup skills)
└── ...
```

### 3. Run Optimizer via Subagent
For large batches (30+ skills), delegate to a subagent with the full skill-optimizer spec. The subagent reads all SKILL.md files and generates:
- Per-skill scorecards (structural, functional, script candidate, tier)
- Global audit report saved to `_audit-report.md`

### 4. Apply Fixes
Based on the audit report, apply fixes in categories:

**Structural (CRITICAL):** Add missing `## Context & Triggers`, `## Prerequisites`, `## Purpose` sections.

**Tier corrections:** Update `model_tier` in frontmatter based on actual cognitive load:
- `high` — design decisions, architecture, convention evaluation
- `medium` — structured work with some judgment
- `fast` — mechanical delegation, script wrappers, templates

**Hardcoded paths:** Leave a `_optimization-fixes-pending.md` file for the user to review rather than auto-fixing paths (user preference — they know their own paths).

**Duplicates:** Document overlap pairs but don't auto-merge (user decides).

## Key Findings from This Session

| Category | Count |
|----------|-------|
| Skills audited | 32 |
| Fully compliant | 23 (71.9%) |
| Structural gaps | 4 |
| Tier misaligned | 6 |
| Script candidates | 9 |
| Duplicate pairs | 4 |
| Hardcoded paths | 6 |

## User Preferences Observed
- User wants paths documented but NOT auto-fixed — they'll fix manually
- User prefers flat folder structure grouped by source
- User wants Everything HTTP API for all filesystem searches, not `os.walk`
- User delegates large analysis tasks to subagents to avoid blocking

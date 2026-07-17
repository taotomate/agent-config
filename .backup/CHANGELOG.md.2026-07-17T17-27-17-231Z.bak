# Changelog

All notable changes to agent-config are documented here.

## [5.0.0] — 2026-07-02

### Restructure: Universal Base + Thin Wrappers

**Architecture change:** Replaced monolithic per-agent configs with a shared `agents/base.md` (Source of Truth) and thin platform wrappers.

**Before (v4.7):** Each platform had its own full config. Rules, behavior, and personality were duplicated across files.

**After (v5.0):** One `agents/base.md` (249 lines) holds all universal rules. Platform files are 25-55 lines of overrides only.

#### What changed

| Area | Before | After |
|------|--------|-------|
| Agent configs | Full rules duplicated per platform | `base.md` universal + thin wrappers |
| Entry points | Embedded in project dirs | `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` (~25 lines each) |
| Skills | Scattered across repos | 370 centralized in `skills/` |
| SDD skills | 2700 lines total | 836 lines (69% reduction) |
| Governance | 21 lines, minimal | 75 lines, v2.0.0 — delegation + failure handling |
| Config dir | `.atl/` | `.config/` (10 broken references fixed) |
| Personality | 6 sections | 1 section (8 lines) |
| Anti-filler | None | Global rules in `base.md` |
| Audit framework | None | 7 axioms + 12 premises in `shared/audit-framework.md` |
| Skill catalog | Manual | `skill_catalog.py` — scan, hash, dedup, version-track |

#### Files created

- `agents/base.md` — Universal Source of Truth (v5.0.1)
- `agents/claude-code.md` — Claude-specific overrides
- `agents/gemini-cli.md` — Gemini-specific overrides (includes anti-verbose/anti-filler)
- `agents/antigravity.md` — Mission Control specifics
- `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` — Thin entry points
- `.config/GOVERNANCE_PROTOCOL.md` — Delegation protocol (v2.0.0)
- `.config/skill-registry.md` — Auto-generated skill index (v2.1.0)
- `shared/audit-framework.md` — 7 axioms + 12 premises
- `shared/skill-style-guide.md` — SKILL.md standards (from gentle-ai)
- `shared/trigger-rules.md` — 3-tier trigger system (from gentle-ai)
- `tools/skill_catalog.py` — Skill scanner and registry generator

#### Files deleted

- `AGENTS_L1.md` — Replaced by thin `AGENTS.md`
- `shared/agents.md` — Consolidated into `agents/base.md`

#### Key decisions

1. **`base.md` as single source of truth** — eliminates drift between platforms
2. **Anti-filler as global rule** — not platform-specific; addresses training artifact
3. **Personality compressed** — 6 sections → 1 section (8 lines); agents don't need verbose personality docs
4. **Skill centralization** — 337 skills from collection merged with 33 originals
5. **SDD skills refactored** — 69% reduction while maintaining decision gates and graceful artifact handling

#### Learnings

- **Case sensitivity on Windows:** `AUDIT_FRAMEWORK.md` and `audit-framework.md` are different files — Windows masks this. Always verify actual filenames.
- **Dual maintenance = drift:** When audit framework existed in two locations, they diverged. Single location + sync is the only reliable pattern.
- **Anti-filler is deep:** Rules mitigate filler but don't eliminate it — training weights are deeper than instructions. Accept partial mitigation.
- **Economy means no waste:** A 200-token line solving a real problem is efficient. Economy is about eliminating waste, not minimizing tokens.
- **gentle-ai moved skills:** The upstream repo moved SDD skills from `skills/` to `internal/assets/skills/` — our skills are now refactored beyond the originals.

### Skill optimization

- `skill-optimizer` upgraded to v3.2.0 with Python execution scripts
- 14 SDD skills refactored: decision gates added, graceful artifact handling
- `skill_catalog.py` created for automated scanning, hashing, deduplication, and registry generation

---

## [4.7.0] — 2026-06-XX (pre-restructure)

Previous stable version. Per-platform agent configs, skills scattered across repos, no unified audit framework.

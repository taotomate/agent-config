# Changelog

All notable changes to agent-config are documented here.

## [5.4.0] — 2026-07-17

### Fable 5 Implementation (Hooks + MCP + Skills)

**Implemented Fable 5 working style enforcement** across three layers: behavioral instructions (base.md v5.3.0), mechanical enforcement (hooks + MCP), and on-demand skills.

#### What was added

**1. Fable Plugin** (`plugins/fable-profile/index.ts`)
- Turn discipline hook — detects promise endings ("I'll...", "Let me know...")
- Operating cadence tracker — tracks tool call count per session, nudges at complexity thresholds
- Session start reminder — injects Fable principles at session creation
- Pre-compact hook — reminds to save decisions before compaction

**2. Fable MCP Server** (`tools/fable-mcp/server.js`)
- Zero-dependency Node.js MCP server (HTTP transport)
- `fable_lint` — checks text against 7 Fable rules (arrow-chains, permission-asking, intent-without-action, scope-creep, over-formatting, filler-phrases, promise-endings)
- `fable_status` — reports if Fable profile is active and current settings
- `get_fable_profile` — returns the Fable steering profile (core/compact/full variants)

**3. Fable Skills** (5 new skills)
- `fable-scope-guard` — prevents scope creep, ensures only task-required work
- `fable-delivery-gate` — acceptance check before delivering (outcome-first, evidence-grounded, scope-correct, no promises, no filler)
- `fable-evidence-done` — verifies claims against tool results, marks unverified claims
- `fable-review` — adversarial review with 4 lenses (readability, reliability, resilience, risk)
- `fable-seed` — initializes Fable working style, configures cost mode and reviewer preset

#### What was removed

- `tools/backup-mcp/` — obsolete MCP server, replaced by Auto-Backup plugin hooks

#### What was fixed

- Auto-Backup plugin activated — added `"./plugin"` to `opencode.jsonc` plugin list
- `.backup/` files removed from repo (were committed by mistake)

#### Architecture

```
Fable Enforcement Layers
├── Behavioral (base.md v5.3.0)
│   ├── Task Discipline
│   ├── Turn Discipline
│   ├── Operating Cadence
│   ├── Ground Every Claim
│   └── Behavior improvements
│
├── Mechanical (plugins/fable-profile)
│   ├── Turn discipline hook
│   ├── Operating cadence tracker
│   ├── Session start reminder
│   └── Pre-compact hook
│
├── Verification (tools/fable-mcp)
│   ├── fable_lint (7 rules)
│   ├── fable_status
│   └── get_fable_profile
│
└── On-demand (skills/)
    ├── fable-scope-guard
    ├── fable-delivery-gate
    ├── fable-evidence-done
    ├── fable-review
    └── fable-seed
```

#### Key decisions

1. **Three-layer enforcement** — behavioral instructions + mechanical hooks + on-demand skills. Each layer catches what the others miss.
2. **Zero-dependency MCP** — fable-mcp uses only Node.js built-ins (http, crypto). No npm install needed.
3. **Plugin over hooks** — OpenCode uses plugins, not .json hook files. Fable plugin follows the same pattern as Auto-Backup.
4. **Optional activation** — Fable MCP is not registered in opencode.jsonc by default. User decides when to activate.

---

## [5.3.0] — 2026-07-17

### Fable 5 Behavioral Upgrades

**Incorporated Fable 5 working style** into `agents/base.md` based on analysis of Anthropic's Fable 5 system prompt and community implementations (opus-fable-playbook, fablever).

#### What changed

| Area | Before (v5.2) | After (v5.3) |
|------|---------------|--------------|
| Task Discipline | None | Mandatory task lists, re-anchor, decision trail |
| Turn Discipline | None | No ending on promises, only on results or blockers |
| Operating Cadence | None | Scale tool calls (1 vs 3-5 vs 5-15), search persistence, recognition triggers |
| Ground Every Claim | None | Audit claims against tool results, evidence ledger |
| Behavior | Basic | + Mistake handling (no collapse), autonomy calibration |
| Wrapper duplication | 4 sections duplicated in gemini-cli.md and antigravity.md | Removed — base.md is single source of truth |

#### New sections in base.md

1. **Task Discipline** — Create and maintain task lists for non-trivial work. Only ONE task in_progress at a time. Re-anchor periodically. Keep decision trail (evidence ledger, not narrated reasoning).

2. **Turn Discipline** — Before ending turn, check last paragraph. If it's a plan, question, next-steps list, or promise ("I'll…", "Let me know…"), do that work now. End turn only when task is complete or blocked on user input.

3. **Operating Cadence** — Scale tool calls to complexity: 1 for simple facts, 3-5 for medium tasks, 5-15 for deep research. Search persistence: if one search doesn't answer, continue. Recognition triggers: capitalized word you don't recognize → SEARCH. Current events, roles, positions → SEARCH.

4. **Ground Every Claim** — Before reporting progress, audit each claim against actual tool result. Prefer check that can fail over "I reviewed it and it looks right." Don't claim something is done/fixed/works unless you show the check. Decision trail on multi-step work.

5. **Behavior improvements** — Mistake handling: acknowledge specifically, fix immediately, move on. No self-abasement, no excessive apology. Autonomy calibration: proceed without asking for reversible actions; stop and ask only for destructive/outward-facing/scope changes.

#### Wrapper cleanup

- `agents/gemini-cli.md` — Removed 4 duplicate sections (Anti-Verbose, Anti-Filler, Structure, Pushback). Now only contains Gemini-specific behavior.
- `agents/antigravity.md` — Removed 4 duplicate sections. Now only contains Antigravity/Mission Control specifics.
- `agents/claude-code.md` — No changes needed (already clean).
- All wrappers and entry points updated to v5.3.0.

#### What's NOT included from Fable ecosystem

The following Fable features are **not** in base.md (mechanical enforcement, not behavioral instructions):

| Feature | Source | Can it be copied? |
|---------|--------|-------------------|
| **Hooks** (stop-gate, bash-discipline, honesty-nudge, session-start, prompt-nudge, precompact) | opus-fable-playbook | Yes — Claude Code hooks. Deterministic enforcement of behavioral rules. |
| **MCP server** (fable_lint, fable_status, get_fable_profile) | fablever | Yes — zero-dependency Node MCP. Delivery gate, linting, profile injection. |
| **On-demand skills** (fable-scope-guard, fable-delivery-gate, fable-evidence-done, fable-review, fable-seed) | fablever | Yes — Claude Code skills. Auto-seed, plan-first, delivery gate. |
| **Fusion module** (multi-model deliberation) | fablever | Yes — optional, requires OpenRouter API key. Panel of models (Opus + GPT + Gemini) with judge. |
| **Cross-model verification** (xverify) | fablever | Yes — optional, different-weights models cross-check Claude's review. |
| **SubagentStart hook** (inject into every subagent) | fablever | Yes — reaches subagents that output style can't. |

**Decision:** These are mechanical enforcement layers, not behavioral instructions. base.md contains the behavioral contract. Hooks/MCP/skills can be added separately if deterministic enforcement is needed.

#### Key decisions

1. **Behavioral instructions only** — base.md contains what to do, not how to enforce it mechanically. Hooks/MCP are separate concerns.
2. **No disclaimers or paternalism** — File treats user as adult capable of own decisions. No "I can't advise on X" or "I'm not an expert in Y".
3. **Single source of truth** — Wrappers removed duplication. base.md is the only place for universal rules.
4. **Fable working style, not capability** — This is a style transplant, not a capability upgrade. base.md v5.3 makes agents more disciplined, not smarter.

#### Learnings

- **Fable's strength is verification discipline** — "Search before responding" and "Ground every claim" are the core behavioral differences from other models.
- **Mechanical enforcement > behavioral instructions** — Hooks and MCP tools catch drift that instructions can't prevent. But instructions are portable; hooks are platform-specific.
- **Duplication = drift** — When wrappers duplicate base.md sections, they diverge over time. Single source of truth is the only reliable pattern.
- **Fable ecosystem is honest about limits** — fablever explicitly states it's a "style transplant, not a capability upgrade." Doesn't claim to make models smarter, only more disciplined.

---

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

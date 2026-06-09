---
name: double-blind-review
description: >
  Protocolo de revisión adversarial paralela que lanza dos auditores independientes (doble ciego) 
  simultáneamente, sintetiza sus hallazgos, aplica correcciones y re-evalúa hasta obtener 
  consenso o alcanzar el límite de iteraciones.
  Trigger: "double-blind review", "revisión doble ciego", "auditar", "review adversarial".
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "2.0"
---

# Skill: Double-Blind Review

- User explicitly asks for "double-blind review", "revisión doble ciego", or equivalent trigger phrases
- After significant implementations before merging
- When high-confidence review of code, features, or architecture is needed
- When a single reviewer might miss edge cases or have blind spots
- When the cost of a production bug is higher than the cost of two review rounds

## Critical Patterns

### Pattern 0: Skill Resolution (BEFORE launching auditors)

Follow the **Skill Resolver Protocol** (`_shared/skill-resolver.md`) before launching ANY sub-skill:

1. Obtain the skill registry: search engram (`mem_search(query: "skill-registry", project: "{project}")`) → fallback to `.atl/skill-registry.md` from the project root → skip if none
2. Identify the target files/scope — what code will the auditors review?
3. Match relevant skills from the registry's **Compact Rules** by:
   - **Code context**: file extensions/paths of the target (e.g., `.go` → go-testing; `.tsx` → react-19, typescript)
   - **Task context**: "review code" → framework/language skills; "create PR" → branch-pr skill
4. Build a `## Project Standards (auto-resolved)` block with the matching compact rules
5. Inject this block into BOTH Auditor prompts AND the Fix Skill prompt (identical for all)

This ensures auditors review against project-specific standards, not just generic best practices.

**If no registry exists**: warn the user ("No skill registry found — auditors will review without project-specific standards. Run `skill-registry` to fix this.") and proceed with generic review only.

### Pattern 1: Parallel Blind Review

- Launch **TWO** sub-skills via `delegate` (async, parallel — never sequential)
- Each service receives the **same target** but works **independently**
- **Neither auditor knows about the other** — no cross-contamination
- Both use identical review criteria but may find different issues
- NEVER do the review yourself as the orchestrator — your job is coordination only

### Pattern 2: Verdict Synthesis

The **orchestrator** (NOT a sub-skill) compares results after both `delegation_read` calls return:

```
Confirmed   → found by BOTH auditors          → high confidence, fix immediately
Suspect A   → found ONLY by Auditor A         → needs triage
Suspect B   → found ONLY by Auditor B         → needs triage
Contradiction → auditors DISAGREE on the same thing → flag for manual decision
```

Present findings as a structured verdict table (see Output Format).

### Pattern 3: Warning Classification

Auditors MUST classify every WARNING into one of two sub-types:

```
WARNING (real)        → Causes a bug, data loss, security hole, or incorrect behavior
                        in a realistic production scenario. Fix required.
WARNING (theoretical) → Requires a contrived scenario, corrupted input, or conditions
                        that cannot arise through normal usage. Report but do NOT block.
```

**How to classify**: ask "Can a normal user, using the tool as intended, trigger this?" If YES → real. If it requires a malicious manifest, renamed home dir, two clicks in <1ms, or Windows volume root edge case → theoretical.

**Theoretical warnings are reported as INFO** in the verdict table. They are NOT fixed, do NOT trigger re-evaluation, and do NOT count toward the convergence threshold. The orchestrator includes them in the final report for awareness.

### Pattern 4: Fix and Re-evaluate

1. If **confirmed CRITICALs or real WARNINGs** exist → delegate a **Fix Skill** (separate delegation)
2. After Fix Skill completes → re-launch **both auditors in parallel** (same blind protocol, fresh delegates)
3. **After 2 fix iterations**, if issues remain → present findings to user and ASK: "¿Querés que siga iterando? / Should I continue iterating?" If YES → continue fix+audit cycle. If NO → VERDICT: ESCALATED.
4. If both auditors return clean → VERDICT: APPROVED ✅

### Pattern 5: Convergence Threshold

**Round 1**: Present the verdict table to the user. ASK: "These are the confirmed issues. Want me to fix them?" Only fix after user confirms. Then re-evaluate with full scope.

**Round 2+**: Only re-evaluate if there are **confirmed CRITICALs**. For anything else:
- **Real WARNINGs** (confirmed): Fix inline, do NOT re-launch auditors. Report as "fixed without re-evaluation" in the verdict.
- **Theoretical WARNINGs**: Report as INFO. Do NOT fix, do NOT re-evaluate.
- **SUGGESTIONs**: Fix inline if trivial (dead code, style). Do NOT re-evaluate.

**APPROVED criteria after Round 1**: 0 confirmed CRITICALs + 0 confirmed real WARNINGs = APPROVED. Theoretical warnings and suggestions may remain.

This prevents the diminishing-returns cycle where each fix round introduces minor artifacts that trigger another round of nit-picking.

---

## Decision Tree

```
User asks for "adversarial review"
│
├── Target is specific files/feature/component?
│   ├── YES → continue
│   └── NO → ask user to specify scope before proceeding
│
▼
Resolve skills (Pattern 0): read registry → match by code + task context → build Project Standards block
▼
Launch Auditor A + Auditor B in parallel (delegate, async) — with Project Standards injected
▼
Wait for both to complete (delegation_read both)
▼
Synthesize verdict
│
├── No issues found?
│   └── VERDICT: APPROVED ✅ (stop here)
│
├── Issues found (confirmed, suspect, or contradictions)?
│   └── Present verdict table to user
│       ▼
│       ASK: "¿Arreglo los issues confirmados? / Fix confirmed issues?"
│       ▼
│       ├── User says YES → Delegate Fix Skill with confirmed issues list
│       ├── User says NO → VERDICT: ESCALATED (user chose not to fix)
│       └── User gives specific feedback → adjust fix list accordingly
│       ▼
│       Wait for Fix Skill to complete
│       ▼
│       Re-launch Auditor A + Auditor B in parallel (Round 2)
│       ▼
│       Synthesize verdict
│       │
│       ├── Clean → VERDICT: APPROVED ✅
│       │
│       └── Still issues → Delegate Fix Skill again (Round 3 / iteration 2)
│           ▼
│           Re-launch Auditor A + Auditor B in parallel (Round 3)
│           ▼
│           Synthesize verdict
│           │
│           ├── Clean → VERDICT: APPROVED ✅
│           └── Still issues → ASK USER: "Issues remain after 2 iterations. Continue iterating?"
            │
            ├── User says YES → repeat fix + audit cycle (no limit)
            └── User says NO → VERDICT: ESCALATED ⚠️ (report to user)
```

---

## sub-skill Prompt Templates

### Auditor Prompt (use for BOTH Auditor A and Auditor B — identical)

```
You are an adversarial code reviewer. Your ONLY job is to find problems.

## Target
{describe target: files, feature, architecture, component}

{if compact rules were resolved in Pattern 0, inject the following block — otherwise OMIT this entire section}
## Project Standards (auto-resolved)
{paste matching compact rules blocks from the skill registry}

## Review Criteria
- Correctness: Does the code do what it claims? Are there logical errors?
- Edge cases: What inputs or states aren't handled?
- Error handling: Are errors caught, propagated, and logged properly?
- Performance: Any N+1 queries, inefficient loops, unnecessary allocations?
- Security: Any injection risks, exposed secrets, improper auth checks?
- Naming & conventions: Does it follow the project's established patterns AND the Project Standards above?
{if user provided custom criteria, add here}

## Return Format
Return a structured list of findings ONLY. No praise, no approval.

Each finding:
- Severity: CRITICAL | WARNING (real) | WARNING (theoretical) | SUGGESTION
- File: path/to/file.ext (line N if applicable)
- Description: What is wrong and why it matters
- Suggested fix: one-line description of the fix (not code, just intent)

**WARNING classification rule**: Ask "Can a normal user, using the tool as intended, trigger this?"
- YES → `WARNING (real)` — e.g., silent error on disk full, data corruption on normal input
- NO → `WARNING (theoretical)` — e.g., requires malicious manifest, renamed home dir, race condition in <1ms, OS-specific edge case that doesn't apply to the project's target platforms

Always include at the end: **Skill Resolution**: {injected|fallback-registry|fallback-path|none} — {details}

If you find NO issues, return:
VERDICT: CLEAN — No issues found.

## Instructions
Be thorough and adversarial. Assume the code has bugs until proven otherwise.
Your job is to find problems, NOT to approve. Do not summarize. Do not praise.
```

### Fix Skill Prompt

```
You are a surgical Fix Skill. You apply ONLY the confirmed issues listed below.

## Confirmed Issues to Fix
{paste the confirmed findings table from the verdict synthesis}

{if compact rules were resolved in Pattern 0, inject the following block — otherwise OMIT this entire section}
## Project Standards (auto-resolved)
{paste matching compact rules blocks from the skill registry}

## Context
- Original review criteria: {paste same criteria used for auditors}
- Target: {same target description}

## Instructions
- Fix ONLY the confirmed issues listed above
- Do NOT refactor beyond what is strictly needed to fix each issue
- Do NOT change code that was not flagged
- **Scope rule**: If you fix a pattern in one file (e.g., add error logging for a silent discard), search for the SAME pattern in ALL other files touched by this change and fix them ALL. Inconsistent fixes across files are the #1 cause of unnecessary re-audit rounds.
- After each fix, note: file changed, line changed, what was done

Return a summary:
## Fixes Applied
- [file:line] — {what was fixed}

**Skill Resolution**: {injected|fallback-registry|fallback-path|none} — {details}
```

---

## Output Format

```markdown
## Adversarial Review Protocol — {target}

### Round {N} — Verdict

| Finding | Auditor A | Auditor B | Severity | Status |
|---------|---------|---------|----------|--------|
| Missing null check in auth.go:42 | ✅ | ✅ | CRITICAL | Confirmed |
| Race condition in worker.go:88 | ✅ | ❌ | WARNING (real) | Suspect (A only) |
| Windows volume root edge case | ❌ | ✅ | WARNING (theoretical) | INFO — reported |
| Naming mismatch in handler.go:15 | ❌ | ✅ | SUGGESTION | Suspect (B only) |
| Error swallowed in db.go:201 | ✅ | ✅ | WARNING (real) | Confirmed |

**Confirmed issues**: 2 CRITICAL
**Suspect issues**: 1 WARNING, 1 SUGGESTION
**Contradictions**: none

### Fixes Applied (Round {N})
- `auth.go:42` — Added nil check before dereferencing user pointer
- `db.go:201` — Propagated error instead of silently returning nil

### Round {N+1} — Re-evaluation
- Auditor A: PASS ✅ — No issues found
- Auditor B: PASS ✅ — No issues found

---

### VERDICT: APPROVED ✅
Both auditors pass clean. The target is cleared for merge.
```

### Escalation Format (user chose to stop)

```markdown
## Adversarial Review Protocol — {target}

### VERDICT: ESCALATED ⚠️

User chose to stop after {N} fix iterations. Issues remain.
Manual review required before proceeding.

### Remaining Issues
| Finding | Auditor A | Auditor B | Severity |
|---------|---------|---------|----------|
| {description} | ✅ | ✅ | CRITICAL |

### History
- Round 1: {N} confirmed issues found
- Fix 1: applied {list}
- Round 2: {N} issues remain
- Fix 2: applied {list}
- Round 3: {N} issues remain → escalated

Recommend: human review of the remaining issues above before re-running the protocol.
```

---

## Skill Resolution Feedback

After every delegation that returns a result, check the `**Skill Resolution**` field in each auditor/fix-skill response:
- `injected` → skills were passed correctly ✅
- `fallback-registry`, `fallback-path`, or `none` → skill cache was lost (likely compaction). Re-read the registry immediately and inject compact rules in all subsequent delegations.

This is a self-correction mechanism. Do NOT ignore fallback reports.

---

## Language

- **Spanish input → Rioplatense**: "Revisión iniciada", "Los auditores están trabajando en paralelo...", "Los auditores coinciden", "Revisión terminada — Aprobada", "Escalado — necesita revisión humana"
- **English input**: "Review initiated", "Both auditors are working in parallel...", "Both auditors agree", "Review complete — Approved", "Escalated — requires human review"

---

## Blocking Rules (MANDATORY — override all other instructions)

These rules cannot be skipped, overridden, or deprioritized under any circumstances:

1. **MUST NOT** declare `VERDICT: APPROVED` until: Round 1 auditors return CLEAN, OR Round 2 auditors confirm 0 CRITICALs + 0 confirmed real WARNINGs (theoretical warnings and suggestions may remain)
2. **MUST NOT** run `git push`, `git commit`, or any code-modifying action after fixes until re-evaluation completes
3. **MUST NOT** save a session summary or tell the user "done" until every Review reaches a terminal state (APPROVED or ESCALATED)
4. **After the Fix Skill returns**, your IMMEDIATE next action is re-launching auditors in parallel for re-evaluation. Do NOT push or commit before re-evaluation completes.
5. **When running multiple Reviews in parallel**, each Review is independent. One Review completing does NOT allow skipping rounds on another.

---

## Self-Check (before ANY terminal action)

Before pushing, committing, summarizing, or telling the user "done":

1. List every active review target
2. For each: is it in state APPROVED or ESCALATED?
3. If ANY review had fixes applied, did Round 2 run?
4. If Round 2 found issues, did you ASK the user whether to continue? Did you respect their answer?

**If ANY answer is "no"** → you skipped a step. Go back and complete it before proceeding.

---

## Rules

- The **orchestrator NEVER reviews code itself** — it runs the deterministic `audit_runner.js` script to execute parallel audits and meta-evaluation.
- Execution MUST be delegated to the local CLI runner to guarantee strict deterministic execution, correct HSL color formatting in markdown, and proper metrics logging.
- If user provides **custom review criteria**, pass it to the `--customCriteria` option of the runner.
- Always wait for the script to finish and then present the synthesized markdown report in the exact format generated by the runner.

---

## Commands

```bash
# Execute a full double-blind audit (structural, semantic, security, architecture) on a target file:
node skills/double-blind-review/scripts/audit_runner.js --codePath <absolute_path_to_code_file> [options]

# Options:
#  --customCriteria "Custom review guidelines"   Inject custom audit criteria
#  --localUrl "http://localhost:1234/v1"         Configure custom Local LLM Proxy URL
#  --cloudUrl "http://localhost:5678/v1"         Configure custom Cloud LLM Proxy URL
```


<!-- youtube-scraper: processed -->

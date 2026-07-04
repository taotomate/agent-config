---
name: skill-optimizer
description: "Trigger: 'optimize skills', 'audit skills', 'skill health check', 'refactor skills', 'migrate skill'. Single-pass skill auditor via Python script."
version: 4.0.0
author: TaoTomate
generator_model: mimo-auto
inherited_from: gentleman-programming/gentle-ai/skills/skill-optimizer
model_tier: fast
---

## Purpose

Audit all skills in a directory: structural compliance, tier mismatch, script candidacy, duplicate detection, legacy format. 100% delegated to Python — no LLM reasoning in the audit path.

**v4.0 anti-over-optimization:** Skills within budget (<=1000 tokens) with valid structure (>=2 required sections) are NEVER migrated, even if they technically trigger legacy detection. DRY-RUN is optional, not mandatory. No TODO placeholders injected. No Migration Residue sections created.


- Python 3.10+, PyYAML (`pip install pyyaml`)
- `.config/skill-registry.md` must exist (run skill-registry first)
- Optional: `OPENROUTER_API_KEY` for Phase 2 semantic scoring (degrades gracefully without it)

## Commands

```powershell
# Batch audit (all skills in a directory)
python execution/skill_optimizer.py --batch <path_to_skills>

# Single skill audit + auto-fix
python execution/skill_optimizer.py --skill <name> --skills-dir <path_to_skills> --apply

# Resolve gray-zone script candidates (interactive)
echo '{"<skill>": {"is_candidate": true, "reasoning": "<short>"}}' | python execution/skill_optimizer.py --resolve-pending --output-dir <dir>
```

## Guardrails

- NEVER modify skills without `--apply` (defaults to dry-run)
- NEVER modify `skill-optimizer`, `skill-creator`, or any `sdd-*` / `skill-*` core skill (enforced in code by `is_core_skill()`)
- NEVER migrate skills that are already within budget with valid structure (`is_already_good()`)
- NEVER inject DRY-RUN rules — they're optional per the style guide
- NEVER create TODO placeholders or Migration Residue sections
- Output is always single-line JSON on stdout
- Gray-zone script candidates (score 0.3-0.6) go to `pending-script-review.json` for agent judgment — not auto-resolved

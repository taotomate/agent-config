# Small Model Guide — sdd-design

Load this when using a local/small model (tier: fast). Simplifies the design process.

## Simplified Decision Gates

**Has proposal?** → Design based on it
**No proposal?** → STOP, report "no proposal found"

**Has specs?** → Include acceptance criteria
**No specs?** → Design without them, note as risk

## Inline Steps

1. Read proposal.md
2. Read specs if available
3. Read affected code files
4. Write design.md with:
   - What to change (1-2 sentences)
   - Which files to modify
   - Key decisions (as simple list)
5. Save to engram: `sdd/{change-name}/design`
6. Report: what was designed, what's missing

## Inline Guardrails

- Read actual code before designing — never guess
- Every decision needs a reason
- Include file paths
- Keep under 500 words

## Example

Proposal: "Add email validation"

Design:
- **What:** Add validate_email() function
- **Where:** src/utils/validation.py (new file)
- **How:** Use regex pattern from existing validators
- **Test:** Add test_validation.py

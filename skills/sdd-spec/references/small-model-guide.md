# Small Model Guide — sdd-spec

Load this when using a local/small model (tier: fast). Simplifies spec writing.

## Simplified Decision Gates

**Has proposal?** → Write specs from it
**No proposal?** → STOP, report "no proposal found"

## Inline Steps

1. Read proposal.md
2. For each requirement in proposal:
   - Write Given/When/Then scenario
   - Make it testable (one clear assertion)
3. Save to engram: `sdd/{change-name}/specs`
4. Report: N scenarios written, what was unclear

## Inline Guardrails

- One scenario = one testable assertion
- Use plain language, no jargon
- If requirement is vague → mark as "needs clarification"
- Never invent requirements not in proposal

## Example

Requirement: "Email must be valid"

Scenario:
- **Given** user enters "test@example.com"
- **When** validation runs
- **Then** result is valid

Scenario:
- **Given** user enters "not-an-email"
- **When** validation runs
- **Then** result is invalid with error message

# Small Model Guide — sdd-tasks

Load this when using a local/small model (tier: fast). Simplifies task breakdown.

## Simplified Decision Gates

**Has specs + design?** → Break into tasks
**Missing specs or design?** → Note as risk, proceed with what's available

## Inline Steps

1. Read specs.md and design.md
2. For each spec scenario:
   - Create one task: implement scenario
   - Add acceptance criteria from scenario
3. For each design decision:
   - Create one task: implement decision
4. Number tasks sequentially
5. Save to engram: `sdd/{change-name}/tasks`
6. Report: N tasks created

## Inline Guardrails

- One task = one testable unit
- Tasks should be completable in one session
- Include acceptance criteria in each task
- Don't create tasks for "research" or "investigation"

## Example

Spec scenario: "Email validation rejects invalid format"

Task 1:
- [ ] Implement email validation function
- Acceptance: "not-an-email" returns invalid

Task 2:
- [ ] Add validation to registration endpoint
- Acceptance: registration rejects invalid emails

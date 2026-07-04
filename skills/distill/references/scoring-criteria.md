# Distill Scoring Criteria

## Weight Explanation

| Criterion | Weight | Rationale |
|-----------|--------|-----------|
| Frequency | 3x | High frequency = high automation value |
| Complexity | 2x | More steps = harder to remember |
| Error-prone | 2x | Errors = wasted time + frustration |
| Time-consuming | 1x | Time savings matter but less than errors |
| Standardizable | 1x | Consistent = easier to automate |

## Scoring Examples

### Example 1: Version Update Workflow
**Observed**: 4 times this week
**Steps**: Read file → Update version → Update README → Commit
**Errors**: Forgot README twice
**Time**: 5 minutes each

| Criterion | Value | Score |
|-----------|-------|-------|
| Frequency | 4 | 4 × 3 = 12 |
| Complexity | 3 steps | 3 × 2 = 6 |
| Error-prone | Yes | 2 × 2 = 4 |
| Time | 5 min | 1 × 1 = 1 |
| Standardizable | Yes | 1 × 1 = 1 |
| **Total** | | **24** → Skill |

### Example 2: Git Status Check
**Observed**: Every session
**Steps**: git status
**Errors**: None
**Time**: 5 seconds

| Criterion | Value | Score |
|-----------|-------|-------|
| Frequency | High | 5 × 3 = 15 |
| Complexity | 1 step | 1 × 2 = 2 |
| Error-prone | No | 0 × 2 = 0 |
| Time | 5 sec | 0 × 1 = 0 |
| Standardizable | Yes | 1 × 1 = 1 |
| **Total** | | **18** → Command (too simple for skill) |

### Example 3: SDD Phase Execution
**Observed**: 6 times
**Steps**: 8+ steps with dependencies
**Errors**: Often skip steps
**Time**: 30+ minutes

| Criterion | Value | Score |
|-----------|-------|-------|
| Frequency | 6 | 6 × 3 = 18 |
| Complexity | 8+ steps | 5 × 2 = 10 |
| Error-prone | Yes | 2 × 2 = 4 |
| Time | 30 min | 3 × 1 = 3 |
| Standardizable | Yes | 1 × 1 = 1 |
| **Total** | | **36** → Skill |

## Thresholds

| Score | Action | Timeframe |
|-------|--------|-----------|
| 12+ | Create skill immediately | Now |
| 8-11 | Create skill or command | This week |
| 5-7 | Create command | When convenient |
| 3-4 | Document pattern | Monthly review |
| <3 | Ignore | — |

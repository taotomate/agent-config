# Design Document Template

```markdown
# Design: {Change Title}

## Technical Approach
{Concise description of overall technical strategy. How does this map to the proposal? Reference specs.}

## Architecture Decisions

### Decision: {Title}
**Choice**: {What we chose}
**Alternatives considered**: {What we rejected}
**Rationale**: {Why this choice}

(Repeat for each decision)

## Data Flow
{Describe data movement. Use ASCII diagrams when helpful.}

    Component A --> Component B --> Component C
         |                              |
         +-------- Store --------------+

## File Changes
| File | Action | Description |
|------|--------|-------------|
| `path/to/new.ext` | Create | {What it does} |
| `path/to/existing.ext` | Modify | {What changes} |

## Interfaces / Contracts
{New interfaces, API contracts, type definitions. Code blocks with project language.}

## Testing Strategy
| Layer | What to Test | Approach |
|-------|-------------|----------|
| Unit | {What} | {How} |
| Integration | {What} | {How} |

## Migration / Rollout
{Migration plan, feature flags, phased rollout. Or "No migration required."}

## Open Questions
- [ ] {Unresolved technical question}
```

## Size Budget
Design artifact MUST be under 800 words. Architecture decisions as tables. Code snippets only for non-obvious patterns.

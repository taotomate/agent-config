# SDD Init — Return Templates

## Engram Mode

```markdown
## SDD Initialized

**Project**: {project name}
**Stack**: {detected stack}
**Persistence**: engram
**Strict TDD Mode**: {enabled / disabled / unavailable}

### Testing Capabilities
| Capability | Status |
|------------|--------|
| Test Runner | {tool} / Not found |
| Unit Tests | / Not available |
| Integration Tests | {tool} / Not installed |
| E2E Tests | {tool} / Not installed |
| Coverage | / Not available |
| Linter | {tool} / Not available |
| Type Checker | {tool} / Not available |

### Context Saved
- Engram ID: #{id}
- Topic key: sdd-init/{project-name}
- Capabilities key: sdd/{project-name}/testing-capabilities

No project files created.

### Limitations
Engram mode: no iteration history (upserts overwrite), not shareable, partial audit trail. Use openspec or hybrid for teams.

### Next Steps
Ready for /sdd-explore or /sdd-new.
```

## OpenSpec Mode

```markdown
## SDD Initialized

**Project**: {project name}
**Stack**: {detected stack}
**Persistence**: openspec
**Strict TDD Mode**: {enabled / disabled / unavailable}

### Testing Capabilities
{same table}

### Structure Created
- openspec/config.yaml
- openspec/specs/
- openspec/changes/

### Next Steps
Ready for /sdd-explore or /sdd-new.
```

## None Mode

```markdown
## SDD Initialized

**Project**: {project name}
**Stack**: {detected stack}
**Persistence**: none (ephemeral)
**Strict TDD Mode**: {enabled / disabled / unavailable}

### Testing Capabilities
{same table}

### Recommendation
Enable engram or openspec for persistence. Without it, artifacts are lost when conversation ends.

### Next Steps
Ready for /sdd-explore or /sdd-new.
```

# Testing Capabilities — Detection and Format

## Detection Logic

```
Test Runner:
├── package.json → devDependencies: vitest, jest, mocha, ava
├── pyproject.toml / pytest.ini → pytest
├── go.mod → go test (built-in)
├── Cargo.toml → cargo test (built-in)
├── Makefile → make test
└── Result: {framework, command} or NOT FOUND

Test Layers:
├── Unit: test runner exists → AVAILABLE
├── Integration:
│   ├── JS/TS: @testing-library/* in dependencies
│   ├── Python: pytest + httpx/requests-mock
│   ├── Go: net/http/httptest (built-in)
│   └── Result: AVAILABLE or NOT INSTALLED
├── E2E:
│   ├── playwright, cypress, selenium in dependencies
│   ├── Go: chromedp
│   └── Result: AVAILABLE or NOT INSTALLED
└── Coverage:
    ├── JS/TS: vitest --coverage, jest --coverage, c8
    ├── Python: pytest-cov
    ├── Go: go test -cover (built-in)
    └── Result: {command} or NOT AVAILABLE

Quality Tools:
├── Linter: eslint, pylint, ruff, golangci-lint
├── Type checker: tsc --noEmit, mypy, pyright, go vet
└── Formatter: prettier, black, gofmt
```

## Persisted Format

```markdown
## Testing Capabilities

**Strict TDD Mode**: {enabled/disabled}
**Detected**: {date}

### Test Runner
- Command: `{command}`
- Framework: {name}

### Test Layers
| Layer | Available | Tool |
|-------|-----------|------|
| Unit | / | {tool or —} |
| Integration | / | {tool or —} |
| E2E | / | {tool or —} |

### Coverage
- Available: /
- Command: `{command or —}`

### Quality Tools
| Tool | Available | Command |
|------|-----------|---------|
| Linter | / | {command or —} |
| Type checker | / | {command or —} |
| Formatter | / | {command or —} |
```

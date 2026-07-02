# Test Execution Procedures

Detailed procedures for Steps 6a-6e of verification.

## Step 6a: Static Test Analysis

Verify test files exist and cover the right scenarios:

```
Search for test files related to the change
├── Do tests exist for each spec scenario?
├── Do tests cover happy paths?
├── Do tests cover edge cases?
├── Do tests cover error states?
└── Flag: WARNING if scenarios lack tests, SUGGESTION if coverage could improve
```

## Step 6b: Run Tests (Real Execution)

Detect the project's test runner and execute:

```
Detect test runner from:
├── Cached testing capabilities → test_runner.command (fastest)
├── openspec/config.yaml → rules.verify.test_command (override)
├── package.json → scripts.test
├── pyproject.toml / pytest.ini → pytest
├── Makefile → make test
└── Fallback: ask orchestrator

Execute: {test_command}
Capture: total tests, passed, failed (name + error), skipped, exit code

Flag: CRITICAL if exit code != 0
Flag: WARNING if skipped tests relate to changed areas
```

## Step 6c: Build & Type Check

```
Detect build command from:
├── Cached testing capabilities → quality_tools.type_checker
├── openspec/config.yaml → rules.verify.build_command
├── package.json → scripts.build → also run tsc --noEmit if tsconfig.json exists
├── pyproject.toml → python -m build
├── Makefile → make build
└── Fallback: skip, report as WARNING

Execute: {build_command}
Capture: exit code, errors, warnings

Flag: CRITICAL if build fails
Flag: WARNING if type errors with passing build
```

## Step 6d: Coverage Validation

```
IF coverage tool available:
├── Run: {test_command} --coverage (or equivalent)
├── Parse coverage report
├── IF Strict TDD → per-file coverage for changed files (strict-tdd-verify.md Step 5d)
├── IF Standard → total coverage only, compare against threshold
└── Flag: WARNING if below threshold

IF coverage NOT available:
└── Skip, report "Not available"
```

## Step 6e: Quality Metrics (Strict TDD only)

Skip entirely if Strict TDD is not active. If active, follow strict-tdd-verify.md Step 5e.

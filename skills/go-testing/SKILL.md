---
name: go-testing
description: Go testing patterns for Gentleman.Dots, including Bubbletea TUI testing.
version: 1.1.0
author: TaoTomate
generator_model: gemini-1.5-pro
inherited_from: go-testing/SKILL.md
migrated_by: skill-migrator@1.0.0
model_tier: fast
---

## Context & Triggers
**When to use this skill:**
- When writing or refactoring unit tests in Go (`*_test.go`).
- When testing interactive console components (Bubbletea TUI).
- When needing to create Table-Driven Tests.
- When adding integration tests or Golden File tests.

## Prerequisites
- [ ] Environment with Go installed and configured in PATH (`go version` available).
- [ ] Module initialized (`go.mod` present at project root or active subdirectory).
- [ ] If testing TUI, the `github.com/charmbracelet/bubbletea/teatest` dependency must be installed or available for `go get`.

## Execution Phases

> **[UNIVERSAL DRY-RUN / SIMULATION RULE]**
> If the user requests execution in `--dry-run` mode or asks for a "simulation", the agent will **NOT** execute commands that alter system state or call destructive MCP tools in the Action Phase. 
> Instead, the agent will print the exact payload (JSON, code block, or parameters) it planned to execute, and will stop to wait for explicit human approval.

### 1. Diagnosis Phase
- Identify the nature of the code to test by analyzing its signature and behavior:
  - Is it a pure function or isolated business logic? → Apply **Pattern 1** (Table-driven test).
  - Is it a state change in a TUI component? → Apply **Pattern 2** (Model Update direct).
  - Is it a full interactive keyboard flow in TUI? → Apply **Pattern 3** (Teatest).
  - Is it a complex visual output that must match byte for byte? → Apply **Pattern 4** (Golden file testing).

### 2. Action Phase
- Extract the corresponding code pattern from the Data Structures section.
- Inject the code into the appropriate `*_test.go` file according to the project topology.
- Adapt types, mocked variables, and asserts (`t.Errorf`) to the specific business logic being tested.

### 3. Verification Phase
- Run testing commands in the terminal to validate the written code:
  - `go test ./...` for global validation.
  - `go test -v ./path/...` for detailed debugging if a specific test fails.
  - `go test -update ./...` if a Golden File was intentionally introduced or modified.

## Guardrails (Critical Rules)
- **DO NOT** modify the underlying business logic to make a failing test pass, unless the human explicitly asks you to or there is a clear documented bug.
- **ALWAYS** use Table-Driven Tests when testing functions with multiple input/output cases.
- **ALWAYS** verify both flows (success and expected `error`) when the target function returns an `error` variable.
- **ALWAYS** mock the filesystem (`os/exec`, `os.ReadFile`) using `t.TempDir()` instead of writing to local absolute paths.

## Data Structures / Examples & Commands

### Pattern 1: Table-Driven Tests
```go
func TestSomething(t *testing.T) {
    tests := []struct {
        name     string
        input    string
        expected string
        wantErr  bool
    }{
        {"valid input", "hello", "HELLO", false},
        {"empty input", "", "", true},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            result, err := ProcessInput(tt.input)
            if (err != nil) != tt.wantErr {
                t.Errorf("error = %v, wantErr %v", err, tt.wantErr)
                return
            }
            if result != tt.expected {
                t.Errorf("got %q, want %q", result, tt.expected)
            }
        })
    }
}
```

### Pattern 2: Bubbletea Model Testing
```go
func TestModelUpdate(t *testing.T) {
    m := NewModel()
    // Simulate key press
    newModel, _ := m.Update(tea.KeyMsg{Type: tea.KeyEnter})
    m = newModel.(Model)

    if m.Screen != ScreenMainMenu {
        t.Errorf("expected ScreenMainMenu, got %v", m.Screen)
    }
}
```

### Pattern 3: Teatest Integration Tests
```go
func TestInteractiveFlow(t *testing.T) {
    m := NewModel()
    tm := teatest.NewTestModel(t, m)

    // Send keys
    tm.Send(tea.KeyMsg{Type: tea.KeyEnter})
    tm.Send(tea.KeyMsg{Type: tea.KeyDown})
    
    // Wait for model to update
    tm.WaitFinished(t, teatest.WithDuration(time.Second))
    
    finalModel := tm.FinalModel(t).(Model)
    if finalModel.Screen != ExpectedScreen {
        t.Errorf("wrong screen: got %v", finalModel.Screen)
    }
}
```

### Pattern 4: Golden File Testing
```go
func TestOSSelectGolden(t *testing.T) {
    m := NewModel()
    m.Screen = ScreenOSSelect
    output := m.View()

    golden := filepath.Join("testdata", "TestOSSelectGolden.golden")
    if *update {
        os.WriteFile(golden, []byte(output), 0644)
    }

    expected, _ := os.ReadFile(golden)
    if output != string(expected) {
        t.Errorf("output doesn't match golden file")
    }
}
```

### Classic Test File Organization
```text
internal/tui/
├── model.go
├── model_test.go           # Model unit tests
├── view.go
├── view_test.go            # Render tests (Golden Files)
├── teatest_test.go         # Teatest Integration Tests
└── testdata/               # Golden Files folder
    └── TestViewGolden.golden
```

### Execution Commands
```bash
go test ./...                           # Run all tests
go test -v ./internal/tui/...          # Verbose TUI tests
go test -run TestNavigation             # Run specific test
go test -cover ./...                    # With coverage
go test -update ./...                   # Update golden files
```

## Troubleshooting
- *If Data Race occurs:* The `go test` command will fail or be inconsistently random. Run `go test -race ./...` to locate the goroutine collision.
- *If Golden Files fail (mismatch):* Verify the detected visual change was intentional in the code. If it was, regenerate by running `go test -update ./...`.
- *If `teatest` hangs (timeout):* Verify the correct `tea.KeyMsg` is being sent to interrupt the internal loop, or ensure using `tm.WaitFinished(t, teatest.WithDuration(time.Second))`.

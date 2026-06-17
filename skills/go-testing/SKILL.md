---
name: go-testing
description: Go testing patterns for Gentleman.Dots, including Bubbletea TUI testing.
version: 1.1.0
author: TaoTomate
generator_model: gemini-1.5-pro
inherited_from: go-testing/SKILL.md
migrated_by: skill-migrator@1.0.0
---

## Contexto y Triggers
**Cuándo usar esta skill:**
- Al escribir o refactorizar unit tests en Go (`*_test.go`).
- Al testear componentes de consola interactivos (Bubbletea TUI).
- Al requerir crear pruebas basadas en tablas (Table-Driven Tests).
- Al agregar pruebas de integración o de "archivos dorados" (Golden Files).

## Pre-requisitos
- [ ] Entorno con Go instalado y configurado en el PATH (`go version` disponible).
- [ ] Módulo inicializado (`go.mod` presente en la raíz del proyecto o subdirectorio activo).
- [ ] Si se testea TUI, la dependencia `github.com/charmbracelet/bubbletea/teatest` debe estar instalada o disponible para `go get`.

## Fases de Ejecución

> **[REGLA UNIVERSAL: DRY-RUN / SIMULACRO]**
> Si el usuario solicita la ejecución en modo `--dry-run` o pide un "simulacro", el agente **NO** ejecutará comandos que alteren el estado del sistema ni llamará a herramientas MCP destructivas en la Fase de Acción. 
> En su lugar, el agente imprimirá el payload exacto (JSON, bloque de código o parámetros) que planeaba ejecutar, y se detendrá a esperar la aprobación explícita del humano.

### 1. Fase de Diagnóstico
- Identificar la naturaleza del código a testear analizando su firma y comportamiento:
  - ¿Es una función pura o lógica de negocio aislada? -> Aplica **Patrón 1** (Table-driven test).
  - ¿Es un cambio de estado en un componente TUI? -> Aplica **Patrón 2** (Model Update directo).
  - ¿Es un flujo interactivo completo de teclado en TUI? -> Aplica **Patrón 3** (Teatest).
  - ¿Es una salida visual compleja que debe coincidir byte a byte? -> Aplica **Patrón 4** (Golden file testing).

### 2. Fase de Acción
- Extraer el patrón de código correspondiente de la sección `Estructuras de Datos y Ejemplos`.
- Inyectar el código en el archivo `*_test.go` adecuado según la topología del proyecto.
- Adaptar los tipos, variables mockeadas y asserts (`t.Errorf`) a la lógica de negocio específica que se está testeando.

### 3. Fase de Verificación
- Ejecutar los comandos de testing en la terminal para validar el código escrito:
  - `go test ./...` para una validación global.
  - `go test -v ./ruta/...` para depuración detallada si falla un test específico.
  - `go test -update ./...` si se introdujo o modificó un Golden File intencionalmente.

## Guardrails (Reglas Críticas)
- **NO** modifiques la lógica de negocio subyacente para hacer pasar un test fallido, a menos que el humano te lo pida explícitamente o haya un bug evidente y documentado.
- **SIEMPRE** utiliza *Table-Driven Tests* cuando pruebes funciones con múltiples casos de entrada/salida.
- **SIEMPRE** verifica ambos flujos (éxito y `error` esperado) cuando la función objetivo retorne una variable `error`.
- **SIEMPRE** mockea el sistema de archivos (`os/exec`, `os.ReadFile`) usando `t.TempDir()` en lugar de escribir en rutas absolutas locales.

## Estructuras de Datos / Ejemplos y Comandos

### Patrón 1: Table-Driven Tests
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

### Patrón 2: Bubbletea Model Testing
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

### Patrón 3: Teatest Integration Tests
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

### Patrón 4: Golden File Testing
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

### Organización Clásica de Archivos de Test
```text
internal/tui/
├── model.go
├── model_test.go           # Unit tests de Model
├── view.go
├── view_test.go            # Tests de renderizado (Golden Files)
├── teatest_test.go         # Tests de Integración Teatest
└── testdata/               # Carpeta para Golden Files
    └── TestViewGolden.golden
```

### Comandos de Ejecución
```bash
go test ./...                           # Run all tests
go test -v ./internal/tui/...          # Verbose TUI tests
go test -run TestNavigation             # Run specific test
go test -cover ./...                    # With coverage
go test -update ./...                   # Update golden files
```

## Troubleshooting
- *Si ocurre Data Race:* El comando `go test` fallará o será inconsistente de forma aleatoria. Ejecutar `go test -race ./...` para localizar la colisión de rutinas.
- *Si los Golden Files fallan (mismatch):* Verificar si el cambio visual detectado fue intencional en el código. Si lo fue, la solución es regenerar ejecutando `go test -update ./...`.
- *Si `teatest` se cuelga (timeout):* Verificar que se esté enviando el `tea.KeyMsg` adecuado que interrumpe el bucle interno, o asegurar el uso de `tm.WaitFinished(t, teatest.WithDuration(time.Second))`.

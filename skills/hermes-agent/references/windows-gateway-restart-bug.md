# Windows: Gateway `/restart` No Reinicia

## Síntoma

El comando `/restart` de Telegram (o `hermes gateway restart` desde CLI) detiene el gateway pero **nunca lo vuelve a levantar**. El log muestra "Stopping gateway for restart..." seguido de "Gateway stopped" y luego silencio — sin "Starting Hermes Gateway...".

## Causa Raíz

El restart en Windows usa un **watcher** (script Python inline lanzado vía `sys.executable -c`) que espera a que el PID del gateway muera y luego ejecuta `hermes gateway restart`. Dos bugs impedían que funcionara:

### Bug 1: `sys.executable` es `hermes.exe` (PyInstaller), no `python.exe`

Cuando el gateway corre como `hermes.exe` (bundle PyInstaller), `sys.executable` apunta a `hermes.exe`, que **no soporta `-c`**. El watcher se lanza como:

```python
subprocess.Popen([sys.executable, "-c", watcher_code, str(pid), *cmd_argv])
```

Esto se convierte en `hermes.exe -c "codigo..."`, que hermes interpreta como búsqueda de sesión y falla silenciosamente (el watcher redirige stdout/stderr a DEVNULL, así que no hay rastro en logs).

**Fix:** Detectar cuando `sys.executable` no es `python.exe` y buscar `python.exe` en el mismo directorio del venv:

```python
_watcher_python = sys.executable
if sys.platform == "win32" and _watcher_python.lower().endswith(".exe") and "python" not in os.path.basename(_watcher_python).lower():
    _candidates = [
        os.path.join(os.path.dirname(_watcher_python), "python.exe"),
        os.path.join(os.path.dirname(_watcher_python), "python3.exe"),
    ]
    for _cand in _candidates:
        if os.path.isfile(_cand):
            _watcher_python = _cand
            break
```

### Bug 2: `shutil.which("hermes")` devuelve `hermes.CMD`, no `hermes.exe`

En Windows, `shutil.which("hermes")` encuentra `hermes-bin/hermes.CMD` (un batch file wrapper). `subprocess.Popen` con `shell=False` **no puede ejecutar archivos `.cmd`** directamente — necesitan `cmd.exe` como intermediario. El watcher ejecutaba:

```python
subprocess.Popen(["hermes.CMD", "gateway", "restart"], shell=False, ...)
```

El proceso quedaba colgado o fallaba silenciosamente.

**Fix:** Parchear `_resolve_hermes_bin()` para que cuando detecte un `.cmd`/`.bat`, lea el archivo y extraiga la ruta real del `.exe`:

```python
if sys.platform == "win32" and hermes_bin.lower().endswith((".cmd", ".bat")):
    with open(hermes_bin, "r", errors="replace") as f:
        for line in f:
            line = line.strip()
            if line.lower().startswith('"') and "hermes.exe" in line.lower():
                exe_path = line.split('"')[1]
                if os.path.isfile(exe_path):
                    return [exe_path]
```

**Fix adicional (defensa en profundidad):** El watcher ahora usa `shell=True` cuando `cmd[0]` termina en `.cmd` o `.bat`:

```python
_use_shell = os.name == 'nt' and cmd[0].lower().endswith(('.cmd', '.bat'))
subprocess.Popen(cmd, shell=_use_shell, ...)
```

## Archivos Modificados

- `gateway/run.py`:
  - Función `_resolve_hermes_bin()` (~línea 1491): Resuelve `.cmd` → `.exe`
  - Función `_launch_detached_restart_command()` (~línea 3843): Usa `python.exe` del venv y `shell=True` para `.cmd`

## Verificación

Después del fix, un `/restart` desde Telegram debería:

1. Detener el gateway (logs: "Stopping gateway for restart..." → "Gateway stopped")
2. El watcher espera ~0.2s a que el PID muera
3. El watcher ejecuta `hermes gateway restart`
4. El gateway arranca de nuevo (logs: "Starting Hermes Gateway..." → "Gateway running")
5. Telegram recibe notificación: "Gateway restarted"

## Diagnóstico Si Vuelve a Fallar

1. Verificar que el watcher se lanza: buscar en logs del gateway "Stopping gateway for restart..."
2. Si el gateway se detiene pero no vuelve a arrancar, el watcher falló
3. Verificar que `python.exe` existe en el venv: `dir venv\Scripts\python.exe`
4. Verificar que `hermes.CMD` apunta a `hermes.exe`: `type %APPDATA%\local\hermes-bin\hermes.CMD`
5. Probar manualmente: `python.exe -c "import subprocess; subprocess.Popen(['hermes.exe', 'gateway', 'status'])"`

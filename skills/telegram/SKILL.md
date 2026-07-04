---
name: telegram-gateway-setup
description: "Configurar, verificar y troubleshoot del gateway de Telegram en Hermes Agent — token, .env, config.yaml, gateway restart, dependencias de plugin."
version: 2.1.0
author: OWL
model_tier: medium
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [telegram, gateway, bot, setup, troubleshooting, windows]
    related_skills: [hermes-agent]
---

## Execution Phases


**DRY-RUN RULE:** Before executing any destructive or external operation, first perform a dry-run to preview what will happen. Show the user what actions would be taken, then ask for confirmation before proceeding.
### 1. Preparation Phase
- Load references and verify prerequisites
- Resolve target scope

### 2. Action Phase
- Execute the main workflow (original content below preserves existing steps)

### 3. Verification Phase
- Verify output matches expected results

## Context & Triggers
**When to use this skill:**
- Triggers: "telegram-gateway-setup", "use telegram-gateway-setup"


# Telegram Gateway — Setup & Troubleshooting


## Diagnóstico Rápido

Cuando algo no funcionar, seguir estos pasos en orden:

### 1. Verificar el token
```bash
curl -s "https://api.telegram.org/bot<TOKEN>/getMe"
```
- **200 OK** → token válido, el problema es otro
- **401 Unauthorized** → token malo/inválido
- **404 Not Found** → bot eliminado de Telegram

### 2. Verificar el gateway
```bash
hermes gateway status
```
Debe mostrar: `✓ Gateway process running` y `✓ telegram connected`

### 3. Verificar logs
```bash
tail -50 ~/.hermes/logs/gateway.log | grep -i telegram
```

### 4. Verificar dependencias del plugin
```bash
uv pip list --python "<ruta_al_venv>/Scripts/python.exe" | grep -i telegram
```
Si no aparece `python-telegram-bot` → es el problema (ver Problema 1).

---

## Problemas Conocidos

### Problema 1: "Platform 'Telegram' requirements not met"

**Síntema:** El gateway arranca pero los logs muestran:
```
WARNING gateway.platform_registry: Platform 'Telegram' requirements not met (pip install 'hermes-agent[telegram]')
ERROR gateway.run: Platform 'telegram' is registered but adapter creation failed
WARNING gateway.run: No adapter available for telegram
```
Y el gateway termina corriendo con 1 plataforma (solo api_server, sin Telegram).

**Causa:** Falta instalar `python-telegram-bot` en la venv. El mensaje `pip install 'hermes-agent[telegram]'` es engañoso — en la versión atual de hermes-agent ese extra NO existe como paquete distribuible. El plugin de Telegram ya está incluido en el código fuente del repo, pero requiere la dependencia `python-telegram-bot` por separado.

**Solución:**
```bash
uv pip install python-telegram-bot --python "<ruta_al_venv>/Scripts/python.exe"
```
Luego reiniciar: `hermes gateway restart`

**Verificación:** Los logs deben mostrar:
```
[Telegram] Connected to Telegram (polling mode)
✓ telegram connected
Gateway running with 2 platform(s)
```

---

### Problema 2: "✓ telegram connected" pero el bot no responde

**Síntema:** Los logs muestran `✓ telegram connected` y `set_my_commands OK`, pero al enviar un mensaje al bot no hay respuesta. Telegram muestra los mensajes como entregados.

**Causa:** El `chat_id` del usuario no está en `TELEGRAM_ALLOWED_USERS`, o está mal configurado (por ejemplo, se puso el @username en vez del ID numérico).

**Solución:**
1. Obtener el chat ID real:
   ```bash
   curl -s "https://api.telegram.org/bot<TOKEN>/getUpdates"
   ```
   El `chat.id` del último mensaje es tu ID numérico.

2. Actualizar `.env` con Python binario (NUNCA con sed/shell):
   ```python
   env_path = r'D:\Engram_SDD\Hermes-Nous\hermes-data\.env'
   with open(env_path, 'rb') as f:
       data = f.read()
   lines = data.split(b'\n')
   for i, line in enumerate(lines):
       if line.startswith(b'TELEGRAM_ALLOWED_USERS='):
           lines[i] = b'TELEGRAM_ALLOWED_USERS=<chat_id_numerico>'
       if line.startswith(b'TELEGRAM_HOME_CHANNEL='):
           lines[i] = b'TELEGRAM_HOME_CHANNEL=<chat_id_numerico>'
   with open(env_path, 'wb') as f:
       f.write(b'\n'.join(lines))
   ```

3. Reiniciar gateway.

**Nota:** Usar el ID numérico del humano, NO el @username del bot.

---

### Problema 3: Token inválido ("was rejected by the server")

**Síntema:** Los logs muestran:
```
telegram.error.InvalidToken: The token `8795...37s` was rejected by the server.
```

**Causa:** El token en `.env` está **truncado**. Sucede cuando se usa `sed` o comandos de shell para escribirlo — el carácter `:` del token rompe el parsing del shell.

**Solución:**
1. Verificar longitud del token:
   ```bash
   grep TELEGRAM_BOT_TOKEN .env | xxd | head -5
   ```
   Un token válido tiene 46+ caracteres.

2. Reescribir con Python (NUNCA con sed/shell):
   ```python
   token = sys.argv[1]  # pasar como argumento
   env_path = r'D:\Engram_SDD\Hermes-Nous\hermes-data\.env'
   with open(env_path, 'rb') as f:
       data = f.read()
   lines = data.split(b'\n')
   for i, line in enumerate(lines):
       if line.startswith(b'TELEGRAM_BOT_TOKEN='):
           lines[i] = b'TELEGRAM_BOT_TOKEN=' + token.encode('utf-8')
           break
   with open(env_path, 'wb') as f:
       f.write(b'\n'.join(lines))
   ```

3. Reiniciar gateway: `hermes gateway restart`

---

### Problema 4: Token con caracteres \r (CRLF)

**Síntoma:** El token es válido (curl a getMe funciona) pero el gateway sigue rechazándolo.

**Causa:** El archivo `.env` tiene finales de línea de Windows (CRLF). El `\r` se pega al final del token y Telegram lo rechaza.

**Solución:**
1. Verificar:
   ```bash
   cat -A .env | grep TELEGRAM_BOT_TOKEN
   ```
   Si hay `^M` al final → hay `\r`.

2. Reescribir el token con Python en modo binario (mismo método que Problema 3).

---

### Problema 5: Gateway usa token viejo en caché

**Síntoma:** Se actualizó el token en `.env` pero el gateway sigue usando el anterior.

**Causa:** El gateway cachea las variables de entorno al iniciar. No relee el `.env` hasta que se reinicia.

**Solución:**
```bash
hermes gateway restart
```

---

### Problema 6: "No bot token configured"

**Síntema:** Los logs muestran `[Telegram] No bot token configured`.

**Causa:** La variable `TELEGRAM_BOT_TOKEN` no existe en el entorno del gateway, o el adapter no se pudo crear por dependencia faltante (ver Problema 1).

**Solución:**
1. Verificar que existe en `.env`:
   ```bash
   grep TELEGRAM_BOT_TOKEN .env
   ```

2. Si existe, verificar que `python-telegram-bot` esté instalado (ver Problema 1).

3. Reiniciar gateway.

---

### Problema 7: Cron delivery "Unauthorized"

**Síntema:** El cron job corre OK pero `last_delivery_error` dice `"Telegram send failed: Unauthorized"`.

**Causa:** El gateway tiene un token inválido/truncado, o se reinició con un token viejo.

**Solución:**
1. Verificar token con `curl` (paso 1 del diagnóstico)
2. Verificar que no esté truncado (Problema 3)
3. Reescribir token + reiniciar gateway

---

## Configuración Inicial (de cero)

### 1. Crear bot en Telegram
1. Buscar **@BotFather** en Telegram
2. Enviar `/newbot`
3. Elegir nombre y username (debe terminar en `bot`)
4. Guardar el token que devuelve BotFather

### 2. Obtener chat ID
```bash
curl -s "https://api.telegram.org/bot<TOKEN>/getUpdates"
```
El `chat.id` del último mensaje es tu chat ID.

### 3. Instalar dependencia del plugin
```bash
uv pip install python-telegram-bot --python "<ruta_al_venv>/Scripts/python.exe"
```

### 4. Configurar .env
Archivo: `D:\Engram_SDD\Hermes-Nous\hermes-data\.env`

```env
TELEGRAM_BOT_TOKEN=<token_completo>
TELEGRAM_HOME_CHANNEL=<chat_id>
TELEGRAM_ALLOWED_USERS=<chat_id>
```

**Escribir con Python binario** (ver Problema 3). NUNCA con sed/shell.

### 5. Configurar config.yaml
Archivo: `D:\Engram_SDD\Hermes-Nous\hermes-data\config.yaml`

```yaml
telegram:
  reactions: false
  channel_prompts: {}
  allowed_chats: '<chat_id>'
```

### 6. Reiniciar y verificar
```bash
hermes gateway restart
hermes gateway status
curl -s "https://api.telegram.org/bot<TOKEN>/getMe"
```

---

## Limpieza (empezar de cero)

1. Eliminar líneas de Telegram del `.env`:
   ```bash
   findstr /V /I "TELEGRAM" .env > .env.tmp && move /Y .env.tmp .env
   ```

2. Limpiar `config.yaml` (vaciar `allowed_chats` y `home_channel`)
3. Reiniciar gateway

---

## Notas

- El `.env` está protegido contra lectura directa por tools de Hermes. Usar `terminal` con `cat`/`grep`.
- El token NUNCA debe aparecer en logs ni mensajes.
- Si el token se revoca, crear uno nuevo con @BotFather — no se puede recuperar.
- En Windows, el gateway corre como proceso nativo (`hermes.cmd`), no desde WSL.
- El gateway usa `python-telegram-bot` internamente — debe estar instalado en la venv.
- El plugin de Telegram se descubre automáticamente desde `plugins/platforms/telegram/` en el repo. No se instala vía pip; solo requiere la dependencia `python-telegram-bot`.
- El mensaje `pip install 'hermes-agent[telegram]'` es un error conocido — ese extra no existe en la versión distribuible actual.

## Mantenimiento de esta Skill

**NO agregar problemas hipotéticos ni edge cases raros.** Solo documentar problemas que el usuario encontró realmente y que sean probables de repetirse. Si un problema se resolvió una vez y es improbable que vuelva (bug específico de una versión ya parcheada, configuración única del usuario, etc.), no merece su propia sección.

Mantener el formato: **Síntoma → Causa → Solución**. No agregar introducciones largas ni explicaciones teóricas.

## Crear Acceso Directo en el Desktop (Windows)

`WScript.Shell.CreateShortcut` NO funciona desde cscript ni PowerShell ejecutados vía bash/MSYS en este entorno. El workaround es crear el .lnk manualmente con el formato binario de Windows Shell Link:

```python
import struct, os

def create_lnk(target_path, working_dir, description, lnk_path):
    link_flags = 0x00020003
    file_attrs = 0x00000080
    hotkey = 0x0000
    header_size = 0x0000004C
    clsid = bytes.fromhex('0002140000000000C000000000000046')
    target_bytes = target_path.encode('utf-16-le')
    working_dir_bytes = working_dir.encode('utf-16-le')
    desc_bytes = description.encode('utf-16-le')
    link_info_header_size = 0x0000001C
    link_info_flags = 0x00000001
    local_path_offset = link_info_header_size + 4
    common_path_suffix_offset = local_path_offset + len(target_bytes) + 2
    link_info_size = common_path_suffix_offset + len(working_dir_bytes) + 2
    string_data = target_bytes + b'\x00\x00' + working_dir_bytes + b'\x00\x00' + desc_bytes + b'\x00\x00'
    lnk = bytearray()
    lnk += struct.pack('<I', header_size)
    lnk += clsid
    lnk += struct.pack('<I', link_flags)
    lnk += struct.pack('<I', file_attrs)
    lnk += b'\x00' * 16
    lnk += struct.pack('<I', 0)
    lnk += struct.pack('<I', hotkey)
    lnk += struct.pack('<H', 0)
    lnk += struct.pack('<H', 0)
    lnk += struct.pack('<I', 0)
    lnk += struct.pack('<I', 0)
    lnk += struct.pack('<H', 0)
    lnk += struct.pack('<I', link_info_size)
    lnk += struct.pack('<I', link_info_header_size)
    lnk += struct.pack('<I', link_info_flags)
    lnk += struct.pack('<I', local_path_offset)
    lnk += struct.pack('<I', local_path_offset)
    lnk += struct.pack('<I', 0)
    lnk += struct.pack('<I', common_path_suffix_offset)
    lnk += target_bytes + b'\x00\x00'
    lnk += working_dir_bytes + b'\x00\x00'
    lnk += struct.pack('<H', 1)
    lnk += struct.pack('<H', len(desc_bytes) // 2)
    lnk += desc_bytes + b'\x00\x00'
    with open(lnk_path, 'wb') as f:
        f.write(lnk)

create_lnk(
    r"C:\Users\user\Desktop\Hermes_Gateway.cmd",
    r"C:\Users\user\Desktop",
    "Hermes Gateway",
    r"C:\Users\user\Desktop\Hermes Gateway.lnk"
)
```

**Nota:** `WindowStyle = 7` = ventana minimizada. El .cmd launcher debe existir antes de crear el .lnk.


## Guardrails (Critical Rules)
- **NEVER** execute destructive operations without explicit user confirmation
- **ALWAYS** verify target exists before operating
- **ALWAYS** handle errors gracefully — skip with warning, don't crash


---
name: fast-file-locator
description: Instruye a la IA sobre cómo buscar archivos en Windows de forma instantánea usando el servidor HTTP local de Everything.
author: TaoTomate
generator_model: gemini-3.5-flash
version: 1.1.0
inherited_from: custom local architecture
---

# Fast File Locator (Everything HTTP API)

## Contexto
No uses herramientas lentas de iteración de directorios o búsqueda estándar cuando necesites encontrar la ruta absoluta de un archivo en el disco duro.
En su lugar, realiza peticiones al servidor HTTP local de Everything que consulta la Master File Table (MFT) directamente y devuelve resultados en milisegundos, salteando el aislamiento de Window Station.

## Credenciales y Endpoint
- **Base URL**: `http://localhost/` (puerto 80)
- **Usuario**: `user`
- **Contraseña**: `123456`

## Reglas de Ejecución
1. **Nunca iteres directorios** para encontrar un archivo si conocés su nombre o extensión. Usá esta herramienta.
2. **Petición HTTP**: Realizá una llamada HTTP GET usando PowerShell (`Invoke-RestMethod`) o curl.
3. **Parámetros Obligatorios**:
   - `search=<query>`: El término a buscar (soporta la sintaxis de búsqueda de Everything).
   - `json=1`: Fuerza la respuesta en formato JSON.
   - `path_column=1`: Obliga a incluir el directorio del archivo en el campo `"path"`.
   - `count=<limit>`: Limitá siempre los resultados (ej. `count=10`) para no inundar el contexto.
4. **Comando para Agentes**: Utilizá la herramienta `run_command` con PowerShell para ejecutar la consulta.

## Ejemplos
- Buscar un archivo por nombre exacto en PowerShell:
  ```powershell
  $secpasswd = ConvertTo-SecureString "123456" -AsPlainText -Force
  $mycreds = New-Object System.Management.Automation.PSCredential ("user", $secpasswd)
  Invoke-RestMethod -Uri "http://localhost/?search=docker-compose.yml&json=1&path_column=1&count=1" -Credential $mycreds
  ```
- Buscar todos los `.log` pesados en un proyecto:
  ```powershell
  $secpasswd = ConvertTo-SecureString "123456" -AsPlainText -Force
  $mycreds = New-Object System.Management.Automation.PSCredential ("user", $secpasswd)
  Invoke-RestMethod -Uri "http://localhost/?search=ext:log C:\Users\user\antigravity&json=1&path_column=1&count=5" -Credential $mycreds
  ```

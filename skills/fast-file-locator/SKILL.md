---
name: fast-file-locator
description: Instruye a la IA sobre cómo buscar archivos en Windows de forma instantánea usando Everything CLI (es.exe).
author: TaoTomate
generator_model: gemini-3.1-pro
version: 1.0.0
inherited_from: custom local architecture
---

# Fast File Locator (Everything CLI)

## Contexto
No uses herramientas lentas de iteración de directorios o búsqueda estándar cuando necesites encontrar la ruta absoluta de un archivo en el disco duro.
En su lugar, utiliza el CLI de Everything (`es.exe`), que consulta la Master File Table (MFT) directamente y devuelve resultados en milisegundos.

## Herramienta Subyacente
Ruta absoluta del binario: `D:\Engram_SDD\Tools\es.exe`

## Reglas de Ejecución
1. **Nunca iteres directorios** para encontrar un archivo si conocés su nombre o extensión. Usá esta herramienta.
2. **Limitá los resultados**: Por defecto, utilizá SIEMPRE el flag `-max-results N` (ej. `-max-results 10`) para evitar inundar el contexto con miles de rutas si la búsqueda es muy genérica.
3. **Búsquedas de ruta específica**: Si sabés que el archivo está en una carpeta, pasale la ruta como parámetro para filtrar: `es.exe "query" "C:\ruta\del\proyecto"`
4. **Búsquedas con Regex**: Si el nombre es complejo o necesitás un patrón exacto, usá el flag `-r`. Ejemplo: `es.exe -max-results 5 -r "^config_.*\.json$"`
5. **Comando para Agentes**: Utilizá tu herramienta de ejecución de comandos de terminal (ej. `run_command`) para llamar al binario.

## Ejemplos
- Buscar todos los `.log` pesados en un proyecto: `D:\Engram_SDD\Tools\es.exe ext:log "C:\Users\user\antigravity" -max-results 5`
- Buscar un archivo por nombre exacto: `D:\Engram_SDD\Tools\es.exe "docker-compose.yml" -max-results 1`

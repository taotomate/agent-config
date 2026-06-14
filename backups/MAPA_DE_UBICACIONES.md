# Mapa de Ubicaciones de Archivos de Agente

Este documento detalla todas las ubicaciones locales donde se encontraban los archivos de agentes duplicados, mapeados a su versión consolidada en este repositorio de backups.

## v4.7 (Última versión conocida)
Hash SHA256: `258230240CBF431A706D36E4C097E658BFDF4F8EFC2FBDF36C6B5E48952E309E`
Ubicaciones locales encontradas:
- `D:\Engram_SDD\AGENTS.md` (Copia principal respaldada aquí)
- `C:\Users\user\.gemini\antigravity\brain\5cc77de3-deb6-4b5b-812f-5cfa818324b0\scratch\agent-config\shared\agents.md`

## v4.3
Hash SHA256: `F69F0B9BAF98EE7C6A04EE51F30445A399A8084C46878FA95A9BB4AEC08B224D`
Ubicaciones locales encontradas:
- `C:\Users\user\.config\opencode\AGENTS.md` (Copia principal respaldada aquí)
- `C:\Users\user\.gemini\config\skills\_shared\agents.md`
- `C:\Users\user\TaoTomate.Dots\agent-config\shared\agents.md`

*Nota:* `D:\TaoTomate.Dots\agent-config\shared\agents.md` tiene un hash ligeramente diferente (`AAA39CB...`), posiblemente por line endings.

## v4.2
Hash SHA256: `DF99E949607557261B5DF42429F5A8D850A723287B59DBB64F289AA471BA7109` y `2494967FF2A9F7AF152F04C7C44B2262215C82DCE5F9CC6E818A4FBEC75796F0`
Ubicaciones locales encontradas:
- `C:\Users\user\.gemini\config\skills\_shared.bak_20260610_223031\agents.md` (Copia principal respaldada aquí)
- `D:\Users\Cosmic\Downloads\CLAUDE.md`

## v4.1
Hashes SHA256 varían ligeramente por saltos de línea (`32E259EB...`, `235049CE...`, `A579273...`)
Ubicaciones locales encontradas:
- `D:\Antigravity\AGENTS.md` (Copia principal respaldada aquí)
- `D:\Antigravity\CLAUDE.md`
- `D:\Antigravity\GEMINI.md`

## Otros (Project Specific / Core Rules)
Archivos respaldados en la carpeta `otros/` que no pertenecen al estándar v4.x pero son propios:
- `C:\Users\user\.gemini\GEMINI.md` -> `otros/GEMINI.md` (Reglas core vivas, sin tag explícito)
- `C:\Users\user\.config\gga\AGENTS.md` -> `otros/gga_AGENTS.md` (Reglas de Code Review React/TS)
- `D:\Engram_SDD\Hermes-Nous\hermes-agent\AGENTS.md` -> `otros/hermes_AGENTS.md` (Guía de desarrollo de Hermes)
- `D:\Voveda\00_Specs\AGENTS.md` -> `otros/voveda_AGENTS.md` (Directivas Zettelkasten)

## Archivos Ignorados (Librerías de Terceros)
Los siguientes archivos no fueron respaldados ya que pertenecen a paquetes de terceros y contienen instrucciones exclusivas para modificar sus propios proyectos:
- `recharts/AGENTS.md` (x3 ubicaciones)
- `thread-stream/CLAUDE.md` (x2 ubicaciones)
- `github.copilot-chat.../agents.md` (x2 ubicaciones)
- `inspect_ai.../CLAUDE.md`
- `everything/AGENTS.md`
- Plantillas de `Hermes-Nous` (`templates/claude.md`) que son boilerplate.

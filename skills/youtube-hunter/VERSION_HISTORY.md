# YouTube-Hunter Version History

## v5.2 - 2026-05-08 (Current)
**The "Surgical Extraction" Update**
- **Desafío**: YouTube cambió su DOM a una arquitectura basada en `view-models` (`transcript-segment-view-model`), rompiendo los selectores clásicos.
- **Solución**: Implementación de selectores híbridos que soportan tanto la UI vieja como la nueva de 2026.
- **Éxito**: Extracción 100% limpia sin ruido de botones, anuncios o descripción.
- **Novedad**: Pausa automática del video (`key: k`) para estabilizar el scroll de la transcripción.

## v5.1 - 2026-05-07
**Metadata & Stealth**
- **Desafío**: Bloqueos por anti-bot y falta de contexto en los archivos generados.
- **Solución**: Agregado de User-Agent real, viewport de escritorio y extracción de metadatos (Canal, Tags, Duración) vía JSON-LD.
- **Éxito**: Los archivos ahora tienen frontmatter YAML compatible con Zettelkasten.

## v5.0 - Early Dev
**Playwright Core**
- Migración de scraping simple a automatización con Playwright.
- Manejo básico de cookies.

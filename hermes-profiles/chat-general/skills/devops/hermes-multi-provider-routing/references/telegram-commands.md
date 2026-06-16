# Comandos de Hermes en Telegram — Referencia Rápida

127 comandos totales (actualizado jun 2026). Organizados por categoría.

## Sesión
- `/start` — Iniciar/reconocer el bot
- `/new [nombre]` — Nueva sesión fresca (alias: `/reset`)
- `/resume [nombre]` — Resumir sesión previa
- `/sessions` — Ver sesiones anteriores
- `/title [nombre]` — Título a la sesión
- `/branch [nombre]` — Ramificar sesión (alias: `/fork`)
- `/topic [off|help|id]` — Temas Telegram DM

## Control de Flujo
- `/stop` — Matar TODOS los procesos background
- `/background <prompt>` — Ejecutar en background (alias: `/bg`, `/btw`)
- `/queue <prompt>` — Encolar sin interrumpir (alias: `/q`)
- `/steer <prompt>` — Inyectar mensaje sin interrumpir
- `/retry` — Reintentar último mensaje
- `/undo` — Deshacer último exchange
- `/compress [here N|focus]` — Comprimir contexto
- `/rollback [número]` — Restaurar checkpoints
- `/approve [session|always]` — Aprobar comando peligroso
- `/deny` — Denegar comando peligroso

## Modelo / Comportamiento
- `/model [modelo]` — Cambiar modelo (alias: `/provider`)
- `/fast [normal|fast]` — Modo rápido
- `/reasoning [level|show|hide]` — Razonamiento
- `/personality [nombre]` — Personalidad predefinida
- `/yolo` — Modo YOLO (sin aprobaciones)
- `/voice [on|off|tts]` — Modo voz

## Info / Debug
- `/status` — Info de la sesión
- `/usage` — Tokens y rate limits
- `/insights [días]` — Analíticas
- `/whoami` — Ver acceso
- `/profile` — Perfil activo
- `/agents` — Agents activos (alias: `/tasks`)
- `/debug` — Subir reporte debug

## Gateway / Sistema
- `/restart` — Reiniciar gateway
- `/update` — Actualizar Hermes
- `/sethome` — Setear canal principal
- `/reload_mcp` — Recargar MCP servers
- `/reload_skills` — Re-escanear skills
- `/platform <pause|resume|list>` — Gestionar plataformas

## Skills Destacados (40+)

### Productividad
`/airtable` `/google_workspace` `/linear` `/notion` `/obsidian` `/maps` `/nano_pdf` `/ocr_and_documents` `/powerpoint` `/teams_meeting_pipeline`

### Desarrollo
`/claude_code` `/codex` `/opencode` `/github_auth` `/github_issues` `/github_pr_workflow` `/github_repo_management` `/github_code_review` `/codebase_inspection` `/debugging_hermes_tui_commands` `/dspy` `/node_inspect_debugger`

### Creatividad
`/ascii_art` `/ascii_video` `/architecture_diagram` `/baoyu_article_illustrator` `/baoyu_comic` `/baoyu_infographic` `/claude_design` `/comfyui` `/excalidraw` `/manim_video` `/p5js` `/pixel_art` `/popular_web_designs` `/pretext` `/sketch` `/songwriting_and_ai_music` `/touchdesigner_mcp`

### Media / Búsqueda
`/arxiv` `/blogwatcher` `/gif_search` `/polymarket` `/spotify` `/youtube_content` `/heartmula` `/songsee`

### Datos / Ciencia
`/jupyter_live_kernel` `/huggingface_hub` `/llama_cpp` `/segment_anything_model` `/weights_and_biases` `/llm_wiki`

### DevOps
`/credential_audit` `/kanban` `/webhook_subscriptions` `/hermes_gateway_windows` `/hermes_multi_provider_routing`

### Comunicación
`/himalaya` `/yuanbao`

### Misc
`/dogfood` `/godmode` `/hermes_agent` `/hermes_agent_skill_authoring` `/humanizer` `/ideation` `/pokemon_player` `/plan` `/requesting_code_review` `/systematic_debugging` `/test_driven_development` `/spike` `/subagent_driven_development` `/writing_plans` `/design_md`

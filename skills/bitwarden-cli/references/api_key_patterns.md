API key field patterns commonly found in Bitwarden items

## Campo de notas
Los items con API keys suelen usar el campo `notes` para almacenar:
- Notas con "Origen: <proyecto> / <archivo>.env"
- Texto: "Migrado automaticamente del .env"
- Clave nombrada: "Key: <NOMBRE_API_KEY>"

## Búsqueda efectiva

```python
# Filtrar por nombre
'api' in i.get('name','').lower()

# Filtrar por notas
'api' in i.get('notes','').lower() or 'key' in i.get('notes','').lower()

# Detectar campos ocultos
len(i.get('fields',[])) > 0
```

## Nombres comunes encontrados

- "Hermes > OpenRouter API Key" - OPENROUTER_API_KEY
- "Hermes > Anthropic Api Key" - ANTHROPIC_API_KEY
- "Hermes > Google Ai Studio Key" - GOOGLE_AI_STUDIO_KEY
- "Hermes > Groq Api Key" - GROQ_API_KEY
- "Hermes > Deepseek Api Key" - DEEPSEEK_API_KEY
- "Api Server Key" - API_SERVER_KEY
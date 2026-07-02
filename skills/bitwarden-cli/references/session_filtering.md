# Session Filtering Pattern

Patrón para filtrar items de Bitwarden desde Hermes en Windows/Unix.

## Comando usado

```bash
export BW_SESSION="<session-key>" && bw list items --session "$BW_SESSION" | python -c "..."
```

## Por qué funciona

- `export BW_SESSION` establece la variable en la misma línea
- `&& bw list items` ejecuta inmediatamente sin esperar a que termine export
- El pipe a `python -c` procesa JSON directamente sin necesidad de `jq` (que no está disponible en Windows)
- Usar Python para filtrar JSON es cross-platform y más confiable que `jq`

## Código de filtrado efectivo

```python
import sys, json
items = json.load(sys.stdin)
for i in items:
    if 'api' in i.get('name','').lower() or 'api' in i.get('notes','').lower():
        print(f"{i.get('name')}: notes={bool(i.get('notes'))} fields={len(i.get('fields',[]))}")
```
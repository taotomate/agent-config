# Token Tracking — Template para Workers Multi-Modelo

## Formato obligatorio (al final de cada respuesta del worker)

```
TOKENS: P={prompt_tokens} C={completion_tokens} T={total_tokens} | TURNO={n} | ACUM={total_acumulado}
```

- `P`: tokens en system prompt + conversation history + mensaje actual
- `C`: tokens en la respuesta
- `T`: P + C
- `TURNO`: número de turno en este hilo (empezando en 1)
- `ACUM`: suma de todos los T de este hilo

Si no hay tokens exactos: estimar `palabras × 1.33`, marcar con `~`.

Ejemplo:
```
TOKENS: P=~1200 C=~350 T=~1550 | TURNO=3 | ACUM=~4200
```

## System prompt fragment para workers

Agregar al system prompt de cada perfil/hilo:

```
## Token Tracking Obligatorio

Al FINAL de cada respuesta, incluí ÚNICAMENTE esta línea (nada después):

TOKENS: P={prompt_tokens} C={completion_tokens} T={total_tokens} | TURNO={turn_number} | ACUM={accumulated_tokens}

Estimación: si no tenés los números exactos, calculá palabras × 1.33.
Marcá claramente si es estimado con ~ delante del número.
```

## Tracking dual

- **Modelo**: reporta tokens en cada respuesta (formato arriba)
- **OWL (orquestador)**: cuenta tokens independientemente para verificar
- **Discrepancia**: si la diferencia es >20%, OWL loguea el evento
- **Compresión**: cuando el acumulado supera el umbral del modelo asignado, OWL comprime el hilo (session compaction nativa de Hermes)

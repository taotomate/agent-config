---
name: dual-execution-validation
description: >
  Ejecuta tareas técnicas mediante validación cruzada (Cloud vs Local LLM) para 
  comparar fidelidad de resultados, establecer fronteras de capacidad y optimizar 
  el consumo de tokens mediante benchmarking en tiempo real.
  Trigger: "dual execution", "validación dual", "correr frontera", "comparar con local".
metadata:
  author: gentleman-programming
  version: "2.0"
---

## When to Use

- Cuando se quiere probar si una tarea repetitiva (tests, refactors simples) puede ser delegada al modelo local.
- Para validar la precisión de modelos locales contra modelos en la nube en problemas de lógica.
- Al procesar grandes volúmenes de texto donde el ahorro de tokens es crítico.

## Protocolo de Ejecución

1. **Prompt Sincronizado**: Se debe enviar EXACTAMENTE el mismo prompt y contexto a ambos modelos.
2. **Uso de Herramienta**: El modelo local se invoca mediante `ask_llm`.
3. **Reporte Comparativo**: El orquestador debe generar una tabla comparativa inmediata.

## Matriz de Evaluación (Veredicto)

| Criterio | Gemini (Pro/Flash) | Qwen 8B (Local) |
|----------|-------------------|-----------------|
| **Lógica** | (1-10) - Profundidad | (1-10) - Precisión |
| **Contexto** | (1-10) - Visión global | (1-10) - Visión túnel |
| **Velocidad** | Tiempo en segundos | Tiempo en segundos |
| **Ahorro** | 0% (Costo base) | 100% (Tokens salvados) |

## Patrones Críticos

- **Detección de "Visión de Túnel"**: Especial atención a si el modelo local ignora el contexto del archivo (ej. mezcla secciones de YAML o rompe scopes de funciones).
- **Actualización de Frontera**: Si el modelo local gana 3 veces seguidas en una categoría, marcar esa categoría como "Segura para Delegación" en Engram.

## Comandos

```bash
# Ejemplo de invocación manual del test de comparación
python scratch/shadow_test.py
```


<!-- youtube-scraper: processed -->

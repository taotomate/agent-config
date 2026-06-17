---
name: dual-execution-validation
description: >
  Ejecuta tareas técnicas mediante validación cruzada (Cloud vs Local LLM) para 
  comparar fidelidad de resultados, establecer fronteras de capacidad y optimizar 
  el consumo de tokens mediante benchmarking en tiempo real.
  Trigger: "dual execution", "validación dual", "correr frontera", "comparar con local".
metadata:
  version: "3.0"
author: TaoTomate
generator_model: gemini-1.5-pro
inherited_from: dual-execution-validation/SKILL.md
---

## Contexto y Triggers
**Cuándo usar esta skill:**
- Cuando se quiere probar si una tarea repetitiva (ej. tests, refactors simples) puede ser delegada al modelo local.
- Para validar la precisión de modelos locales contra modelos en la nube (ej. GPT/Gemini) en problemas de lógica.
- Al procesar grandes volúmenes de texto donde el ahorro de tokens es crítico.
- Triggers: "dual execution", "validación dual", "correr frontera", "comparar con local".

## Pre-requisitos
- [ ] Tener el modelo local configurado y accesible.
- [ ] Conocer el prompt exacto que se utilizará para la validación cruzada.

## Fases de Ejecución

> **[REGLA UNIVERSAL: DRY-RUN / SIMULACRO]**
> Si el usuario solicita la ejecución en modo `--dry-run` o pide un "simulacro", el agente **NO** ejecutará comandos que alteren el estado del sistema ni llamará a herramientas MCP destructivas en la Fase de Acción. 
> En su lugar, el agente imprimirá el payload exacto que planeaba ejecutar, y se detendrá a esperar la aprobación explícita del humano.

### 1. Fase de Diagnóstico
- Extraer la intención principal de la tarea.
- Preparar el prompt sincronizado: Se debe formular EXACTAMENTE el mismo prompt y contexto que se enviará a ambos modelos.

### 2. Fase de Acción
- **Ejecución Local**: Invocar el modelo local a través de la herramienta correspondiente o script (por ejemplo, mediante `ask_local_llm` si existe el MCP, o vía scripts en Python/bash pegándole a Ollama).
- **Ejecución Cloud**: Como agente orquestador, procesa tú mismo la tarea (utilizando tu propio motor) y guarda el resultado.

### 3. Fase de Verificación
- Generar un "Reporte Comparativo" inmediato. Presentar la matriz de evaluación (Veredicto) al usuario en el chat.
- Analizar y declarar en el reporte si hubo "Visión de Túnel" (si el modelo local ignoró el contexto general, como mezclar secciones o romper scopes).

## Guardrails (Reglas Críticas)
- **Sincronización Estricta:** El prompt debe ser exactamente el mismo para ambos modelos. No simplifiques el prompt del local.
- **Detección de Frontera:** Si el modelo local demuestra superar o igualar la prueba 3 veces seguidas en una categoría específica, deberás actualizar la frontera marcando esa categoría como "Segura para Delegación" y guardarlo en Engram.
- **No Halucinación Local:** Al evaluar el modelo local, penaliza fuertemente la alucinación o si rompe la estructura del código existente.

## Estructuras de Datos / Ejemplos y Comandos

**Matriz de Evaluación (Veredicto)**
Debe presentarse en formato Markdown con esta estructura:

| Criterio | Cloud (Ej. Gemini Pro) | Local (Ej. Qwen 8B / Hermes) |
|----------|------------------------|------------------------------|
| **Lógica** | (1-10) - Profundidad | (1-10) - Precisión |
| **Contexto** | (1-10) - Visión global | (1-10) - Visión túnel |
| **Velocidad** | Tiempo en segundos | Tiempo en segundos |
| **Ahorro** | 0% (Costo base) | 100% (Tokens salvados) |

**Comando de Ejecución (Opcional si hay script):**
```bash
# Ejemplo de invocación manual del test de comparación si existe el script de shadow test:
python scratch/shadow_test.py
```

## ⚠️ Residuos de Migración (Feedback para evolución)
*(Migrado exitosamente de v2.0 a IaC v1.2, formalizando el pipeline de delegación local vs cloud dentro de las fases de ejecución)*

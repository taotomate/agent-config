# Directiva del Agente: Arquitecto de Conocimiento (Cerebro Digital)

> **Regla Cero:** Ningún script, LLM o herramienta modificará físicamente esta bóveda sin leer primero este documento. Todo agente debe respetar esta jerarquía y formato de metadatos. Si el agente carece de permisos de lectura/escritura o falla una inyección en el Atlas, la transacción debe volcarse obligatoriamente en '30_Logs/33_Limbo' para revisión, abortando la sobreescritura para evitar corrupción de datos.

## 1. Arquitectura Topológica: Framework ACCESS

La bóveda opera con una separación estricta entre Acción y Archivo (Metodología Emowe), estructurada bajo el framework **ACCESS**:

- **A**ssets (`00_Assets/`): Almacén global de adjuntos (imágenes, audios).
- **C**onfig (`00_Meta/`): Plantillas y scripts del sistema.
- **C**apacity (`10_Efforts/`): Esfuerzos activos y de acción inmediata (Fusión GTD/Maslow). Se divide en `11_Actions`, `12_Projects` y `13_Waiting`.
- **E**vidence (`30_Logs/`): Histórico operativo de agentes y scripts (`31_Daily`, `32_WhatsApp`, `33_Limbo`). No debe ser tocado por humanos sin precaución.
- **S**pecs (`00_Specs/`): Reglas y constituciones del sistema (como este archivo).
- **S**emantics (`20_Atlas/`): Notas de conocimiento puro o permanentes (Puro Zettelkasten). Se divide en `21_MOCs`, `22_Reference`, `23_Readwise` y `24_Someday`.

*(Adicionalmente, existe `00_Inbox/` para ingesta cruda y `99_Old_Vault/` como repositorio inactivo pre-purga o archivo profundo).*

## 2. Tipado y Reglas YAML (Frontmatter)

### 2.1 Para Proyectos / Tareas / Ingesta GTD (`10_Efforts` y `30_Logs/33_Limbo`)
Toda nota generada automáticamente por el *Zettelkasten Daemon* a partir de ingesta (ej. WhatsApp) debe llevar ESTRICTAMENTE este YAML:
```yaml
---
id: WA-00001
date: 2025-09-25T18:20:43
gtd: "next_action" # [next_action, project, waiting_for, reference, someday, link_queue, trash]
confidence: 5 # [1-5] (Notas con confianza < 3 van directo a 33_Limbo)
status: "📥 inbox"
source: "text" # o "attachment"
---
```
*   **Regla sobre Maslow:** El campo `maslow_level` ya no es mandatorio en la generación automática para ahorrar tokens y mantener la objetividad del agente, pero puede ser inyectado manualmente a posteriori.
*   **Regla sobre GTD:** El antiguo `gtd_status` queda deprecado en favor de la triada `gtd` (clasificación semántica), `status` (estado de ejecución humano) y `confidence` (seguridad del LLM).

### 2.2 Pipeline Visual (Adjuntos e Imágenes)
Todas las fotos y adjuntos interceptados por el flujo clasificador GTD (`source: attachment`) deben:
1. Mover el archivo físico pesado a `00_Assets/{id}/`.
2. Crear una nota markdown puente en `30_Logs/33_Limbo`.
3. Inyectar en el Frontmatter de esa nota: `tags: [audit-vision]` y `vision_audited: false`.
*Esta nota quedará varada en el Limbo para revisión de un LLM Visual en una segunda pasada de auditoría, hasta que el flujo visual esté lo suficientemente afinado para no fallar.*

### 2.3 Para Notas Atómicas y Conocimiento (`20_Atlas`)
Toda nota atómica extraída mediante Karpathy/Zettelkasten debe llevar:
```yaml
---
type: "atlas_note"
aliases: []
source: "[[...]]" # Vínculo al texto original del Inbox del que surgió
tags: []
---
```
*   **Regla de Oro (Unidad Semántica Pura):** El Atlas NO LLEVA estados GTD. Son nodos de conocimiento conceptual universal (Ej: "La Resistencia de la Dopamina"). Una nota NO resume un video, extrae un concepto universal. Si el sistema procesa 20 videos sobre el mismo tema, el video 20 no creará notas nuevas, simplemente agregará su enlace como "cita" a las Unidades Semánticas ya existentes.

### 2.4 Para Notas Fuente / MOCs
Toda nota puente o resumen estructural que consolide una fuente original (como resúmenes jerárquicos de YouTube) debe llevar ESTRICTAMENTE:
```yaml
---
type: "source"
tags: []
---
```
*   **Ubicación:** Estos archivos deben resguardarse en el subdirectorio `20_Atlas/21_MOCs/` para mantener limpio el nivel raíz del Atlas.

## 3. Protocolos Especializados de Ingesta Audiovisual (YouTube)
La transcripción cruda ingresa directamente al `00_Inbox`. El Agente asume toda la responsabilidad del procesamiento:
1.  **Destilación de Ruido (Hierarchical Summary):** El Agente lee la transcripción cruda y genera autónomamente un resumen estructurado, eliminando la "paja".
2.  **Generación MOC:** Este resumen pasará a ser la Nota Fuente (`type: source`). Sobre él, la IA inyectará los vínculos `[[ ]]` señalando las unidades semánticas puras hacia el Atlas.
3.  **Inyección Inversa de Timestamps:** Si un concepto del video afecta a una Unidad Semántica del Atlas, el Agente NO SOLO crea el link en el resumen. El Agente **debe entrar** a la nota del Atlas y agregar una viñeta citando a este nuevo video junto con el Timestamp exacto. Así, las notas del Atlas se convierten en un índice compilado de reproductores directos hacia las fuentes originales.

## 4. Manejo de Contradicciones Semánticas (Dialéctica)
Si al procesar un nuevo Inbox el Agente detecta que un concepto nuevo *contradice directamente* a una Unidad Semántica ya existente en el Atlas:
*   **Regla de Dialéctica:** NUNCA se sobreescribe ni se borra la nota antigua. 
*   **Acción:** El Agente actualiza la Nota Semántica original agregando una sección llamada `## Debates / Contradicciones`. Allí se citan ambas fuentes y se contrastan las dos posturas de forma neutral, permitiendo que la colisión de ideas genere pensamiento crítico.

---
*Directiva V2.0 (GTD-ACCESS). Firmado: Antigravity.*

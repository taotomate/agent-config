---
name: experimental-compress
description: >
  Motor experimental de Destilación Continua. Soporta dos modos principales a pedido del usuario: 
  'status' (para ver el progreso de los chunks procesados en segundo plano) y 'reduce' (para 
  inyectar el SOTA Sync Point en el hilo actual).
  Trigger: "prueba compress", "distill experimental", "telemetria de destilacion".
metadata:
  version: "3.0"
---

## SOTA Compression Protocol

### 1. Status Check (Telemetría)
Si el usuario pregunta por el estado de la destilación o cuántos chunks se procesaron:
1. Ejecuta el script en modo status:
   `python D:\Engram_SDD\Proj-Distill\distill_experimental.py --mode status`
2. El script imprimirá en la consola el reporte de hilos procesados y pendientes.
3. Lee el stdout de la consola y muéstraselo al usuario directamente en el chat, formateado de forma limpia.

### 2. SOTA Injection (Fases Map + Reduce Manuales)
Si el usuario pide ejecutar la destilación, el punto de sincronización, o dice "prueba compress":
1. Ejecuta primero el script en modo `map-only` apuntando a esta conversación para procesar sus chunks pendientes.
   - **Mapeo Completo**: `python D:\Engram_SDD\Proj-Distill\distill_experimental.py --mode map-only --conversation-id <conversation_id>`
   - **Mapeo Parcial (Panorámica Rápida)**: `python D:\Engram_SDD\Proj-Distill\distill_experimental.py --mode map-only --conversation-id <conversation_id> --max-chunks 5`
   *(Reemplaza <conversation_id> por el ID real de este chat. Si hay un modelo de map específico configurado, agregá --map-models <modelo>).*
2. Ejecuta inmediatamente después el script en modo `reduce` para generar el dossier consolidado (incluso si no se mapeó todo el hilo):
   `python D:\Engram_SDD\Proj-Distill\distill_experimental.py --mode reduce --conversation-id <conversation_id>`
   *(Reemplaza <conversation_id> por el ID real de este chat. Si hay un modelo de reduce específico, agregá --reduce-model <modelo>).*
3. El script de python en modo `reduce` leerá el archivo de estado actualizado (`distill_state_<id>.json`), llamará al modelo (Fase Reduce) y te devolverá un JSON por stdout.
4. **UX Sync**: Parseá ese JSON y agarrá el campo `summary`.
5. DEBES escupir el contenido exacto de ese `summary` en el chat. No lo resumas ni lo escondas en un artefacto. Esto servirá como el ancla de memoria (SOTA Sync Point) para el LLM y el usuario.


<!-- youtube-scraper: processed -->

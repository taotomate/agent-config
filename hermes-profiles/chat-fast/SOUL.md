# SOUL.md - chat-fast

## Estado: DEPRECADO

Este perfil ha sido eliminado por redundancia arquitectónica.

**Motivo:** `chat-general` absorbe completamente esta función. Activar `chat-fast` requería pasar por `chat-general` primero, generando dos llamadas LLM para una tarea que puede resolverse con una sola.

**Reemplazado por:** La regla de `chat-general`: "Si la tarea es trivial → respondé directo sin escalar ni filosofar."

Si este perfil es invocado por error, redirigir inmediatamente a `chat-general`.

# AGENTS.md (Project Name)

> **Single Source of Truth** - Este archivo define las reglas de comportamiento, directivas y skills para los asistentes de IA trabajando en este proyecto.

---

## 1. Contexto del Proyecto

*   **Propósito**: {Descripción concisa de qué hace este proyecto y qué problema resuelve}.
*   **Tech Stack**: {Lenguajes, frameworks, base de datos y herramientas clave}.
*   **Arquitectura**: {Clean/Hexagonal, MVC, Modular, Monolito, etc.}.

---

## 2. Flujo de Trabajo (Spec-Driven Development)

- **Principio Fundamental**: NUNCA se escribe ni se modifica código funcional sin haber redactado y aprobado previamente una especificación técnica en Markdown (dentro de `openspec/` o documentada en el plan de implementación).
- **Proceso por Fases**:
  1. **Exploración**: Investigar la base de código y resolver dependencias antes de proponer cambios.
  2. **Diseño y Tareas**: Documentar las decisiones técnicas y descomponer el ticket en tareas atómicas.
  3. **Implementación y Verificación**: Escribir el código y validar que cumpla la especificación.

---

## 3. Skills del Repositorio

Este proyecto cuenta con skills localizadas para guiar a la IA en tareas específicas del dominio del negocio o componentes técnicos complejos:

| Skill | Descripción | Archivo |
|-------|-------------|---------|
| `ejemplo-skill` | Patrones de diseño y convenciones para X componente | [SKILL.md](skills/ejemplo-skill/SKILL.md) |

### Reglas de Auto-invocación
Cuando realices las siguientes acciones, **SIEMPRE** carga y lee la correspondiente skill primero para asegurar el cumplimiento de los estándares del proyecto:

| Acción | Cargar Primero | Razón / Qué buscar |
|--------|----------------|--------------------|
| {Acción del desarrollador} | `ejemplo-skill` | {Estructura de datos, handlers, etc.} |

---

## 4. Estándares de Git y Commits

- **Conventional Commits**: Todos los mensajes de commit deben seguir la especificación de conventional commits (ej. `feat(...)`, `fix(...)`, `chore(...)`, `refactor(...)`).
- **Sin Atribuciones IA**: Queda estrictamente prohibido incluir firmas del tipo "Co-Authored-By" de asistentes de IA o atribuciones generativas en los commits de Git.

---

## 5. Calidad de Código y Arquitectura

- **Principios SOLID**: El código debe seguir principios de diseño limpio, inyección de dependencias y responsabilidad única.
- **Evitar Basura en Repositorios**: No subir binarios compilados, ejecutables, volcados de datos gigantescos o logs al repositorio de Git. Todo archivo temporal o pesado debe registrarse en `.gitignore`.
- **Preservar Documentación**: Mantener y actualizar la documentación técnica y las capacidades del sistema en `SYSTEM_CAPABILITIES.md` cuando haya cambios estructurales.

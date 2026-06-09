# Reglas del Proyecto (GGA Configuration)

Este documento contiene las reglas de desarrollo y estándares de calidad del proyecto. El asistente virtual y el pipeline de CI/CD (GGA) auditarán las contribuciones basándose en estas directrices.

---

## 1. Flujo de Trabajo (Spec-Driven Development)
- **Principio Fundamental**: NUNCA se escribe ni se modifica código funcional sin haber redactado y aprobado previamente una especificación técnica en Markdown (dentro de `openspec/` o documentada en el plan).
- **Proceso por Fases**:
  1. **Exploración**: Investigar la base de código y resolver dependencias antes de proponer cambios.
  2. **Diseño y Tareas**: Documentar las decisiones técnicas y descomponer el ticket en tareas atómicas.
  3. **Implementación y Verificación**: Escribir el código y validar que cumpla la especificación.

---

## 2. Estándares de Git y Commits
- **Conventional Commits**: Todos los mensajes de commit deben seguir la especificación de conventional commits (ej. `feat(...)`, `fix(...)`, `chore(...)`, `refactor(...)`).
- **Sin Atribuciones IA**: Queda estrictamente prohibido incluir firmas del tipo "Co-Authored-By" de asistentes de IA o atribuciones generativas en los commits de Git.

---

## 3. Calidad de Código y Arquitectura
- **Principios SOLID**: El código debe seguir principios de diseño limpio, inyección de dependencias y responsabilidad única.
- **Evitar Basura en Repositorios**: No subir binarios compilados, ejecutables, volcados de datos gigantescos (`.har`, `.json` de dumps) o logs al repositorio de Git. Todo archivo temporal o pesado debe registrarse en `.gitignore`.
- **Preservar Documentación**: Mantener y actualizar la documentación técnica y las capacidades del sistema en `SYSTEM_CAPABILITIES.md` cuando haya cambios estructurales.

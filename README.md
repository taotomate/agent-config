# agent-config

Fuente de verdad de configuración de agentes IA (Antigravity, Gemini CLI, Claude Code, Hermes).

Usar este repositorio para alinear todos los agentes bajo la misma lógica, protocolos y skills.

## Estructura

```
agent-config/
├── shared/               # Archivos compartidos entre todos los agentes
│   ├── agents.md         # Instrucciones base del agente (v4.5)
│   ├── VISION.md         # Filosofía y principios del sistema (v3.2)
│   ├── routing.md        # Decisión de modelos por capa
│   ├── engram-convention.md      # Convención de naming para artifacts en Engram
│   ├── persistence-contract.md   # Contrato de persistencia SDD
│   ├── openspec-convention.md    # Estructura de directorios OpenSpec
│   ├── sdd-phase-common.md       # Protocolo común a todas las fases SDD
│   ├── skill-resolver.md         # Protocolo de resolución de skills
│   └── distillation-protocol.md  # Protocolo de destilación de conversaciones
├── skills/               # Skills del sistema
│   ├── sdd-init/         # Inicializar SDD en un proyecto
│   ├── sdd-explore/      # Fase de exploración
│   ├── sdd-propose/      # Fase de propuesta
│   ├── sdd-spec/         # Fase de especificaciones
│   ├── sdd-design/       # Fase de diseño
│   ├── sdd-tasks/        # Fase de tareas
│   ├── sdd-apply/        # Fase de implementación
│   ├── sdd-verify/       # Fase de verificación
│   ├── sdd-archive/      # Fase de archivo
│   ├── sdd-onboard/      # Onboarding guiado
│   ├── sdd-telemetry/    # Telemetría de tokens
│   ├── sdd-local-distiller/ # Destilación vía LLM local
│   ├── branch-pr/        # Workflow de PRs
│   ├── issue-creation/   # Workflow de issues
│   ├── skill-creator/    # Creador de skills
│   ├── skill-registry/   # Registro de skills
│   ├── conversation-distillation/ # Destilación de conversaciones
│   ├── double-blind-review/       # Revisión adversarial paralela
│   ├── dual-execution-validation/ # Validación dual Cloud vs Local
│   ├── go-testing/       # Patterns de testing en Go
│   └── experimental-compress/     # Motor experimental de destilación
└── project-templates/    # Templates para proyectos nuevos
    └── AGENTS.md         # Template de AGENTS.md para proyectos
```

## Uso

Cuando instales un agente nuevo (Antigravity CLI, Hermes, Cloud, etc.), cloná este repo y apuntale la ruta de configuración.

## Versiones

- agents.md: v4.5
- VISION.md: v3.2
- Skills SDD: v3.0 (apply, verify), v2.0 (resto)

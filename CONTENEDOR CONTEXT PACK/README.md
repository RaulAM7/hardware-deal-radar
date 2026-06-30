# Hardware Deal Radar

Radar interno de oportunidades de compra para hardware profesional usado/reacondicionado en eBay Europa.

Este repositorio nace con una doble finalidad:

1. Construir una herramienta real para detectar gangas de portátiles business, inicialmente ThinkPad, con foco en equipos útiles para desarrollo intensivo con IA, múltiples sesiones de Codex/Claude Code, worktrees, navegador, servicios locales y multitarea pesada.
2. Servir como experimento de ejecución agentic **B-shot**:
   - `/goal` 1: convertir el contexto estratégico y técnico en specs completas.
   - `/goal` 2: implementar el sistema completo siguiendo esas specs.

## Estado actual

Este repo empieza como **context pack**. Todavía no contiene implementación funcional. La prioridad inicial es que el contexto esté suficientemente claro para que una sesión de Codex en modo planning genere specs implementables sin volver a rediseñar el producto.

## Decisiones cerradas v1

- Lenguaje: Python 3.12+
- Persistencia: SQLite
- Configuración: YAML
- Interfaz: CLI
- Fuente principal: eBay Browse API oficial
- Alertas: Telegram + email digest
- Scheduling: systemd timer cada 6 horas
- Deployment: VPS con venv + systemd
- Docker: opcional/documentado, no obligatorio
- Scope inicial: ThinkPad
- Mercados iniciales: eBay España, Alemania, Italia y Reino Unido
- UK: penalizado por aduanas, fricción y riesgo de coste total
- RAM mínima: 32 GB
- RAM ideal: 64 GB
- Scoring: determinista, sin IA generativa en v1
- Scraping: fuera de v1
- Frontend web: fuera de v1
- Compra automática: fuera de v1

## Estructura prevista

```txt
hardware-deal-radar/
  README.md
  docs/
  codex/
  specs/
  config/
  src/
  tests/
  scripts/
  data/
```

## Flujo funcional esperado

```txt
YAML searches
    ↓
CLI / scheduled run
    ↓
eBay Browse API
    ↓
normalización
    ↓
deduplicado SQLite
    ↓
estimación coste total
    ↓
scoring determinista
    ↓
alerta Telegram si hay ganga fuerte
    ↓
email digest si hay candidatos interesantes
    ↓
histórico consultable por CLI
```

## Próximo paso agentic

Ejecutar el contenido de `codex/goal-01-planning.md` en una sesión de Codex/agent planner.

Ese primer goal no debe implementar código. Debe generar specs detalladas en `specs/` y un plan de implementación en `codex/implementation-plan.md`.

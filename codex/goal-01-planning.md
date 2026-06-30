# Goal 01 — Planning and Specs

```txt
/goal

Actúa como arquitecto técnico senior, product engineer y planning agent para el proyecto `hardware-deal-radar`.

Tu objetivo NO es implementar todavía.

Tu objetivo es transformar todo el contexto existente del repositorio en un paquete completo de planificación, especificación y ejecución para que una futura sesión agentic pueda implementar el sistema de principio a fin con mínima intervención humana.

Debes leer obligatoriamente:

- README.md
- docs/*
- codex/agent-rules.md
- codex/definition-of-done.md
- cualquier fichero de contexto disponible en el repo

Debes producir o completar:

1. Una visión técnica consolidada del sistema.
2. Una arquitectura clara y justificada.
3. Un modelo de datos inicial/refinado.
4. Un diseño de módulos.
5. Un diseño del flujo end-to-end.
6. Una estrategia de integración con eBay Browse API.
7. Una estrategia de configuración de búsquedas.
8. Una estrategia de scoring.
9. Una estrategia de alertas.
10. Una estrategia de persistencia.
11. Una estrategia de despliegue en VPS.
12. Una estrategia de logs, errores y observabilidad mínima.
13. Una lista de specs implementables, numeradas y ordenadas.
14. Criterios de aceptación para cada spec.
15. Un plan de implementación secuencial, sin ambigüedades.
16. Una lista explícita de decisiones cerradas.
17. Una lista explícita de supuestos razonables.
18. Una lista explícita de cosas fuera de alcance.
19. Un checklist final para validar que el repo está preparado para implementación.

Debes generar, como mínimo:

- specs/SPEC-001-project-foundation.md
- specs/SPEC-002-config-system.md
- specs/SPEC-003-ebay-api-integration.md
- specs/SPEC-004-normalization-pipeline.md
- specs/SPEC-005-storage-and-deduplication.md
- specs/SPEC-006-scoring-engine.md
- specs/SPEC-007-alerting-system.md
- specs/SPEC-008-cli-interface.md
- specs/SPEC-009-scheduling-and-vps-deployment.md
- specs/SPEC-010-tests-observability-and-docs.md
- codex/implementation-plan.md
- docs/assumptions.md, si hay supuestos
- docs/technical-decisions.md, si aporta claridad

Reglas:

- No implementes código funcional todavía salvo stubs mínimos si ayudan a estructurar.
- No pidas confirmación salvo bloqueo absoluto.
- Si falta información menor, toma una decisión razonable y documéntala como supuesto.
- No amplíes el alcance del producto.
- No conviertas el sistema en SaaS.
- No diseñes frontend complejo.
- No añadas scraping a v1.
- No añadas IA generativa al núcleo v1.
- Prioriza una implementación funcional, mantenible y desplegable en VPS.
- El resultado debe dejar el repo listo para una segunda sesión `/goal` de implementación.

Definition of Done:

- Existen specs suficientemente detalladas para implementar el sistema completo.
- Cada spec tiene objetivo, alcance, tareas, ficheros afectados, criterios de aceptación y pruebas mínimas.
- Existe un plan de ejecución ordenado.
- Existe documentación suficiente para que otro agente implemente sin volver a preguntar.
- El repo queda preparado para el goal de implementación.
```

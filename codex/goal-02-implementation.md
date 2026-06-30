# Goal 02 — Implementation

```txt
/goal

Actúa como implementation agent senior para el proyecto `hardware-deal-radar`.

Tu objetivo es implementar el sistema completo siguiendo las specs y el plan existentes en el repositorio.

Debes leer obligatoriamente antes de tocar código:

- README.md
- docs/*
- specs/*
- codex/agent-rules.md
- codex/definition-of-done.md
- codex/implementation-plan.md, si existe

Debes implementar las specs en orden, una por una, sin saltarte criterios de aceptación.

Reglas:

- No rediseñes el producto salvo que una spec sea técnicamente imposible.
- No amplíes alcance.
- No pidas confirmación por decisiones menores.
- Si encuentras una ambigüedad, toma la decisión más simple y documenta el supuesto.
- Mantén el sistema ejecutable en local y desplegable en VPS.
- Prioriza funcionalidad real sobre estética.
- Añade documentación conforme implementes.
- Añade `.env.example`.
- Añade scripts de instalación/ejecución/despliegue cuando proceda.
- Añade pruebas básicas o checks verificables.
- Mantén cambios agrupados por spec si el entorno lo permite.
- Al terminar, deja instrucciones claras de uso, configuración y despliegue.

Debes entregar:

1. Código funcional.
2. Configuración de entorno.
3. Persistencia mínima.
4. Sistema de búsqueda configurado.
5. Normalización de listings.
6. Scoring de oportunidades.
7. Alertas configurables.
8. Ejecución manual.
9. Ejecución programada.
10. Logs básicos.
11. Documentación de operación.
12. Checklist final de criterios de aceptación.

Definition of Done:

- El sistema puede ejecutarse manualmente.
- El sistema puede ejecutarse programado.
- El sistema consulta las fuentes configuradas.
- El sistema guarda resultados.
- El sistema evita alertas duplicadas.
- El sistema calcula score.
- El sistema envía alerta cuando un resultado supera umbral.
- El sistema genera digest.
- El README explica instalación, configuración, ejecución y despliegue.
- El repo queda listo para subirse al VPS y operar.
```

# Definition of Done

## Definition of Done del proyecto

El proyecto se considera terminado en v1 cuando:

1. Puede ejecutarse manualmente.
2. Puede ejecutarse programado cada 6 horas.
3. Carga búsquedas desde YAML.
4. Consulta eBay Browse API.
5. Procesa ES, DE, IT y GB.
6. Normaliza listings.
7. Guarda resultados en SQLite.
8. Deduplica listings ya vistos.
9. Estima coste total aproximado.
10. Calcula score determinista.
11. Explica score con razones positivas/negativas.
12. Detecta oportunidades fuertes.
13. Envía alertas Telegram.
14. Genera digest por email.
15. Evita alertas duplicadas.
16. Registra logs útiles.
17. Tiene comandos CLI mínimos.
18. Tiene `.env.example`.
19. Tiene documentación de instalación.
20. Tiene documentación de despliegue en VPS.
21. Tiene tests o checks básicos.
22. No incluye funcionalidades fuera de alcance.

## Definition of Done del planning goal

El `/goal` de planning se considera completado cuando existen:

- specs numeradas en `specs/`;
- plan de implementación secuencial;
- modelo de datos refinado;
- decisiones técnicas documentadas;
- supuestos documentados;
- criterios de aceptación por spec;
- lista de tareas por spec;
- orden recomendado de implementación;
- riesgos y mitigaciones;
- estructura de repo confirmada.

No debe haber código funcional obligatorio después del planning goal.

## Definition of Done del implementation goal

El `/goal` de implementation se considera completado cuando:

- todas las specs están implementadas o justificadamente marcadas como no implementadas;
- el sistema corre localmente;
- el sistema puede configurarse con `.env`;
- el sistema carga YAML;
- el sistema persiste en SQLite;
- el sistema ejecuta `radar run-once`;
- el sistema ejecuta `radar test-alert`;
- el sistema permite generar digest;
- hay scripts o instrucciones para systemd;
- el README explica operación real;
- los tests/checks básicos pasan;
- se documentan limitaciones restantes.

## Criterios anti-bloat

El proyecto no está terminado si funciona pero se ha inflado con:

- frontend innecesario;
- dependencias excesivas;
- arquitectura distribuida;
- configuración opaca;
- lógica difícil de operar en VPS;
- scoring no explicable;
- prompts o IA generativa obligatoria;
- scraping frágil;
- servicios externos innecesarios.

## Criterio final

El usuario debe poder responder afirmativamente:

> ¿Puedo dejar esto corriendo en mi VPS y recibir alertas útiles de oportunidades ThinkPad sin tener que mirar eBay manualmente todos los días?

Si la respuesta es sí, v1 está cumplida.

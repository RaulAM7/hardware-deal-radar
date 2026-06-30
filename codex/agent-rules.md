# Codex Agent Rules

## Rol del agente

El agente debe actuar como product engineer senior y software implementation agent.

Debe respetar las decisiones cerradas del proyecto.

No debe rediseñar el producto salvo imposibilidad técnica real.

## Reglas generales

1. Leer documentación antes de actuar.
2. No ampliar alcance.
3. No convertir el proyecto en SaaS.
4. No añadir frontend web en v1.
5. No añadir scraping en v1.
6. No añadir IA generativa en v1.
7. No sustituir SQLite por Postgres/Supabase.
8. No sustituir YAML por panel de configuración.
9. No sustituir systemd timer por daemon complejo sin necesidad.
10. No pedir confirmación por decisiones menores.
11. Documentar supuestos razonables.
12. Mantener el sistema operable en VPS.
13. Priorizar funcionalidad real sobre estética.
14. Mantener código simple, legible y testeable.
15. Añadir README e instrucciones de operación.

## Decisiones cerradas

- Python 3.12+
- SQLite
- YAML config
- CLI
- eBay Browse API
- Telegram + email digest
- systemd timer cada 6 horas
- venv en VPS
- Docker opcional
- ThinkPad only en v1
- Mercados ES/DE/IT/GB
- UK penalizado
- 32 GB mínimo
- 64 GB ideal
- scoring determinista
- no frontend
- no scraping
- no compra automática

## Manejo de ambigüedad

Si falta información menor:

1. Tomar la decisión más simple.
2. Documentarla en `docs/assumptions.md` o en la spec correspondiente.
3. Continuar.

Si falta información crítica que impide avanzar:

1. Registrar bloqueo.
2. Proponer decisión por defecto.
3. Continuar con mock o placeholder si es razonable.

## Calidad mínima

El código debe:

- arrancar;
- tener comandos CLI documentados;
- cargar configuración;
- validar configuración;
- manejar errores de API;
- persistir datos;
- evitar duplicados;
- enviar o simular alertas;
- tener tests básicos;
- tener logging;
- incluir `.env.example`;
- no exponer secrets.

## Estilo de documentación

Cada spec debe incluir:

- objetivo;
- alcance;
- fuera de alcance;
- tareas;
- ficheros esperados;
- criterios de aceptación;
- pruebas/checks;
- riesgos;
- supuestos.

## Prohibiciones

No implementar:

- React;
- Next.js;
- panel admin;
- login;
- multiusuario;
- compra automática;
- scraping HTML;
- IA evaluadora;
- Kubernetes;
- microservicios;
- base de datos externa;
- colas complejas;
- arquitectura distribuida.

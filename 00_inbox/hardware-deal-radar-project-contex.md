# Hardware Deal Radar — Project Context for Basic Scaffolding

## Uso previsto de este documento

Este documento está pensado como material de entrada para el harness `basic-scaffolding` de Raúl. Debe colocarse en `00_inbox/` antes de ejecutar la skill de context building / initiate context building.

Objetivo del documento: condensar en un único contexto inicial la visión estratégica, el criterio de producto, las decisiones CTO ya cerradas y el prototipado grueso de arquitectura para que el harness pueda permear ese contexto en el resto del repo.

Este documento **no es todavía un blueprint final**, **no es todavía un system design completo** y **no es una spec implementable**. Es el contexto estratégico-técnico fundacional que debe alimentar la fase posterior de planning/specs.

---

# 1. Resumen ejecutivo

## Nombre del proyecto

**Hardware Deal Radar**

## Qué queremos construir

Un radar interno, ejecutado en VPS, para detectar oportunidades reales de compra de portátiles profesionales ThinkPad usados/reacondicionados en eBay Europa.

El sistema debe buscar listings en varios marketplaces europeos, normalizarlos, estimar coste total, penalizar riesgos, calcular un score de oportunidad y avisar a Raúl solo cuando aparezca una ganga que merezca atención.

## Por qué existe

Raúl está valorando sustituir o complementar su equipo actual por un portátil profesional más potente, especialmente con más RAM, para desarrollo, automatizaciones, trabajo con IA, sesiones múltiples de Codex/Claude Code, worktrees, navegador intensivo y operación diaria de negocio.

La alternativa MacBook Air con memoria alta perdió atractivo relativo por subida de precios y por el salto económico que supone entrar en configuraciones con RAM suficiente. Por eso se abre la tesis de buscar un portátil business usado/reacondicionado, especialmente ThinkPad, donde pueden aparecer gangas procedentes de renovaciones de parque empresarial.

## Doble objetivo

Este proyecto tiene dos objetivos simultáneos:

1. **Objetivo funcional:** construir una herramienta útil para detectar oportunidades reales de compra de hardware.
2. **Objetivo metodológico:** usarlo como experimento de construcción agentic B-shot:
   - Shot 1: generar planning/specs detalladas.
   - Shot 2: implementar integralmente el sistema siguiendo las specs.

---

# 2. Decisión estratégica cerrada

## Tesis central

No vamos a construir “un buscador de eBay”. eBay ya permite guardar búsquedas y recibir avisos.

El valor diferencial está en construir una capa inteligente propia que haga lo que eBay no hace suficientemente bien para este caso:

- unificar varios eBay europeos;
- normalizar listings caóticos;
- extraer RAM/CPU/modelo/SSD/teclado cuando sea posible;
- calcular coste total aproximado;
- penalizar riesgos por vendedor, país, aduanas, teclado o estado;
- deduplicar;
- guardar histórico;
- detectar bajadas de precio;
- calcular score determinista;
- generar alerta accionable, no ruido.

## Qué debe responder el sistema

El sistema debe ayudar a contestar:

- ¿Ha aparecido una oportunidad real?
- ¿Merece que Raúl la mire ahora?
- ¿Qué tan buena es?
- ¿Por qué tiene ese score?
- ¿Qué riesgos tiene?
- ¿Cuál es el coste total aproximado?
- ¿Ya se alertó antes?
- ¿Ha cambiado el precio?
- ¿Encaja con el criterio de compra definido?

## Principio rector

**Alertar poco, pero alertar bien.**

Un radar que avisa de todo fracasa. Un radar que avisa solo cuando hay señal real tiene valor.

---

# 3. Contexto del usuario y caso de uso

## Perfil operativo de Raúl

Raúl trabaja en desarrollo de negocio, estrategia, preventa, producto, automatizaciones y soporte técnico-operativo para Skilland/Reboot/Edukami. Su flujo real combina:

- investigación;
- redacción de propuestas;
- análisis de proyectos;
- trabajo con CRM;
- automatizaciones;
- documentación;
- sesiones múltiples de IA;
- Codex/Claude Code;
- edición de repos;
- despliegues en VPS;
- trabajo con herramientas agentic;
- programación progresivamente más intensa.

## Problema hardware actual

El equipo actual de Raúl tiene 16 GB de RAM. Aunque es competente, puede quedarse corto para:

- muchas pestañas de navegador;
- sesiones concurrentes de Codex/Claude Code;
- varios repos/worktrees;
- Docker/servicios locales;
- herramientas de automatización;
- procesos de desarrollo y documentación abiertos a la vez.

El salto deseado no es cosmético. Cambiar de equipo solo tiene sentido si hay una mejora clara.

## Criterio de compra

No se comprará por ansiedad. El radar debe permitir esperar hasta que aparezca una oportunidad objetiva.

---

# 4. Criterios de compra del portátil

## Mínimo absoluto

- 32 GB RAM mínimo.
- CPU claramente útil y superior al umbral actual de trabajo.
- SSD mínimo 512 GB.
- Chasis profesional/business.
- No gamer.
- Peso y formato razonables.
- Buen teclado.
- Buen soporte Linux.
- Vendedor fiable.
- Precio suficientemente atractivo para justificar comprar usado/reacondicionado.

## Ideal

- 64 GB RAM.
- SSD 1 TB.
- CPU moderna eficiente: Ryzen 7 PRO / Intel i7-i9 moderno o equivalente.
- ThinkPad de gama T/P/X1 Extreme/P14s.
- Vendedor profesional/business.
- Buen feedback.
- Devolución o garantía.
- Mercado UE.
- Precio total claramente competitivo.

## Familias objetivo v1

V1 se limita a **ThinkPad**.

Modelos prioritarios:

- ThinkPad P14s.
- ThinkPad T14.
- ThinkPad T16.
- ThinkPad P1.
- ThinkPad X1 Extreme.

## Fuera de prioridad

- Equipos con menos de 32 GB RAM.
- Equipos gamer.
- Workstations demasiado pesadas/calientes salvo ganga extrema.
- Equipos muy antiguos.
- Listings “for parts”, “defect”, “broken”, “spare”, “sin RAM”, “sin disco”.
- Vendedores débiles.
- Equipos sin devolución y con descripción pobre.

---

# 5. Alcance funcional v1

## Incluido

- Consulta de eBay Browse API oficial.
- Marketplaces iniciales:
  - eBay España.
  - eBay Alemania.
  - eBay Italia.
  - eBay Reino Unido.
- Solo ThinkPad en v1.
- Configuración por YAML.
- Persistencia SQLite.
- CLI.
- Scoring determinista.
- Deduplicado.
- Histórico de listings.
- Alertas Telegram.
- Digest por email.
- Ejecución manual.
- Ejecución programada cada 6 horas.
- Despliegue VPS-first con venv + systemd timer.
- Docker solo opcional/documentado.
- Modo mock/dry-run/noop para evitar bloqueos por credenciales o dependencias externas.

## No incluido en v1

- Frontend web.
- Panel React/Next.
- Login.
- SaaS.
- Multiusuario.
- Compra automática.
- Scraping HTML agresivo.
- IA generativa en el núcleo del scoring.
- Postgres/Supabase.
- Kubernetes.
- Microservicios.
- App móvil.
- WhatsApp.
- Integración con Wallapop, Milanuncios, BackMarket, Amazon Renewed u otros marketplaces.
- Comparador perfecto de precios históricos.
- Cálculo fiscal exacto de aduanas/IGIC.

---

# 6. Decisiones CTO cerradas

## Stack v1

- Python 3.12+.
- SQLite.
- YAML config.
- CLI.
- eBay Browse API oficial.
- Telegram alerts.
- Email digest.
- systemd timer cada 6 horas.
- venv en VPS.
- Docker opcional/documentado, no obligatorio.

## Librerías candidatas

- Typer para CLI.
- Pydantic para settings/modelos.
- httpx para APIs.
- PyYAML para configuración.
- SQLModel o SQLAlchemy ligero para SQLite.
- Rich para output en terminal.
- pytest para tests básicos.
- ruff para lint/format.

## Decisiones específicas

- Lenguaje: Python, no TypeScript.
- Base de datos: SQLite, no Postgres.
- Configuración: YAML, no panel.
- Interfaz: CLI, no frontend.
- Fuente: eBay Browse API oficial, no scraping.
- Alertas: Telegram + email digest.
- Frecuencia: cada 6 horas.
- Alcance de marcas: solo ThinkPad en v1.
- Mercados: ES/DE/IT/GB.
- UK: permitido, pero penalizado por aduanas/riesgo.
- Teclado extranjero: penalizado, no descartado automáticamente.
- Scoring: determinista, explicable, sin LLM en v1.
- Deployment: VPS con venv + systemd timer.
- Docker: opcional como documentación/futuro, no dependencia de operación.

---

# 7. Arquitectura gruesa candidata

## Flujo funcional

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

## Componentes conceptuales

```txt
hardware-deal-radar/
  config/
    searches.yaml
    scoring.yaml
    marketplaces.yaml

  src/
    hardware_deal_radar/
      cli.py
      settings.py

      sources/
        base.py
        ebay_client.py

      pipeline/
        fetch.py
        normalize.py
        deduplicate.py
        enrich.py
        score.py

      storage/
        db.py
        listings_repo.py
        alerts_repo.py
        runs_repo.py

      alerts/
        telegram.py
        email.py
        formatter.py

      reports/
        daily_digest.py

      utils/
        money.py
        logging.py
        text_parsing.py

  tests/
  scripts/
  data/
  docs/
  specs/
  codex/
```

## Comandos CLI esperados

- `radar run-once`
- `radar run-once --mock --dry-run`
- `radar digest`
- `radar digest --dry-run`
- `radar test-alert`
- `radar test-alert --dry-run`
- `radar list-recent`
- `radar explain-score <listing_id>`
- `radar validate-config`
- `radar show-config`
- `radar doctor`

## Modos de ejecución

El sistema debe contemplar:

- **real mode:** usa eBay, Telegram y SMTP reales.
- **mock mode:** usa fixtures locales sin credenciales.
- **dry-run mode:** ejecuta pipeline sin enviar alertas reales.
- **noop mode:** sustituye Telegram/email por consola o archivo.

Esto es crítico para que el agente de implementación no se bloquee si faltan credenciales, si una API falla o si el entorno todavía no está listo.

---

# 8. Modelo de datos grueso

## Entidades principales

### Run

Una ejecución del radar.

Campos esperados:

- id;
- started_at;
- finished_at;
- status;
- marketplaces_checked;
- searches_checked;
- listings_found;
- listings_new;
- alerts_sent;
- errors_count.

### Listing

Identidad estable de un listing observado.

Campos esperados:

- id;
- source;
- source_item_id;
- marketplace;
- title;
- url;
- seller_username;
- first_seen_at;
- last_seen_at;
- last_score;
- last_total_estimated_cost;
- last_status.

### ListingSnapshot

Estado observado de un listing en una ejecución concreta.

Campos esperados:

- id;
- listing_id;
- run_id;
- observed_at;
- title;
- price_amount;
- price_currency;
- shipping_amount;
- total_estimated_cost_eur;
- condition;
- location_country;
- seller_feedback_score;
- seller_feedback_percentage;
- seller_account_type;
- inferred_model;
- inferred_ram_gb;
- inferred_ssd_gb;
- inferred_cpu;
- inferred_keyboard;
- score;
- score_reasons_json;
- risk_reasons_json;
- raw_json.

### Alert

Alerta enviada o simulada.

Campos esperados:

- id;
- listing_id;
- snapshot_id;
- channel;
- alert_type;
- sent_at;
- score;
- message_preview;
- status.

### PriceChange

Cambio relevante de precio.

Campos esperados:

- id;
- listing_id;
- old_total_estimated_cost_eur;
- new_total_estimated_cost_eur;
- delta;
- detected_at.

### ErrorLog

Error ocurrido en una ejecución.

Campos esperados:

- id;
- run_id;
- source;
- marketplace;
- error_type;
- message;
- created_at.

---

# 9. Scoring determinista

## Objetivo

Asignar un score de 0 a 100 que indique si un listing merece atención.

El score debe ser explicable. Cada puntuación debe ir acompañada de:

- razones positivas;
- riesgos;
- campos inferidos;
- campos desconocidos;
- motivo de alerta o no alerta.

## Bloques de scoring propuestos

### RAM

- 64 GB o más: muy positivo.
- 32 GB: positivo.
- Menos de 32 GB: descartar o score muy bajo.
- RAM desconocida: penalizar incertidumbre.

### CPU

- CPU moderna alta/PRO eficiente: positivo fuerte.
- CPU moderna media: positivo.
- CPU antigua usable: leve.
- CPU vieja o débil: penalización.
- CPU desconocida: penalización leve/moderada.

### Modelo

- P14s/T14/T16 moderno: positivo fuerte.
- P1/X1 Extreme moderno: positivo, pero vigilar calor/peso.
- ThinkPad válido menos prioritario: positivo leve.
- Modelo desconocido: neutro o penalización leve.

### Precio total estimado

Debe considerar:

- precio;
- envío;
- penalización UK/no UE;
- incertidumbre de aduanas/gestión;
- comparación contra umbrales configurados.

### Vendedor

- Business/profesional con feedback alto: positivo fuerte.
- Feedback alto: positivo.
- Feedback medio: leve.
- Feedback bajo/desconocido: penalización.

### Mercado

- ES: positivo.
- DE: positivo.
- IT: levemente positivo.
- GB: penalización por riesgo/aduanas/devolución.

### Teclado

- Español: positivo.
- Inglés: casi neutro/positivo leve.
- Alemán/italiano/francés: penalización moderada.
- Desconocido: penalización leve.

### Riesgos

Penalizar:

- batería no verificada;
- sin cargador;
- pantalla dañada;
- BIOS bloqueada;
- descripción incompleta;
- precio sospechosamente bajo;
- UK sin coste claro;
- vendedor débil;
- “for parts” / “defect” / “broken”.

## Umbrales iniciales

- Score >= 80: alerta fuerte Telegram.
- Score 65-79: digest email.
- Score < 65: guardar histórico, no alertar.

---

# 10. Estrategia de alertas

## Principio

La alerta debe ser una ficha de decisión, no un simple link.

## Alerta Telegram

Se envía cuando un listing supera el umbral fuerte.

Debe incluir:

- título;
- modelo inferido;
- RAM;
- SSD;
- CPU;
- marketplace;
- país;
- vendedor;
- feedback;
- tipo de vendedor si está disponible;
- precio;
- envío;
- coste total estimado;
- score;
- razones positivas;
- riesgos;
- link.

## Digest email

El digest debe agrupar candidatos interesantes, pero no urgentes.

Debe incluir:

- nuevos candidatos medianos;
- listings fuertes si no se pudo mandar Telegram;
- bajadas de precio relevantes;
- resumen de ejecución.

## Anti-duplicado

No alertar dos veces por el mismo listing salvo:

- bajada de precio significativa;
- score sube por encima de umbral fuerte;
- reaparece tras tiempo relevante;
- hay cambio significativo en datos clave.

---

# 11. Credenciales y secretos

## Regla principal

No commitear secretos.

El archivo `.env` debe vivir en la raíz del repo, pero debe estar incluido en `.gitignore`.

## Variables esperadas

```env
EBAY_ENV=production
EBAY_CLIENT_ID=
EBAY_CLIENT_SECRET=
EBAY_SCOPE=https://api.ebay.com/oauth/api_scope

TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=

SMTP_HOST=
SMTP_PORT=587
SMTP_USERNAME=
SMTP_PASSWORD=
SMTP_FROM=
DIGEST_EMAIL_TO=

RADAR_ENV=production
RADAR_DB_PATH=./data/radar.sqlite
RADAR_LOG_LEVEL=INFO
```

## Estrategia para Codex/agentes

El agente debe asumir que las credenciales se leen desde `.env`, pero nunca debe:

- pedir que se peguen secretos en el prompt;
- escribir secretos en documentación;
- volcar secretos en logs;
- crear tests con secretos reales;
- commitear `.env`.

## Validación esperada

Debe existir un comando `radar doctor` que valide:

- presencia de `.env`;
- variables requeridas;
- acceso a eBay si se ejecuta en modo real;
- token Telegram si se ejecuta en modo real;
- capacidad de envío email si está activado;
- DB accesible;
- config YAML válida;
- permisos razonables.

---

# 12. Protocolo anti-bloqueos para implementación agentic

## Problema

El segundo shot de implementación puede encontrarse con dependencias humanas o externas:

- falta token Telegram;
- falta client secret eBay;
- eBay API falla;
- SMTP no configurado;
- systemd no disponible en entorno de desarrollo;
- red no disponible;
- credenciales inválidas;
- límites de API;
- permisos de VPS.

## Decisión

Ninguna dependencia externa puede bloquear la implementación.

Si falta algo, el agente debe:

1. implementar el adaptador real;
2. implementar mock/noop equivalente;
3. añadir dry-run;
4. añadir validación en `radar doctor`;
5. documentar acción humana pendiente;
6. continuar con el resto de specs.

## Regla para `/goal 02`

No detener la implementación por ausencia de credenciales reales.

El sistema debe poder funcionar al menos con:

```bash
radar run-once --mock --dry-run
radar test-alert --dry-run
radar digest --dry-run
radar doctor
```

---

# 13. Método B-shot del proyecto

## Fase 0 — Context building

Colocar este documento en `00_inbox/` del harness.

Ejecutar la skill de context building para permear el contexto en el repo.

## Fase 1 — Planning/specs

Ejecutar un `/goal` de planning.

Objetivo: convertir este contexto y los documentos derivados en specs implementables.

El agente debe generar, como mínimo:

- specs numeradas;
- plan de implementación;
- decisiones cerradas;
- supuestos;
- fuera de alcance;
- modelo de datos detallado;
- arquitectura final;
- criterios de aceptación;
- pruebas/checks por spec;
- riesgos y mitigaciones.

Specs esperadas:

- Project Foundation.
- Configuration System.
- eBay Browse API Client.
- Domain Models and Normalization.
- SQLite Persistence.
- Deduplication.
- Scoring Engine.
- Telegram Alerts.
- Email Digest.
- CLI.
- VPS Deployment and systemd Timer.
- Logging and Observability.
- Tests and Quality Checks.
- Documentation and Runbook.

## Fase 2 — Implementation

Ejecutar un `/goal` de implementación.

Objetivo: implementar el sistema completo siguiendo specs, sin rediseñar el producto.

## Fase 3 — Operación

En VPS:

- configurar `.env`;
- ejecutar `radar doctor`;
- ejecutar `radar run-once --dry-run`;
- probar Telegram;
- probar digest;
- activar systemd timer;
- revisar logs;
- dejar corriendo cada 6 horas.

---

# 14. Reglas para agentes

## Hacer

- Leer todo el contexto antes de actuar.
- Mantener el scope cerrado.
- Priorizar una herramienta funcional y operable.
- Usar configuración YAML.
- Mantener SQLite.
- Mantener CLI.
- Implementar mocks/dry-run/noop.
- Documentar supuestos.
- Añadir tests básicos.
- Añadir runbook.
- Añadir `.env.example`.
- Asegurar que `.env` está en `.gitignore`.

## No hacer

- No convertirlo en SaaS.
- No crear frontend web.
- No introducir React/Next.
- No añadir Postgres/Supabase.
- No añadir scraping HTML en v1.
- No meter IA generativa en scoring v1.
- No crear compra automática.
- No pedir confirmación por decisiones menores.
- No bloquearse por credenciales.
- No loggear secretos.
- No commitear `.env`.

---

# 15. Definition of Done de alto nivel

El proyecto estará listo cuando:

- se pueda instalar en el VPS;
- exista CLI funcional;
- exista configuración YAML;
- exista `.env.example`;
- exista validación de configuración;
- exista SQLite con persistencia;
- se puedan consultar fuentes reales o mock;
- se normalicen listings;
- se dedupliquen;
- se calcule score;
- se expliquen razones/riesgos;
- se envíe Telegram en modo real;
- se simule Telegram en dry-run;
- se genere digest email;
- se eviten alertas duplicadas;
- se pueda ejecutar programado cada 6 horas;
- existan logs útiles;
- existan tests/checks mínimos;
- README/runbook expliquen instalación, operación y troubleshooting.

---

# 16. Estado de madurez de este documento

Este documento debe tratarse como:

- contexto estratégico;
- product framing;
- decisiones CTO cerradas;
- arquitectura en pincelada gruesa;
- input para planning/specs.

No debe tratarse como:

- blueprint final;
- contrato técnico completo;
- implementación directa;
- sustituto de specs.

La siguiente fase debe convertir este contexto en un diseño ejecutable por specs.
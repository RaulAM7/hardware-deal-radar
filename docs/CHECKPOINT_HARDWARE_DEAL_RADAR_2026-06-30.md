# Hardware Deal Radar — Checkpoint técnico y próximos milestones

## 1. Resumen ejecutivo

Hardware Deal Radar ya es un CLI funcional que carga `.env`, valida YAML, consulta eBay Browse API real, persiste resultados en SQLite y permite inspección por `list-recent` y `explain-score`.

La base activa contiene evidencia clara de funcionamiento real: `348` listings persistidos, `0` errores en la última ejecución `dry_run`, y distribución por marketplace en `ES/DE/IT/GB`.

El sistema no está listo para producción real continua. El problema principal no es de infraestructura sino de calidad de datos y calibración de reglas: están entrando componentes RAM, placas base y listings fuera de rango; además el parser pierde CPU modernas, teclado y parte del mapeo de vendedor business.

El scoring actual contiene daño parcialmente, pero no lo suficiente: `325/348` listings acaban en `reject`, `15` en `ignore`, `8` en `watch`, y no hay `strong_candidate` real en la DB activa. Aun así, dos placas base llegaron a `watch`, lo que ya invalida activar digest o scheduler sin una fase intermedia de limpieza.

`--dry-run` está bien orientado para pruebas seguras: persiste DB y runs, llama a eBay real si no se usa `--mock`, y simula outbound con `NoopAlerter` en vez de mandar Telegram/email reales.

Telegram existe y hay evidencia externa de al menos una alerta visual, pero el código muestra que `doctor` no comprueba el canal de verdad; solo reporta presencia de credenciales. SMTP sigue vacío, así que email digest real no está operativo.

La recomendación técnica es no activar `systemd` todavía. El siguiente paso correcto es una fase explícita de “Data Quality & Scoring Calibration” antes de cualquier modo semi-productivo.

## 2. Objetivo original del proyecto

El objetivo reconstruido desde el repo, las specs y la configuración es:

- construir un radar CLI para detectar oportunidades de compra de hardware usado/reacondicionado en eBay Europa;
- priorizar ThinkPads y workstations/laptops business relacionadas;
- cargar búsquedas desde YAML;
- consultar eBay Browse API oficial;
- normalizar listings;
- estimar coste total en EUR;
- puntuar de forma determinista y explicable;
- persistir histórico en SQLite;
- generar digest y alertas Telegram;
- operar en VPS con `uv`, `.env`, y systemd timer cuando la calidad de señal sea suficiente.

## 3. Camino recorrido

| hito | estado | evidencia | confianza | pendiente |
| --- | --- | --- | --- | --- |
| scaffold repo/CLI | hecho | `pyproject.toml`, entrypoint `radar`, `uv run radar --help` OK | alta | ninguna |
| config/.env | hecho | `radar doctor` muestra `.env` presente y `config valid` | alta | mantener sin exponer secretos |
| permisos/seguridad básica | hecho | `.env` con `0o600`, `.gitignore` y docs de seguridad | alta | falta política formal de rotación/backup |
| mock pipeline | hecho | backup mock con runs `mock,dry_run`, `48` raw, `4` strong simulated | alta | usarlo para tests de regresión nuevos |
| scoring mock | hecho | `test-alert --dry-run`, `digest --dry-run`, tests `pytest -q` | alta | calibrar contra datos reales |
| Telegram bot | parcialmente hecho | evidencia externa de alerta visual; código `TelegramAlerter` existe | media | falta smoke test trazable en DB activa sin dry-run |
| eBay credentials | hecho | `doctor` muestra `EBAY_CLIENT_ID/SECRET <set>` | alta | falta verificación explícita en `doctor` |
| eBay real dry-run | hecho | run activo `mode=dry_run`, `raw_results_count=357`, `new=348`, `errors=0` | alta | repetir tras ajustes de filtros |
| SQLite persistence | hecho | `data/radar.sqlite`, schema válido, `348` listings, `348` rows en `price_history` | alta | definir backup/retention |
| list-recent/explain-score | hecho | comandos ejecutados; `explain-score 348` devuelve razones y riesgos | alta | corregir visualización de score `0` como `n/a` |
| digest dry-run | hecho | comando funciona; backup mock registra digest `simulated` | media | alinear threshold de digest con recomendaciones |
| systemd/timer | preparado, no activado | scripts y templates existen en `scripts/systemd/` | alta | no activar hasta cerrar calidad de datos |

## 4. Estado actual por componente

| componente | funciona | evidencia | problemas | siguiente acción |
| --- | --- | --- | --- | --- |
| CLI | sí | `radar --help`, `list-recent`, `explain-score`, `doctor`, `validate-config` | salida de score `0` aparece como `n/a` | corregir presentación y añadir smoke checks más precisos |
| Config | sí | YAML runtime y ejemplo; `validate-config` OK | no hay filtros ricos por categoría/scope | ampliar schema con exclusiones/categorías |
| eBay client | sí | real dry-run con `357` raw y `0` errores | solo usa `q` + `limit=25`; sin categoría, sin paginación, sin buying filters | endurecer request a Browse API |
| Normalizer/parser | parcialmente | datos poblados en SQLite | seller business roto, CPU moderna perdida, teclado nulo, familias incompletas, RAM/SSD frágil | fase dedicada de data quality |
| Scoring | parcialmente | `325 reject`, `8 watch`, casos explicables | watch falsos positivos; digest inconsistente con threshold por search | recalibrar score y jerarquía de filtros |
| SQLite | sí | schema válido, `runs/listings/price_history/alerts/error_logs` | backup/retention no definido; item-group duplicates no tratados | definir política y mejorar dedup semántico |
| Telegram | parcialmente | adapter real existe; evidencia externa de test visual | `doctor` no valida conectividad; no hay prueba controlada trazable en DB activa | primer test real controlado después de M2.5 |
| Email/SMTP | no | `SMTP_* <empty>` en `doctor` | digest real no operativo | decidir si entra en siguiente hito o se difiere |
| Digest | parcialmente | `digest --dry-run` funciona | usa threshold global `60`, no el threshold por search; puede incluir `ignore` | alinear selección con recomendación final |
| Scheduling/systemd | preparado | scripts y unit/timer presentes | no calibrado para uso real; no activado | dejar para después de la primera alerta controlada |
| Tests | sí, pero cortos | `27 passed in 2.48s` | faltan regresiones del mundo real (Ultra, Ryzen AI, T14s, sellerAccountType, motherboards, RAM-only) | ampliar suite con fixtures reales |
| Observabilidad/logs | básica | logs de inicio/fin de run, doctor, digest, test-alert | `doctor` superficial; no hay resumen de calidad/riesgo | añadir checks de readiness reales y reporting más útil |

## 5. Lectura de resultados reales

### Qué tipo de resultados están entrando

En la DB actual entran tres grupos:

1. ThinkPads/laptops reales potencialmente interesantes.
2. ThinkPads/workstations muy caras y fuera de rango.
3. Falsos positivos de componentes y accesorios:
   - RAM/SODIMM/DDR4/DDR5.
   - placas base (`motherboard`, `placa madre`, `scheda madre`).
   - accesorios puntuales (`dock`, `SSD suelta`, etc.).

### Cuáles son falsos positivos

Ejemplos claros:

- ID `348`: módulo RAM DDR4 para ThinkPad P1, no portátil completo.
- IDs `3` y `53`: placas base de P14s/P16s, ambas en `watch`.
- ID `198`: otra placa base, `ignore` con score `53`.
- varios listings con `SODIMM`, `DDR4`, `DDR5`, `compatible for`, `for Lenovo`.

### Si el scoring los rechaza bien

Parcialmente.

- El caso `348` se rechaza correctamente (`score=17`, `recommendation=reject`).
- Pero el rechazo llega tarde y con razones positivas que no deberían existir para un componente:
  - `32GB RAM`
  - `target family P1`
  - `seller feedback 99+`
  - `price very competitive`

Esto indica que el scoring está tapando ruido, pero el filtro de entrada y el parser todavía regalan puntos estructurales a listings que nunca debieron ser candidatos de laptop.

### Si el ruido viene de search/filter, parser, scoring o todos

Viene de los tres niveles:

- `search/filter`: el cliente eBay usa solo `q` y `limit`; no hay filtro de categoría laptop ni exclusión server-side.
- `parser`: RAM/SSD/CPU/familia/teclado son demasiado débiles y no distinguen bien componentes frente a portátiles.
- `scoring`: aunque rechaza mucho, todavía permite `watch` a placas base y `ignore` altos a máquinas fuera del target real.

### Qué nos dice el caso ID 348

El ID `348` es un buen test de humo del estado actual:

- positivo: el sistema no lo considera ganga real y lo deja en `reject`;
- negativo: el pipeline lo trató como listing suficientemente parecido a un portátil ThinkPad como para darle puntos de RAM, familia y precio;
- conclusión: la capa de exclusión debe endurecerse antes de mejorar seller mapping o CPU parsing, porque arreglar esos puntos sin filtrar componentes puede empujar falsos positivos hacia `watch` o incluso `strong`.

## 6. Gaps técnicos detectados

| ID | severidad | descripción | impacto | propuesta de solución | esfuerzo estimado | riesgo si no se corrige |
| --- | --- | --- | --- | --- | --- | --- |
| G01 | P0 | No hay filtro de categoría eBay ni exclusiones robustas para componentes/accesorios | Entran RAM, SSD sueltas, placas base y accesorios; algunas llegan a `watch` | añadir filtros Browse API si están disponibles y un prefilter textual duro para `motherboard`, `RAM`, `SODIMM`, `compatible for`, `for Lenovo`, `battery`, `charger`, `screen`, `keyboard`, `palmrest` | medio | digest/alertas con basura |
| G02 | P0 | `sellerAccountType=BUSINESS` no se mapea a `seller_type/is_business_seller` | `268` listings business reales quedan como no-business y distorsionan score | mapear `seller.sellerAccountType` y normalizar a enum interno | bajo | scores falsamente bajos y recalibración engañosa |
| G03 | P0 | `digest` usa threshold global (`>=60`) mientras la recomendación usa thresholds por search | hay `4` listings `ignore` con score `>=60`; digest puede incluirlos | hacer que `collect_digest_candidates` use recomendación final o threshold por search persistido | medio | digest incoherente y ruido operatorio |
| G04 | P1 | Parser CPU no reconoce `Core Ultra`, `Ultra 7/9`, `Ryzen AI 7/9`, `AI 360/370` | `98` títulos con `Ultra`, `8` con `Ryzen AI`, `0` CPUs parseadas | ampliar regex/normalización de CPU con fixtures reales | medio | infravaloración masiva de hardware moderno |
| G05 | P1 | Parser de familia es incompleto y case-sensitive | `29` títulos `T14s` no reconocidos; `P14S` uppercase falla en target; `P16v`/`P16s` ambiguos | normalizar casing y ampliar familias/variantes permitidas o excluidas explícitamente | medio | falsos negativos y target mismatch |
| G06 | P1 | Detector de teclado es casi inútil en datos reales | `348/348` con `keyboard_layout = null` | añadir detección de `UK English`, `US English`, `QWERTZ`, `DEU`, `ENGLISCH`, `SWISS`, etc. | medio | penalización constante y explicación pobre |
| G07 | P1 | Parser de RAM/SSD es frágil | `16GB` queda `null`; `4TB/8TB` queda `null`; componentes RAM heredan puntos de RAM | soportar más capacidades y añadir heurísticas “RAM-only / storage-only product” | medio | score incoherente y explicaciones erróneas |
| G08 | P1 | Falsos positivos de placa base alcanzan `watch` | IDs `3` y `53` en `watch` | añadir exclusión dura por keywords de componentes antes del score | bajo | digest no confiable |
| G09 | P1 | Anti-duplicado de alertas no está calibrado para casos multi-mercado / multi-query | DB mock histórica muestra `12` strong simulated sobre `listing_id=1` | revisar dedup/alert key y no re-alertar por cambios cosméticos o marketplace-locales | medio | spam de Telegram cuando aparezca un candidato fuerte real |
| G10 | P2 | `doctor` solo valida presencia de `.env` y YAML; no prueba eBay/Telegram/SMTP | falsa sensación de readiness | añadir `doctor --live` o checks opt-in por integración | medio | sorpresas en primer uso real |
| G11 | P2 | Solo se pide `limit=25` a eBay y no hay paginación | cobertura parcial del mercado | añadir paginación controlada y límite configurable | medio | oportunidades perdidas |
| G12 | P2 | No se deduplican variantes por `itemGroupHref` | hay `13` grupos con 2-3 variantes | persistir `item_group_id` y usarlo en reporting/dedup | medio | saturación de variantes similares |
| G13 | P2 | `list-recent` / `explain-score` muestran `score=0` como `n/a` | inspección manual confusa | formatear `0` como `0` | bajo | diagnóstico más lento |
| G14 | P2 | Política de backup/retention no definida | solo hay un backup ad hoc en `data/backups/` | definir backup de SQLite y retención mínima | bajo | operación frágil |

## 7. Decisiones pendientes

- ¿Priorizar solo `P14s/T14/T14s/T16` y dejar `P1/P16/P16v` fuera hasta que el ruido esté bajo control?
- ¿Excluir `UK` por defecto durante la fase de calibración o mantenerlo con penalización fuerte?
- ¿Aceptar teclados no ES si el precio compensa, o bajar mucho el score salvo `ES/UK`?
- ¿Cuál es el rango de precio objetivo real por familia? Ahora el sistema usa `1200` y `1300`, pero la base demuestra que gran parte del mercado real de P1 queda muy por encima.
- ¿El target mínimo sigue siendo solo `64GB`, o queremos alertar también `32GB/512GB` si el precio es excepcional?
- ¿Mantener email fuera del scope inmediato y centrar todo en Telegram + dry-run?
- ¿Meter `T14s` como familia objetivo explícita en la próxima iteración?
- ¿Meter `P16/P16v` como scope controlado o excluirlos duro para v1?
- ¿Activar systemd solo después del primer “real alert controlled”, o aceptar un periodo intermedio con timer en dry-run?

## 8. Propuesta de próximos milestones

### Ruta A — Conservadora / calidad primero

- objetivo: limpiar señal, endurecer filtros y llegar a una shortlist revisable manualmente;
- pasos:
  - excluir componentes/accesorios/categorías no laptop;
  - arreglar seller business mapping;
  - ampliar parsers CPU/RAM/SSD/familia/teclado;
  - recalibrar thresholds con la DB real;
  - repetir `real dry-run` hasta que top 20 sea creíble;
- duración estimada: `2-4` sesiones de trabajo;
- riesgo: bajo;
- cuándo elegirla: si la prioridad es no quemar confianza con alertas basura.

### Ruta B — Beta rápida con Telegram y thresholds duros

- objetivo: empezar a recibir muy pocas alertas reales cuanto antes;
- pasos:
  - subir thresholds;
  - desactivar digest;
  - excluir UK temporalmente;
  - dejar solo búsquedas/familias más seguras;
  - hacer un primer alert controlled;
- duración estimada: `1-2` sesiones;
- riesgo: medio-alto, porque el parser sigue débil y pueden escaparse falsos positivos raros;
- cuándo elegirla: si se prioriza feedback temprano sobre calidad del dataset.

### Ruta C — Expansión de scope / radar más ambicioso

- objetivo: cubrir más familias, variantes y mercados desde ya;
- pasos:
  - añadir `T14s`, `P16`, `P16v`, más categorías y mejor dedup por item group;
  - ampliar scoring con más señales;
  - introducir reporting más rico;
- duración estimada: `4-6` sesiones;
- riesgo: alto; amplía superficie antes de cerrar los bugs básicos;
- cuándo elegirla: solo si el objetivo cambia de “herramienta útil ya” a “motor de radar más general”.

### Recomendación

Recomiendo **Ruta A**.

El sistema ya tiene infraestructura suficiente; el cuello de botella es calidad de señal. Meter más scope o activar producción ahora empeora el problema en vez de resolverlo.

## 9. Plan recomendado

### M2.5 Data Quality & Scoring Calibration

Checklist:

- [ ] añadir exclusiones duras para RAM-only / memory / SODIMM / compatible for / for Lenovo / motherboard / battery / charger / screen / keyboard / palmrest / SSD-only
- [ ] añadir o endurecer filtros Browse API por categoría laptop/workstation si están disponibles
- [ ] mapear `sellerAccountType -> seller_type/is_business_seller`
- [ ] soportar CPUs `Core Ultra`, `Ultra 7/9`, `Ryzen AI`, `AI 350/360/370`, `8840U/8840HS`
- [ ] reconocer `T14s`, normalizar `P14S -> P14s`, decidir `P16/P16v`
- [ ] ampliar detector de teclado (`UK English`, `US English`, `QWERTZ`, `DEU`, `SWISS`, etc.)
- [ ] ampliar parser de RAM/SSD (`16/32/48/64/96/128`, `512GB/1TB/2TB/4TB/8TB`, `NVMe`, `M.2`)
- [ ] corregir selección de digest para no incluir `ignore`
- [ ] corregir visualización de score `0`
- [ ] añadir tests reales de regresión con títulos capturados de esta DB
- [ ] rerun `radar run-once --dry-run` y revisar top 20

### M3 First Real Alert Controlled

- [ ] elegir 1-2 searches de bajo ruido
- [ ] decidir si UK queda fuera temporalmente
- [ ] ejecutar un `radar test-alert` real controlado con DB limpia o label de prueba
- [ ] validar que solo una alerta fuerte realmente valiosa podría pasar
- [ ] revisar anti-duplicate logic antes de repetir

### M4 Scheduler/Systemd

- [ ] activar timer primero en `dry-run`
- [ ] revisar logs de varias ejecuciones
- [ ] confirmar que no crecen falsos positivos críticos
- [ ] solo entonces pasar a modo real controlado

### M5 Monitoring/Digest Polish

- [ ] decidir si SMTP entra o se difiere
- [ ] mejorar `doctor` con checks opt-in reales
- [ ] definir backup/retention SQLite
- [ ] mejorar reporting de runs y shortlist

## 10. DoD antes de activar producción

- [ ] eBay real dry-run `errors=0`
- [ ] false positives críticos filtrados
- [ ] no RAM/components
- [ ] parser seller business arreglado
- [ ] top 20 candidates revisables
- [ ] 0 alert spam
- [ ] Telegram live test OK
- [ ] DB backup/retention definido
- [ ] systemd timer en dry-run primero
- [ ] logs revisables

## 11. Anexo técnico

### Repo audit

- branch: `main`
- último commit: `497083e Implement hardware deal radar v1`
- `git status --short`: `?? data/backups/`
- artefacto no trackeado detectado: `data/backups/radar.mock-preflight.20260630-230157.sqlite`

Árbol relevante:

- `pyproject.toml`
- `README.md`
- `config/*.yaml`
- `src/hardware_deal_radar/`
- `tests/`
- `scripts/`
- `docs/`
- `04_outputs/`

Dependencias principales (`pyproject.toml`):

- runtime: `httpx`, `pydantic`, `pydantic-settings`, `pyyaml`, `rich`, `sqlmodel`, `typer`
- dev: `pytest`, `ruff`
- entrypoint: `radar = hardware_deal_radar.main:main`

Entrypoints CLI observados:

- `validate-config`
- `show-config`
- `run-once`
- `digest`
- `test-alert`
- `list-recent`
- `explain-score`
- `doctor`

Módulos principales del pipeline:

- `config.loader`, `config.schemas`
- `sources.ebay_client`, `sources.ebay_normalizer`, `sources.mock_source`
- `pipeline.normalize`, `pipeline.enrich`, `pipeline.cost`, `pipeline.score`, `pipeline.alert_decision`, `pipeline.run`
- `storage.db`, `storage.models`, `storage.listings_repo`, `storage.alerts_repo`, `storage.runs_repo`

### Cómo funciona realmente la arquitectura

- Config:
  - carga `config/searches.yaml`, `config/scoring.yaml`, `config/marketplaces.yaml`
  - valida thresholds y referencias cruzadas
- Marketplaces consultados:
  - `EBAY_ES`, `EBAY_DE`, `EBAY_IT`, `EBAY_GB`
- Searches configuradas:
  - `thinkpad_p14s_64gb`
  - `thinkpad_t14_64gb`
  - `thinkpad_t16_64gb`
  - `thinkpad_p1_64gb`
- eBay:
  - OAuth client credentials
  - `GET /buy/browse/v1/item_summary/search`
  - header `X-EBAY-C-MARKETPLACE-ID`
  - params actuales: solo `q` y `limit=25`
- Normalización:
  - Browse API -> `ListingCandidate`
  - luego enrich + cost estimate
- Deduplicación:
  - `source + marketplace + source_item_id`
  - fallback `canonical_url`
  - fallback `marketplace + seller + normalized_title + price`
- Persistencia:
  - SQLite con tablas `runs`, `listings`, `alerts`, `price_history`, `error_logs`
- Score:
  - thresholds globales: `strong=80`, `digest=60`, `ignore_below=50`
  - per-search:
    - P14s/T14/T16: `strong=80`, `digest=60`
    - P1: `strong=85`, `digest=65`
  - recomendación:
    - `reject`: score por debajo de ignore-below o reject keyword / hard fail
    - `ignore`: score >= 50 pero por debajo del digest threshold efectivo
    - `watch`: score >= digest threshold efectivo
    - `strong_candidate`: score >= strong threshold efectivo
- Alert:
  - Telegram fuerte si `strong_candidate` y no hay alerta previa o hay cambio significativo
  - digest candidate si `score >= digest threshold` en `run_once`
  - `digest` CLI: actualmente selecciona por threshold global `60`, no por threshold efectivo por search

### Qué hace exactamente `--dry-run`

- `run-once --dry-run`:
  - **sí** consulta eBay real si no se usa `--mock`
  - **sí** persiste `runs`, `listings` y `price_history`
  - **sí** puede persistir alert rows si el score cruza `strong` (estado `simulated`)
  - **no** envía Telegram real
  - **no** envía email real
  - usa `NoopAlerter`
- `digest --dry-run`:
  - **sí** lee la DB real
  - **sí** puede persistir alert rows de digest `simulated`
  - **no** envía email real
- `test-alert --dry-run`:
  - genera un payload estático
  - usa `NoopAlerter`
  - **no** persiste DB
  - **no** manda Telegram real

### Comandos ejecutados

Ejecutados en este checkpoint:

- `git branch --show-current`
- `git log -1 --stat --oneline`
- `git status --short`
- `~/.local/bin/uv run radar --help`
- `~/.local/bin/uv run radar doctor`
- `~/.local/bin/uv run radar validate-config`
- `~/.local/bin/uv run radar list-recent`
- `~/.local/bin/uv run radar explain-score 348`
- `~/.local/bin/uv run pytest -q`
- inspección read-only de SQLite con `python sqlite3` (el binario `sqlite3` no estaba disponible)

### Outputs resumidos

- `doctor`:
  - `.env` presente
  - permisos `0o600`
  - `EBAY_*` y `TELEGRAM_*` en `<set>`
  - `SMTP_*` en `<empty>`
  - `db_parent present`
  - `config valid`
- `validate-config`: `Config is valid.`
- `pytest -q`: `27 passed`
- `list-recent`: muestra IDs `329-348` recientes en `EBAY_GB`
- `explain-score 348`: `reject`, score `17`, con positivos espurios de RAM/familia/precio

### Tablas SQLite relevantes

Schema observado:

- `runs`
- `listings`
- `alerts`
- `price_history`
- `error_logs`

Métricas DB activa:

- total listings: `348`
- por marketplace:
  - `EBAY_DE: 99`
  - `EBAY_ES: 95`
  - `EBAY_GB: 82`
  - `EBAY_IT: 72`
- por recommendation:
  - `reject: 325`
  - `ignore: 15`
  - `watch: 8`
  - `strong_candidate: 0`
- `score_total is null`: `0`
- `score_total = 0`: `54`
- `price_history`: `348`
- `error_logs`: `0`

Distribuciones:

- `risk_flags`:
  - `keyboard_layout_risk: 348`
  - `import_risk: 82`
  - `seller_risk: 18`
- `unknown_fields`:
  - `keyboard_layout: 348`
  - `cpu_text: 252`
  - `ssd_gb: 123`
  - `ram_gb: 89`
  - `model_family: 55`

Detecciones cuantificadas:

- `raw sellerAccountType = BUSINESS`: `268`
- de esos, mapeados con `seller_type = null`: `268`
- de esos, mapeados con `is_business_seller = false`: `268`
- títulos con `Ultra`: `98`, CPUs parseadas: `0`
- títulos con `Ryzen AI`: `8`, CPUs parseadas: `0`
- títulos con `T14s`: `29`, reconocidos como familia: `0`
- `keyboard_layout is null`: `348`
- casos `score >= 60` pero `recommendation = ignore`: `4`

### Notas de tests

- la suite actual protege la base del proyecto y algunos flujos mock
- no cubre todavía:
  - `sellerAccountType`
  - `Core Ultra`
  - `Ryzen AI`
  - `T14s`
  - `motherboard`
  - `RAM-only`
  - inconsistencia digest threshold por search
  - score `0` visible como `n/a`


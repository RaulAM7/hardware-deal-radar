# 07 — Data Model

## Objetivo

Definir un modelo de datos mínimo, estable y suficiente para:

- guardar listings vistos;
- detectar duplicados;
- detectar cambios relevantes;
- registrar alertas enviadas;
- explicar scores;
- generar digest;
- consultar histórico por CLI.

## Entidades principales

### Listing

Representa un listing normalizado.

Campos sugeridos:

```txt
id
source
marketplace
source_item_id
canonical_url
title
seller_username
seller_type
seller_feedback_score
seller_feedback_percentage
seller_country
item_country
condition
buying_options
currency
price_amount
shipping_amount
estimated_total_eur
estimated_import_cost_eur
risk_adjustment_eur
model_family
model_generation
cpu_text
ram_gb
ssd_gb
keyboard_layout
is_thinkpad
is_target_family
is_business_seller
has_returns
has_warranty
listing_status
first_seen_at
last_seen_at
last_changed_at
raw_payload_json
```

### Score

Puede vivir como campos en Listing o como tabla separada.

Campos sugeridos:

```txt
listing_id
score_total
score_version
positive_reasons_json
negative_reasons_json
risk_flags_json
recommendation
created_at
```

Para v1 puede almacenarse en la propia tabla `listings` si simplifica.

### Alert

Representa una alerta enviada o intentada.

Campos sugeridos:

```txt
id
listing_id
alert_type
channel
threshold
score_at_send
price_at_send
status
sent_at
error_message
payload_preview
```

### Run

Representa una ejecución del radar.

Campos sugeridos:

```txt
id
started_at
finished_at
status
searches_count
marketplaces_count
raw_results_count
new_listings_count
updated_listings_count
strong_alerts_count
digest_candidates_count
errors_count
summary_json
```

## Deduplicado

Clave principal preferida:

```txt
source + marketplace + source_item_id
```

Fallbacks:

```txt
canonical_url
marketplace + seller_username + normalized_title + price_amount
```

## Cambios relevantes

Un listing ya visto debe considerarse actualizado si cambia:

- precio;
- envío;
- coste total estimado;
- score;
- condición;
- vendedor;
- disponibilidad;
- política de devolución;
- información de RAM/SSD/CPU extraída.

## Histórico de precios

V1 puede guardar precio actual en Listing y registrar cambios relevantes en `raw_payload_json` o tabla simple de eventos.

Si no complica la implementación, añadir tabla `price_history`:

```txt
id
listing_id
price_amount
shipping_amount
estimated_total_eur
observed_at
```

No es obligatorio si amenaza el B-shot.

## JSON fields

Para v1 es aceptable guardar campos JSON serializados en SQLite para:

- raw payload;
- score reasons;
- risk flags;
- run summary.

## Migraciones

V1 puede usar creación automática de tablas al arrancar.

No es obligatorio introducir Alembic salvo que el agente lo considere muy simple y no aumente fricción.

## Índices recomendados

- `source_item_id`
- `canonical_url`
- `marketplace`
- `score_total`
- `first_seen_at`
- `last_seen_at`
- `estimated_total_eur`
- `ram_gb`
- `model_family`
- `alert status/listing_id`

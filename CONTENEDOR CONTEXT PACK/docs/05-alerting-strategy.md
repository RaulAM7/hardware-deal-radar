# 05 — Alerting Strategy

## Principio

El sistema no debe generar ruido.

Una alerta debe ser accionable. Si el usuario recibe una alerta, debería poder decidir rápido si abre el listing, lo ignora o lo investiga.

## Canales v1

- Telegram para alertas fuertes.
- Email para digest de candidatos interesantes.

## Telegram

Telegram se usa para oportunidades de alta prioridad.

Debe ser breve, claro y accionable.

Contenido mínimo:

- título;
- modelo estimado;
- RAM;
- SSD;
- CPU si se detecta;
- país/marketplace;
- vendedor;
- precio;
- envío;
- coste total estimado;
- score;
- motivos positivos;
- riesgos;
- link.

Ejemplo conceptual:

```txt
🔥 Posible ganga ThinkPad

ThinkPad P14s Gen 4 AMD
RAM: 64 GB
SSD: 1 TB
CPU: Ryzen 7 PRO 7840U
Marketplace: eBay DE
Vendedor: business / 99,5%
Precio: 849 €
Envío: 29 €
Coste estimado: 878 €
Score: 88/100

Por qué interesa:
+ 64 GB RAM
+ CPU moderna
+ vendedor profesional
+ devolución disponible

Riesgos:
- teclado alemán
- batería no verificada

Link:
...
```

## Email digest

El digest debe agrupar candidatos medianos o interesantes, no necesariamente gangas fuertes.

Frecuencia inicial: diaria, si hay candidatos.

Contenido:

- resumen ejecutivo;
- top candidatos;
- tabla/lista con score;
- riesgos principales;
- links;
- notas de mercado.

## Umbrales iniciales

Estos valores son orientativos y deben fijarse en specs:

- `strong_alert_threshold`: 80/100
- `digest_threshold`: 60/100
- `ignore_below`: 50/100

## Antiduplicados

No debe alertar dos veces por el mismo listing salvo cambio relevante.

Cambios relevantes:

- bajada de precio significativa;
- mejora de score;
- cambio de envío/coste;
- cambio de condición;
- aparición de nueva información crítica.

## Tipos de evento

El sistema puede registrar internamente:

- listing_seen;
- listing_updated;
- strong_alert_sent;
- digest_candidate_added;
- listing_ignored;
- price_drop_detected;
- risk_changed.

## Modo test

Debe existir un comando para probar alertas sin consultar fuentes reales:

```bash
radar test-alert
```

Debe enviar una alerta falsa/controlada a Telegram y/o email para validar configuración.

## Fallos de alerta

Si Telegram falla, el sistema debe registrar error y continuar.

Si email falla, debe registrar error y continuar.

Un fallo de alerta no debe romper la persistencia de listings ya procesados.

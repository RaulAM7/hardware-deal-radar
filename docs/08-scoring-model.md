# 08 — Scoring Model

## Principio

El scoring v1 debe ser determinista, explicable y configurable.

No se usará IA generativa para decidir si algo es una ganga.

El sistema debe producir:

- score total 0-100;
- motivos positivos;
- motivos negativos;
- flags de riesgo;
- recomendación breve.

## Estructura conceptual

Puntuación base sugerida:

```txt
score = hardware_score
      + seller_score
      + price_score
      + marketplace_score
      + confidence_score
      - risk_penalties
```

El resultado debe limitarse a 0-100.

## Hardware score

Factores positivos:

- 64 GB RAM: fuerte positivo.
- 32 GB RAM: positivo moderado.
- SSD 1 TB: positivo.
- CPU moderna: positivo.
- Familia objetivo ThinkPad: positivo.
- Generación reciente: positivo.
- Buen equilibrio peso/potencia: positivo si se puede inferir.

Factores negativos:

- RAM < 32 GB: descarte o penalización extrema.
- CPU antigua: penalización.
- SSD pequeño: penalización.
- equipo no ThinkPad: en v1, penalización o exclusión según búsqueda.
- workstation demasiado pesada: penalización.

## Seller score

Factores positivos:

- vendedor business/profesional;
- feedback alto;
- feedback percentage alto;
- muchas ventas;
- devolución aceptada;
- garantía;
- descripción clara.

Factores negativos:

- feedback bajo;
- vendedor nuevo;
- sin devolución;
- información incompleta;
- señales de riesgo.

## Price score

El precio se evalúa sobre coste total estimado, no precio visible.

Factores positivos:

- coste total bajo para la configuración;
- descuento aparente fuerte;
- precio dentro de rango objetivo.

Factores negativos:

- coste total cercano a nuevo/reacondicionado oficial;
- envío alto;
- precio sospechosamente bajo si coincide con otras señales de riesgo;
- subasta sin precio final representativo.

## Marketplace score

España:

- baja fricción;
- baja penalización.

Alemania:

- mercado prioritario;
- penalización leve por teclado/logística.

Italia:

- penalización leve/media.

Reino Unido:

- penalización fuerte por importación, aduanas, devolución y coste incierto.

## Keyboard risk

No descartar por teclado extranjero. Penalizar.

Valores sugeridos:

- ES: 0
- UK: -2
- DE: -5
- IT: -4
- desconocido: -5
- raro/no estándar: -8

## Import risk

Valores sugeridos:

- UE: 0
- UK: -10
- desconocido: -6

Además, para UK debe añadirse advertencia textual.

## Umbrales

Valores iniciales:

```txt
strong_alert_threshold = 80
digest_threshold = 60
ignore_below = 50
```

## Recomendación textual

El sistema debe generar una recomendación simple:

- `strong_candidate`
- `watch`
- `ignore`
- `reject`

Ejemplos:

```txt
strong_candidate: "Merece revisión inmediata."
watch: "Interesante, pero no urgente."
ignore: "No compensa por precio/riesgo."
reject: "No cumple mínimos."
```

## Razones

Cada score debe explicar:

### Positive reasons

- `64GB RAM`
- `CPU moderna`
- `vendedor profesional`
- `precio competitivo`
- `devolución disponible`

### Negative reasons

- `teclado alemán`
- `UK/import risk`
- `batería no verificada`
- `descripción incompleta`
- `precio alto`

### Risk flags

- `keyboard_layout_risk`
- `import_risk`
- `seller_risk`
- `condition_risk`
- `battery_unknown`
- `low_information`
- `possible_parts_only`
- `price_too_good_to_be_true`

## Palabras de descarte

Si aparecen en título/descripción, penalizar o rechazar:

```txt
for parts
spares
defective
broken
no boot
BIOS locked
locked
icloud locked
password locked
water damage
cracked
faulty
not working
```

Debe considerarse traducción/idiomas si no complica v1.

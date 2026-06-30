# 04 — Marketplaces and Sources

## Fuente v1

La fuente oficial v1 es eBay Browse API.

No se implementará scraping HTML en v1.

La arquitectura debe permitir añadir fuentes futuras, pero la implementación inicial debe mantenerse enfocada.

## Marketplaces iniciales

- eBay España
- eBay Alemania
- eBay Italia
- eBay Reino Unido

## Razonamiento

### España

Menos fricción logística y fiscal. Probablemente menor volumen de oportunidades, pero mayor simplicidad de compra.

### Alemania

Mercado prioritario. Alto volumen de portátiles business y posible liquidación empresarial. Mayor probabilidad de oportunidades ThinkPad.

### Italia

Mercado complementario. Puede aportar oportunidades puntuales.

### Reino Unido

Mercado con volumen, pero penalizado por importación, aduanas, devoluciones y coste total incierto.

## API-first

El sistema debe usar la API oficial siempre que sea posible.

Ventajas:

- mayor estabilidad;
- menor riesgo de bloqueo;
- mejor mantenibilidad;
- estructura de datos más predecible;
- menor fragilidad frente a cambios de HTML;
- mejor encaje con un proyecto interno serio.

## Abstracción de fuente

Aunque v1 solo use eBay, el diseño debe crear una interfaz conceptual de fuente:

```txt
SourceClient.search(search_config, marketplace) -> list[RawListing]
```

Esto permitirá añadir futuras fuentes sin reescribir pipeline.

## Normalización

Cada fuente debe tener dos capas:

1. Cliente fuente: obtiene datos raw.
2. Normalizador fuente: convierte datos raw a modelo interno.

## Consideraciones por marketplace

Cada marketplace debe tener configuración:

- identificador interno;
- marketplace id/API id;
- país;
- moneda esperada;
- idioma principal;
- penalización base;
- penalización teclado;
- penalización fiscal;
- si pertenece o no a UE para el caso de compra desde España/Canarias;
- notas operativas.

## Configuración esperada

Ejemplo conceptual:

```yaml
marketplaces:
  EBAY_ES:
    country: ES
    currency: EUR
    base_risk_penalty: 0
    import_risk_penalty: 0
    keyboard_risk_penalty: 0

  EBAY_DE:
    country: DE
    currency: EUR
    base_risk_penalty: 2
    import_risk_penalty: 0
    keyboard_risk_penalty: 5

  EBAY_IT:
    country: IT
    currency: EUR
    base_risk_penalty: 2
    import_risk_penalty: 0
    keyboard_risk_penalty: 4

  EBAY_GB:
    country: GB
    currency: GBP
    base_risk_penalty: 8
    import_risk_penalty: 10
    keyboard_risk_penalty: 2
```

Los valores definitivos deben ser definidos en specs.

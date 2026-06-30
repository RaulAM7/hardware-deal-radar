# marketplaces.example.yaml

Ejemplo conceptual de configuración de marketplaces.

Cuando se implemente el sistema, este contenido debería convertirse en `config/marketplaces.yaml`.

```yaml
marketplaces:
  EBAY_ES:
    label: "eBay España"
    country: "ES"
    currency: "EUR"
    base_risk_penalty: 0
    import_risk_penalty: 0
    keyboard_risk_penalty: 0
    notes: "Mercado de menor fricción logística/fiscal."

  EBAY_DE:
    label: "eBay Alemania"
    country: "DE"
    currency: "EUR"
    base_risk_penalty: 2
    import_risk_penalty: 0
    keyboard_risk_penalty: 5
    notes: "Mercado prioritario por volumen business/ThinkPad. Penalizar teclado alemán."

  EBAY_IT:
    label: "eBay Italia"
    country: "IT"
    currency: "EUR"
    base_risk_penalty: 2
    import_risk_penalty: 0
    keyboard_risk_penalty: 4
    notes: "Mercado complementario. Penalizar teclado/logística levemente."

  EBAY_GB:
    label: "eBay Reino Unido"
    country: "GB"
    currency: "GBP"
    base_risk_penalty: 8
    import_risk_penalty: 10
    keyboard_risk_penalty: 2
    notes: "Penalizar por aduanas, devoluciones y coste total incierto."
```

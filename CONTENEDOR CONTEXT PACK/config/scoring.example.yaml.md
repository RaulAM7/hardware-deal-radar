# scoring.example.yaml

Ejemplo conceptual de configuración de scoring.

Cuando se implemente el sistema, este contenido debería convertirse en `config/scoring.yaml`.

```yaml
thresholds:
  strong_alert: 80
  digest: 60
  ignore_below: 50

ram:
  minimum_gb: 32
  preferred_gb: 64
  points:
    below_minimum: -100
    minimum: 10
    preferred: 25

storage:
  points:
    ssd_512gb: 4
    ssd_1tb: 8
    ssd_2tb: 10

seller:
  business_seller: 10
  feedback_percentage_99_plus: 8
  feedback_percentage_97_plus: 5
  feedback_low_penalty: -10
  returns_accepted: 7
  warranty_available: 5

marketplace:
  EBAY_ES: 0
  EBAY_DE: -3
  EBAY_IT: -3
  EBAY_GB: -15

keyboard:
  ES: 0
  UK: -2
  DE: -5
  IT: -4
  unknown: -5
  other: -8

negative_keywords:
  reject:
    - "for parts"
    - "spares"
    - "defective"
    - "broken"
    - "not working"
    - "no boot"
    - "BIOS locked"
    - "password locked"
  penalize:
    - "battery issue"
    - "scratches"
    - "cracked"
    - "no charger"
```

# 06 — CTO Architecture

## Arquitectura v1 aprobada

```txt
Python 3.12+
SQLite
YAML config
CLI
eBay Browse API
Telegram alerts
Email digest
systemd timer cada 6 horas
venv en VPS
Docker opcional/documentado
```

## Principios técnicos

1. Mantener el sistema simple.
2. Evitar frontend en v1.
3. Evitar scraping en v1.
4. Separar fuente, normalización, scoring, persistencia y alertas.
5. Priorizar operación real en VPS.
6. Hacer el sistema fácil de inspeccionar por CLI.
7. Hacer el sistema fácil de modificar por agentes.
8. Documentar supuestos.
9. Fallar de forma visible, no silenciosa.
10. No sobrediseñar.

## Stack recomendado

- Python 3.12+
- `uv` o `pip-tools` para dependencias
- `pydantic` para settings/modelos
- `httpx` para APIs
- `PyYAML` para configuración
- `SQLite`
- `SQLModel` o `SQLAlchemy` ligero para persistencia
- `Typer` para CLI
- `Rich` para output terminal
- `pytest` para tests/checks
- `ruff` para lint/format
- Telegram Bot API para alertas
- SMTP para email digest
- systemd timer para scheduling

## Estructura candidata

```txt
hardware-deal-radar/
  README.md
  pyproject.toml
  .env.example

  config/
    searches.yaml
    scoring.yaml
    marketplaces.yaml

  src/
    hardware_deal_radar/
      __init__.py
      main.py
      cli.py

      sources/
        __init__.py
        ebay_client.py
        base.py

      pipeline/
        __init__.py
        fetch.py
        normalize.py
        deduplicate.py
        enrich.py
        score.py

      storage/
        __init__.py
        db.py
        models.py
        listings_repo.py
        alerts_repo.py

      alerts/
        __init__.py
        telegram.py
        email.py
        formatter.py

      reports/
        __init__.py
        daily_digest.py

      config/
        __init__.py
        loader.py
        schemas.py

      utils/
        __init__.py
        money.py
        logging.py
        text.py

  tests/
  scripts/
    run-once.sh
    install-vps.sh
    setup-systemd.sh

  data/
    radar.sqlite

  docs/
  specs/
  codex/
```

## Flujo end-to-end

```txt
1. CLI inicia ejecución.
2. Settings cargan `.env`.
3. Config loader lee YAML.
4. Para cada búsqueda:
   4.1 Para cada marketplace:
       - consulta eBay API
       - recibe raw listings
       - normaliza
       - enriquece datos extraíbles desde título/descripción disponible
       - estima coste total
       - calcula score
       - guarda/actualiza SQLite
       - decide si alerta
5. Se envían alertas fuertes por Telegram.
6. Se acumulan candidatos para digest.
7. Se registra resumen de ejecución.
```

## CLI mínima

```bash
radar run-once
radar digest
radar test-alert
radar list-recent
radar explain-score <listing_id>
```

## Configuración por entorno

Variables esperadas:

```env
EBAY_CLIENT_ID=
EBAY_CLIENT_SECRET=
EBAY_MARKETPLACE_DEFAULT=EBAY_ES

TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=

SMTP_HOST=
SMTP_PORT=
SMTP_USER=
SMTP_PASSWORD=
EMAIL_FROM=
EMAIL_TO=

RADAR_DB_PATH=data/radar.sqlite
RADAR_LOG_LEVEL=INFO
```

## Scheduling

V1 usará systemd timer.

Frecuencia aprobada:

```txt
cada 6 horas
```

El repo debe incluir scripts o documentación para:

- instalar servicio;
- instalar timer;
- activar timer;
- ver logs;
- ejecutar manualmente.

## Docker

Docker no es obligatorio en v1.

Puede documentarse como opción futura o añadirse si no complica el objetivo. La prioridad es venv + systemd en VPS.

## Observabilidad mínima

Debe haber logs con:

- inicio de ejecución;
- búsquedas cargadas;
- marketplaces consultados;
- número de resultados;
- errores de API;
- resultados nuevos;
- alertas enviadas;
- digest enviado;
- duración de ejecución.

## Política de errores

- Error en un marketplace no detiene todo el run.
- Error en una búsqueda no detiene el resto.
- Error de Telegram se registra y no rompe el proceso.
- Error de email se registra y no rompe el proceso.
- Error de configuración crítica sí debe fallar claramente.

## Seguridad

- Nunca commitear `.env`.
- Incluir `.env.example`.
- No imprimir secrets en logs.
- Limitar datos sensibles.
- Guardar solo información necesaria para la operación.

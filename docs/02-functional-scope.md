# 02 — Functional Scope

## Alcance v1

Hardware Deal Radar v1 debe implementar un sistema interno que:

1. Lea búsquedas desde ficheros YAML.
2. Consulte eBay Browse API en mercados configurados.
3. Normalice los resultados a un modelo común.
4. Deduzca o extraiga características clave.
5. Deduplicate listings ya vistos.
6. Guarde resultados en SQLite.
7. Calcule coste total estimado.
8. Aplique scoring determinista.
9. Genere alertas Telegram para oportunidades fuertes.
10. Genere digest por email para candidatos interesantes.
11. Permita ejecución manual por CLI.
12. Permita ejecución programada cada 6 horas con systemd timer.
13. Evite alertas duplicadas salvo cambios relevantes.
14. Deje logs suficientes para operar en VPS.
15. Documente instalación, configuración, ejecución y despliegue.

## Funcionalidades obligatorias

### Configuración de búsquedas

El sistema debe permitir declarar búsquedas por YAML.

Cada búsqueda debe poder definir:

- nombre;
- query textual;
- marketplaces;
- RAM mínima;
- RAM preferida;
- precio máximo estimado;
- familias/modelos objetivo;
- umbral de alerta fuerte;
- umbral de digest;
- palabras positivas;
- palabras negativas;
- exclusiones.

### Consulta de fuente

La fuente v1 es eBay Browse API.

El sistema debe consultar, como mínimo:

- eBay España;
- eBay Alemania;
- eBay Italia;
- eBay Reino Unido.

El diseño debe estar preparado para añadir futuras fuentes, pero no debe implementarlas en v1.

### Normalización

Los resultados deben convertirse en un modelo interno estable con campos como:

- source;
- marketplace;
- item id;
- title;
- url;
- price;
- currency;
- shipping cost;
- estimated total cost EUR;
- seller username;
- seller feedback score;
- seller feedback percentage;
- seller type if available;
- country;
- condition;
- buying options;
- listing date if available;
- extracted RAM;
- extracted SSD;
- extracted CPU;
- extracted model family;
- keyboard risk;
- import risk;
- score;
- score explanation.

### Deduplicado

El sistema debe evitar tratar el mismo listing como nuevo en cada ejecución.

Debe deduplicar por:

- item id si existe;
- url canonicalizada;
- combinación marketplace + seller + title + price si fuera necesario.

### Scoring

El scoring debe ser determinista y explicable.

Cada resultado debe tener:

- score total;
- motivos positivos;
- motivos negativos;
- flags de riesgo;
- recomendación textual breve.

### Alertas

El sistema debe enviar alerta Telegram si un listing supera el umbral de oportunidad fuerte.

Debe enviar email digest con candidatos medianos/interesantes si existen.

No debe enviar alertas duplicadas salvo que:

- el precio baje de forma relevante;
- el score suba de forma relevante;
- el listing haya cambiado en una propiedad crítica.

### CLI

Debe existir una CLI con comandos mínimos:

```bash
radar run-once
radar digest
radar test-alert
radar list-recent
radar explain-score <listing_id>
```

La implementación puede ajustar nombres si documenta claramente el uso.

## Fuera de alcance v1

- Panel web.
- Login.
- Multiusuario.
- React/Next.js.
- Compra automática.
- Watchlist automática en eBay.
- Scraping HTML.
- IA generativa para decidir scoring.
- Integración con Google Sheets.
- Integración con n8n como núcleo del sistema.
- Postgres/Supabase.
- Comparador histórico avanzado de precios.
- Soporte completo para todas las marcas.
- Dell/HP en v1.
- Kubernetes.
- Arquitectura distribuida.

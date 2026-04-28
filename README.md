# Wiredup

Flask weather app demonstrating live MCP tool integrations.

## MCP Servers

| Server | Purpose |
|--------|---------|
| [Context7](https://github.com/upstash/context7) | Live library docs (Flask, requests, Open-Meteo) fetched at build time |
| [Puppeteer](https://github.com/modelcontextprotocol/servers/tree/main/src/puppeteer) | Chrome visual verification of rendered weather UI |

## App

Queries [Open-Meteo](https://open-meteo.com/) (no API key required) and renders current weather for any city.

## Setup

```bash
pip install -r requirements.txt
python src/app.py
```

## Tests

```bash
pytest tests/
```

## How Live Docs Changed the Workflow

Context7 was queried 3 times during development — for Flask's app factory pattern,
Open-Meteo's forecast endpoint parameters, and the geocoding API response shape.
Each query caught at least one assumption that would have shipped as a bug:
the `results` key is absent (not `[]`) on no match, and `is_day` is `0/1` not a bool.

Puppeteer verified the rendered UI at 3 states: blank load, valid city, unknown city.
Screenshots replaced manual browser checks and gave shareable visual proof.

See [`evidence/live-docs-usage.md`](evidence/live-docs-usage.md) for full transcripts.

## Hallucination Comparison

Two cases documented side-by-side — WMO weather codes and geocoding empty-result shape.
Without live docs, both hallucinations were confident and plausible. Both were wrong.

See [`evidence/hallucination-comparison.md`](evidence/hallucination-comparison.md).

## What's Next

- Add hourly forecast (temperature chart)
- Add a third MCP server (e.g. filesystem for caching responses)
- Expand Puppeteer tests to cover responsive layout

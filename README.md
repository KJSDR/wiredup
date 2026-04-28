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

See [`evidence/live-docs-usage.md`](evidence/live-docs-usage.md).

## Hallucination Comparison

See [`evidence/hallucination-comparison.md`](evidence/hallucination-comparison.md).

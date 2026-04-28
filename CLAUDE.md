# Wiredup — CLAUDE.md

## Project

Flask weather app using Open-Meteo API. Demonstrates MCP integrations (Context7 + Puppeteer).

## Stack

- Python 3.9, Flask, requests
- pytest for tests
- Open-Meteo API (free, no key)

## MCP Servers

- **context7**: Use for live docs on any third-party library before writing code against it.
- **puppeteer**: Use to take screenshots of the running Flask app for visual verification.

## Conventions

- Test-first: write pytest tests before implementing features.
- Source lives in `src/`, tests in `tests/`.
- Evidence of MCP usage goes in `evidence/`.

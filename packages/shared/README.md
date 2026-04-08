# packages/shared

Small cross-cutting helpers only.

- `config.py` — Pydantic BaseSettings config loader from `.env`

Business logic must not collapse into this package.
If a helper grows complex, it belongs in its own package.

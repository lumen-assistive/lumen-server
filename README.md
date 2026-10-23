# lumen-server

[Italiano](README.it.md) | English

The optional backend for [Lumen](https://github.com/lumen-assistive):
caregiver device pairing, end-to-end encrypted sync, and model pack
metadata. FastAPI + PostgreSQL + Docker Compose.

Lumen's essential features work entirely offline; this server exists
only for features that require coordination between devices (a
caregiver's phone and the person they support) or between a device and
a future model distribution point. It never sees plaintext personal
data: calendar entries, daily status, and similar records are encrypted
on-device before upload and stored here as opaque blobs.

## Current scope

- Device pairing: `POST /api/v1/pairing` creates a caregiver account
  and a paired device, returning a bearer token.
- Encrypted sync: `POST /api/v1/blobs` and `GET /api/v1/blobs` store
  and retrieve opaque, client-encrypted payloads keyed by category
  (for example `daily-status`, `calendar`). The server cannot decrypt
  them.
- Model metadata: `GET /api/v1/models` returns the model pack catalog.
  It starts empty; no models have been converted, benchmarked, or
  license-cleared yet. This endpoint never serves model binaries.

Not in scope yet: push notifications to caregiver devices, multi-device
accounts beyond the pairing flow above, and the real model catalog
(populated once `lumen-models` exists).

## Running locally

```
docker compose up --build
```

This starts the API on `http://localhost:8000` and a PostgreSQL
database. Apply migrations once the containers are up:

```
docker compose exec app alembic upgrade head
```

`GET /health` is the liveness check.

## Development

Requires Python 3.12+.

```
python -m venv .venv
.venv/bin/pip install -e .[dev]   # .venv\Scripts\pip on Windows
ruff check .
ruff format --check .
mypy .
pytest --cov
```

All four pass as of this release (9 tests, 97% coverage), verified
locally, including an end-to-end `alembic upgrade head` /
`alembic downgrade base` round trip against a throwaway SQLite
database.

Install the shared commit message hook before committing:

```
git config core.hooksPath .githooks
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full workflow.

## License

Apache License 2.0, see [LICENSE](LICENSE).

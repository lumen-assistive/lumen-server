# Contributing to lumen-server

See the organization-wide
[CONTRIBUTING.md](https://github.com/lumen-assistive/.github/blob/main/CONTRIBUTING.md)
for the general workflow. This file only covers what is specific to
this repository.

## Setup

Requires Python 3.12+.

```
pip install -e .[dev]
git config core.hooksPath .githooks
```

Running against PostgreSQL locally:

```
docker compose up -d db
export LUMEN_SERVER_DATABASE_URL=postgresql+psycopg://lumen:lumen@localhost:5432/lumen
alembic upgrade head
uvicorn app.main:app --reload
```

Tests run against an isolated in-memory SQLite database and do not
require PostgreSQL.

## Before sending a pull request

```
ruff check .
ruff format --check .
mypy .
pytest --cov
```

All four must pass; CI runs the same commands on every push and pull
request.

## Adding a migration

After changing `app/models.py`, add a new revision under
`alembic/versions/`. Autogeneration (`alembic revision --autogenerate`)
requires a reachable database; without one, write the migration by
hand following the style of `0001_initial_schema.py`.

## Privacy constraint

Nothing added to this repository may let the server decrypt or infer
the plaintext content of a caregiver's calendar, daily status, or any
other personal record. If a feature seems to require that, it belongs
on the device, not here.

# Changelog

All notable changes to this project are documented in this file. The
format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org).

## [Unreleased]

### Added

- Device pairing endpoint issuing a bearer token per device.
- Encrypted blob upload and retrieval, scoped per device, storing
  opaque ciphertext the server cannot decrypt.
- Model pack metadata endpoint, starting with an empty catalog.
- PostgreSQL schema and initial Alembic migration.
- Docker Compose setup for local development.

### Known limitations

- No push notifications to caregiver devices yet.
- The model catalog is empty until `lumen-models` exists.
- `starlette.testclient` emits a deprecation warning about `httpx` in
  favor of an `httpx2` package; left as-is pending that ecosystem
  change stabilizing, since it is a warning, not a failure.

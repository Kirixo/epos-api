# Epos API
Self-hosted backend API for Epos PKM.

[![Tests](https://github.com/kirixo/epos-api/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/kirixo/epos-api/actions/workflows/ci-cd.yml)

## Running the Project

Build and start the application:
```bash
docker compose down
docker compose up -d --build
```
The API will be available at `http://localhost:8000`.
MongoDB is used for opaque encrypted sync envelopes, while PostgreSQL keeps auth and profile data.

## Applying Database Migrations

Apply migrations to the running database:
```bash
docker compose exec api alembic upgrade head
```

## Running Tests

Run the full pytest suite:
```bash
docker compose exec api alembic upgrade head
docker compose exec api pytest tests/
```

## Sync API

The sync layer is auth-scoped and stores only encrypted payloads. The client pushes opaque updates to:

- `POST /v1/sync/push`
- `GET /v1/sync/pull?workspace_id=...&after_cursor=...`

The server never decrypts workspace data.

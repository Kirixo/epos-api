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
The backend also enables CORS for the desktop and local browser origins the renderer uses by
default:

- `http://localhost:3000`
- `http://127.0.0.1:3000`
- `null`

Override this with `CORS_ALLOWED_ORIGINS` when you need a different renderer origin. The value
can be a comma-separated list or a JSON array.

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

The sync layer is auth-scoped and stores only opaque payloads. Workspace content uses encrypted,
bounded file-op batches, while workspace discovery uses a separate encrypted catalog stream so
devices can learn about workspaces created elsewhere without exposing titles to the server.

Workspace content sync:

- `POST /v1/sync/push`
- `GET /v1/sync/pull?workspace_id=...&after_cursor=...`

Workspace catalog sync:

- `POST /v1/sync/catalog/push`
- `GET /v1/sync/catalog/pull?after_cursor=...`

`after_cursor` is the last update id the client has already applied from that stream. The server
returns only newer updates after that point. For catalog sync, the request body is an opaque
encrypted `payload`; the server stores and replays it without interpreting workspace ids or
titles.

The server never decrypts workspace content or catalog data.
Browser and Electron clients can call these endpoints directly from the renderer because the API
sets explicit CORS headers for the configured allowed origins.

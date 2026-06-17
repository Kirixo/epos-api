# Epos API
## Running the Project

Build and start the application:
```bash
docker compose down
docker compose up -d --build
```
The API will be available at `http://localhost:8000`.

## Applying Database Migrations

Apply migrations to the running database:
```bash
docker compose exec api alembic upgrade head
```

## Running Tests

Run the full pytest suite:
```bash
docker compose exec api pytest tests/
```

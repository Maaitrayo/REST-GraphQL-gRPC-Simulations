# REST API Simulation

This folder contains the REST-based implementation of the project. The current setup demonstrates a simple layered FastAPI application with:

- user CRUD endpoints
- order CRUD endpoints
- separate SQLite databases for users and orders
- service and repository separation

## Run The Server

From the repository root, start the API with:

```powershell
uvicorn rest.app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## Project Docs

The main REST docs are in [`rest/docs/`](rest\docs):

- [`implementation.md`](docs\implementation.md): implementation order and execution flow
- [`objective.md`](docs\objective.md): project direction and design notes
- [`db-users-check.md`](docs\db-users-check.md): SQL commands for inspecting users and orders
- [`rest-pain-points.md`](docs\rest-pain-points.md): REST-specific pain points seen in this project

### Phase Plans

- [`phase-1-plan.md`](docs\phase\phase-1-plan.md): foundation and application bootstrap
- [`phase-2-plan.md`](docs\phase\phase-2-plan.md): user resource implementation
- [`phase-3-plan.md`](docs\phase\phase-3-plan.md): order resource implementation
- [`phase-4-plan.md`](docs\phase\phase-4-plan.md): cross-resource workflows
- [`phase-5-plan.md`](docs\phase\phase-5-plan.md): API quality improvements

## Sample Client Commands

Use the user client:

```powershell
uv run rest/user_client.py health
uv run rest/user_client.py create-user --name Alice --email alice@example.com
uv run rest/user_client.py list-users
uv run rest/user_client.py get-user 1
uv run rest/user_client.py update-user 1 --name "Alice Updated"
uv run rest/user_client.py delete-user 1
```

Use the order client:

```powershell
uv run rest/order_client.py create-order --user-id 1 --product-name Laptop --quantity 1
uv run rest/order_client.py list-orders
uv run rest/order_client.py get-order 1
uv run rest/order_client.py update-order 1 --status shipped
uv run rest/order_client.py delete-order 1
```

## Sample Database Commands

Open the databases:

```powershell
sqlite3 rest\db\users.db
sqlite3 rest\db\orders.db
```

Inside SQLite:

```sql
.tables
.schema users
.schema orders
SELECT id, name, email, is_active, created_at FROM users ORDER BY id;
SELECT id, user_id, product_name, quantity, status, created_at FROM orders ORDER BY id;
```

## Current Scope

Completed so far:

- Phase 1 foundation
- Phase 2 user resource
- Phase 3 order resource
- Phase 4 cross-resource workflows
- Phase 5 API quality improvements in progress

Next work should continue incrementally with remaining Phase 5 refinement and documentation updates.

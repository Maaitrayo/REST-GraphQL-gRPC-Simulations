# REST-GraphQL-gRPC-Simulations
simulations for 3 different API architectures

## REST API Simulation

The REST implementation lives in [`rest/`](C:\Users\USER\work\PERSONAL%20PROJECTS\REST-GraphQL-gRPC-Simulations\rest). It currently includes:

- user CRUD APIs
- order CRUD APIs
- separate SQLite databases for users and orders
- cross-resource flow for `GET /users/{user_id}/orders`
- API quality improvements such as standardized error responses, middleware timing, pagination, and order filtering

### Run The REST Server

From the repository root:

```powershell
uvicorn rest.app.main:app --reload
```

### REST Docs

See:

- [`rest/README.md`](rest\README.md)
- [`rest/docs/implementation.md`](rest\docs\implementation.md)
- [`rest/docs/phase/phase-5-plan.md`](rest\docs\phase\phase-5-plan.md)
- [`rest/docs/rest-pain-points.md`](rest\docs\rest-pain-points.md)

### Sample Commands

```powershell
python rest/user_client.py list-users
python rest/order_client.py list-orders
sqlite3 rest\db\users.db
sqlite3 rest\db\orders.db
```

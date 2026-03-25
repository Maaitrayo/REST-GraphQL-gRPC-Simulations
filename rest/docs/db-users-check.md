# User And Order DB SQL Commands

Use these commands to inspect the active SQLite databases used by the current app.

```powershell
sqlite3 rest\db\users.db
```

## Open Order Database

```powershell
sqlite3 rest\db\orders.db
```

## List Tables

```sql
.tables
```

## Show User Table Schema

```sql
.schema users
```

## View All Users

```sql
SELECT id, name, email, is_active, created_at
FROM users
ORDER BY id;
```

## Find One User By ID

```sql
SELECT id, name, email, is_active, created_at
FROM users
WHERE id = 1;
```

## Find One User By Email

```sql
SELECT id, name, email, is_active, created_at
FROM users
WHERE email = 'alice@example.com';
```

## Count Users

```sql
SELECT COUNT(*) AS total_users
FROM users;
```

## Show Order Table Schema

```sql
.schema orders
```

## View All Orders

```sql
SELECT id, user_id, product_name, quantity, status, created_at
FROM orders
ORDER BY id;
```

## Find Orders For One User

```sql
SELECT id, user_id, product_name, quantity, status, created_at
FROM orders
WHERE user_id = 1
ORDER BY id;
```

## Find One Order By ID

```sql
SELECT id, user_id, product_name, quantity, status, created_at
FROM orders
WHERE id = 1;
```

## Count Orders

```sql
SELECT COUNT(*) AS total_orders
FROM orders;
```

## Exit SQLite

```sql
.quit
```

## Quick Usage Examples

Start the API:

```powershell
uv run uvicorn rest.app.main:app --reload
```

Create a user with the client:

```powershell
uv run rest/user_client.py create-user --name Alice --email alice@example.com
```

Create an order:

```powershell
uv run rest/order_client.py create-order --user-id 1 --product-name Laptop --quantity 1
```

Then inspect the databases:

```powershell
sqlite3 rest\db\users.db
sqlite3 rest\db\orders.db
```

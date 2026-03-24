# User DB SQL Commands

Use these commands to inspect the active SQLite database used by the current app:

```powershell
sqlite3 rest\db\users.db
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
python rest/client.py create-user --name Alice --email alice@example.com
```

Then inspect the database:

```powershell
sqlite3 rest/users.db
```

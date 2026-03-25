# Phase 2 Plan

## Objective

Phase 2 is about implementing the `User` resource end to end.

The goal is to establish one complete CRUD pattern that later phases can copy for other resources.

This phase should prove the layered architecture works for a real entity.

---

## Features To Implement

### 1. User Model

Create the SQLAlchemy `User` model with fields such as:

- `id`
- `name`
- `email`
- `is_active`
- `created_at`

### 2. User Schemas

Add request and response schemas for:

- create
- update
- read

### 3. User Repository

Add user persistence methods for:

- list
- get by id
- get by email
- create
- update
- delete

### 4. User Service

Add business logic for:

- fetching a user
- preventing duplicate emails
- updating a user
- deleting a user

### 5. User Routes

Expose:

- `GET /api/v1/users`
- `GET /api/v1/users/{user_id}`
- `POST /api/v1/users`
- `PATCH /api/v1/users/{user_id}`
- `DELETE /api/v1/users/{user_id}`

### 6. User Tests

Add tests for:

- create and fetch flow
- duplicate email rejection
- not-found behavior

---

## Recommended Implementation Order

Implement Phase 2 in this order:

1. `rest/app/models/user.py`
2. `rest/app/schemas/user.py`
3. `rest/app/repositories/user_repository.py`
4. `rest/app/services/user_service.py`
5. `rest/app/api/v1/users.py`
6. route registration in `rest/app/main.py`
7. tests for user behavior

This keeps one resource self-contained from storage to API surface.

---

## Do We Need A Lot Of Data?

No.

Phase 2 only needs a few user records to verify CRUD behavior.

---

## Recommended Test Dataset

A very small dataset is enough:

- `1-5` users

That is sufficient to verify:

- create
- fetch
- update
- delete
- duplicate email handling

---

## Boundaries For This Phase

Do not add these in Phase 2:

- order logic
- cross-resource workflows
- middleware
- pagination or filtering

Phase 2 should focus only on one clean user resource implementation.

---

## Domain Knowledge Sources

Use these sources to understand the concepts behind this phase:

- FastAPI request body and response model docs: https://fastapi.tiangolo.com/tutorial/body/
- Pydantic docs: https://docs.pydantic.dev/
- SQLAlchemy ORM quickstart: https://docs.sqlalchemy.org/en/20/orm/quickstart.html
- HTTP semantics and status codes: https://httpwg.org/specs/rfc9110.html

---

## Expected Outcome

At the end of Phase 2, the project should have:

- a complete user CRUD flow
- a reusable route/service/repository pattern
- basic automated tests for user behavior

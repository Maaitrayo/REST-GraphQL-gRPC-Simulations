# Phase 1 Plan

## Objective

Phase 1 is about establishing the project foundation.

The goal is to create a minimal but reliable FastAPI application structure that:

- starts cleanly
- exposes a health endpoint
- initializes both SQLite databases
- provides the base package layout for later phases

This phase should stay small and focus only on bootstrapping.

---

## Features To Implement

### 1. FastAPI App Bootstrap

Create the application entrypoint in `rest/app/main.py`.

It should:

- create the FastAPI app
- register startup behavior
- expose a health endpoint

### 2. Basic App Configuration

Add a small configuration module to store:

- app name
- app version
- API prefix such as `/api/v1`

### 3. Shared SQLAlchemy Base

Create the shared declarative base that later models will inherit from.

### 4. Two Database Setup Files

Add separate database setup for:

- `users.db`
- `orders.db`

Each should provide:

- engine
- session factory
- init function

### 5. Base Package Structure

Create the initial package structure for:

- `api`
- `core`
- `db`
- `models`
- `repositories`
- `schemas`
- `services`

---

## Recommended Implementation Order

Implement Phase 1 in this order:

1. `rest/app/main.py`
2. `rest/app/core/config.py`
3. `rest/app/db/base.py`
4. `rest/app/db/user_database.py`
5. `rest/app/db/order_database.py`
6. package `__init__.py` files

This keeps dependencies simple and avoids unnecessary scaffolding too early.

---

## Do We Need A Lot Of Data?

No.

Phase 1 does not require domain data. It only needs the application to start and the database files to be initialized.

---

## Recommended Verification

For Phase 1, verification should be minimal:

- app imports successfully
- `/api/v1/health` returns `200`
- `users.db` and `orders.db` are created

No seed data is required.

---

## Boundaries For This Phase

Do not add these in Phase 1:

- CRUD endpoints
- business logic
- middleware
- tests for domain workflows
- pagination or filtering

Phase 1 should only establish the platform for later phases.

---

## Domain Knowledge Sources

Use these sources to understand the concepts behind this phase:

- FastAPI User Guide: https://fastapi.tiangolo.com/
- FastAPI application structure: https://fastapi.tiangolo.com/tutorial/bigger-applications/
- SQLAlchemy 2.0 docs: https://docs.sqlalchemy.org/en/20/
- SQLite docs: https://www.sqlite.org/docs.html

---

## Expected Outcome

At the end of Phase 1, the project should have:

- a working FastAPI app
- a versioned health route
- initialized SQLite database setup for users and orders
- a clean package structure ready for resource implementation

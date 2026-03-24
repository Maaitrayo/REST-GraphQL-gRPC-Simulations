# REST Implementation Guide

## 1. Purpose

This document explains how to approach the implementation of the REST simulation defined in `plan.md`.

It is an execution guide, not a design document. The goal is to reduce confusion while building by defining:

- the order of implementation
- the first milestone to target
- the coding pattern to follow for each feature
- what to avoid during the build

---

## 2. Implementation Strategy

The project should be built from the bottom up in stable layers.

Do not start by creating every endpoint quickly. Start by making the application structure reliable, then complete one resource end to end, then move to the next, and only then implement cross-resource workflows.

The recommended strategy is:

1. build the application skeleton
2. complete the `User` resource fully
3. complete the `Order` resource fully
4. add cross-database workflows
5. add API quality improvements
6. add tests and documentation

This reduces rework and keeps business logic from spreading into route handlers.

---

## 3. Phase-by-Phase Execution

### Phase 1: Foundation

Build the minimum structure required to run the project cleanly.

Implement:

- FastAPI application bootstrap
- `/api/v1/health` route
- app configuration module
- SQLAlchemy base setup
- database initialization for:
  - `users.db`
  - `orders.db`
- versioned router structure
- base package structure for:
  - `api`
  - `services`
  - `repositories`
  - `schemas`
  - `models`
  - `db`

Goal:

- the app starts without errors
- both database files can be initialized
- the health endpoint works

Do not move to resource implementation until this is stable.

### Phase 2: User Resource

Implement the `User` resource end to end before touching orders.

Implement:

- `User` SQLAlchemy model
- `User` Pydantic schemas
- user repository methods
- user service methods
- user routes
- tests for create and fetch flows

Required user flows:

- create user
- list users
- get user by id
- update user
- delete user

Goal:

- a complete CRUD pattern exists for one resource
- route handlers remain thin
- business logic stays in the service layer

This phase establishes the pattern for the rest of the codebase.

### Phase 3: Order Resource

After users are stable, implement orders with the same structure.

Implement:

- `Order` SQLAlchemy model
- `Order` Pydantic schemas
- order repository methods
- order service methods
- order routes
- tests for create and fetch flows

Required order flows:

- create order
- list orders
- get order by id
- update order
- delete order

Important rule:

- do not create an order unless the referenced user exists

This validation belongs in the service layer because the user and order data live in different databases.

### Phase 4: Cross-Database Workflows

Once both resources work independently, add workflows that require coordination.

Implement:

- `GET /api/v1/users/{user_id}/orders`
- business rule blocking user deletion when orders exist

Goal:

- show how REST handles aggregation
- make multi-database coordination explicit in service logic

This phase is where the simulation starts demonstrating realistic REST friction.

### Phase 5: API Quality Improvements

Only after the main flows are correct, improve the API surface.

Implement:

- pagination on list routes
- order filtering
- consistent error response format
- global exception handling
- request logging middleware
- request timing middleware

Goal:

- stable, predictable API behavior
- improved observability
- cleaner failure handling

### Phase 6: Testing and Documentation

Add tests after the main workflows exist so the test suite validates actual behavior rather than incomplete placeholders.

Implement tests for:

- user CRUD
- order creation with valid and invalid user ids
- user-orders aggregation endpoint
- user deletion rule when orders exist

Document:

- how to run the app
- how to run tests
- example requests for key endpoints

---

## 4. Recommended File Creation Order

Use this order to avoid jumping around the codebase too early:

1. `rest/app/main.py`
2. `rest/app/core/config.py`
3. `rest/app/db/base.py`
4. `rest/app/db/user_database.py`
5. `rest/app/db/order_database.py`
6. `rest/app/models/user.py`
7. `rest/app/schemas/user.py`
8. `rest/app/repositories/user_repository.py`
9. `rest/app/services/user_service.py`
10. `rest/app/api/v1/users.py`
11. `rest/app/models/order.py`
12. `rest/app/schemas/order.py`
13. `rest/app/repositories/order_repository.py`
14. `rest/app/services/order_service.py`
15. `rest/app/api/v1/orders.py`
16. cross-resource service and route logic
17. middleware and exception handling
18. tests

This order keeps dependencies straightforward and helps each layer build on top of a working lower layer.

---

## 5. First Milestone

The first milestone should be small and testable.

Target:

- app starts successfully
- `/api/v1/health` works
- database initialization works
- `POST /api/v1/users` works
- `GET /api/v1/users/{id}` works

If this milestone is not complete, do not move to orders yet.

---

## 6. Coding Pattern for Each Feature

For every new resource or workflow, implement in this order:

1. model
2. schema
3. repository
4. service
5. route
6. test

Why this order works:

- the data shape is defined first
- persistence is isolated before business logic depends on it
- services own rules and coordination
- routes stay minimal
- tests validate complete behavior instead of partial layers

---

## 7. Layer Responsibilities

### Routes

Routes should only:

- accept requests
- validate inputs
- call services
- return HTTP responses

Routes should not contain direct database queries or cross-resource business rules.

### Services

Services should:

- implement business logic
- coordinate repositories
- enforce workflow rules
- handle cross-database checks

### Repositories

Repositories should:

- contain query and persistence logic
- stay focused on one model or database concern
- avoid owning business decisions

---

## 8. Key Rules During Implementation

- do not put SQLAlchemy queries directly in route files
- do not mix user and order logic in one module
- do not implement advanced features before CRUD works
- do not rely on cross-database foreign keys
- do not skip tests for cross-resource rules

These rules protect the learning value of the project and keep the structure clean.

---

## 9. What to Implement Last

The following should come after the main CRUD and aggregation flows are stable:

- pagination
- filtering
- middleware
- global exception handling
- caching experiments
- stretch goals

These are important, but they are not foundational.

---

## 10. Suggested Daily Execution Flow

If you want to work iteratively, use this sequence:

### Day 1

- bootstrap FastAPI app
- configure routers
- initialize both databases
- add health route

### Day 2

- complete user model, schemas, repository, service, and routes
- test user CRUD

### Day 3

- complete order model, schemas, repository, service, and routes
- validate order creation against existing users

### Day 4

- implement `GET /api/v1/users/{user_id}/orders`
- implement user deletion rule when orders exist

### Day 5

- add pagination, filtering, middleware, exception handling
- add tests and example API documentation

This is only a pacing suggestion. The actual rule is to finish one stable milestone before starting the next.

---

## 11. End State

When implementation is complete, the project should have:

- a clear layered FastAPI structure
- two separate SQLite databases
- complete CRUD for users and orders
- cross-database validation and aggregation
- a clean baseline for comparing REST with GraphQL and gRPC

That should be the definition of done for the first version.

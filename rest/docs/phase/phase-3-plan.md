# Phase 3 Plan

## Objective

Phase 3 is about implementing the `Order` resource end to end.

The goal is to repeat the Phase 2 resource pattern while introducing the first multi-database validation rule: an order can only be created for an existing user.

This phase should make the project feel like a real multi-resource system.

---

## Features To Implement

### 1. Order Model

Create the SQLAlchemy `Order` model with fields such as:

- `id`
- `user_id`
- `product_name`
- `quantity`
- `status`
- `created_at`

### 2. Order Schemas

Add request and response schemas for:

- create
- update
- read

### 3. Order Repository

Add order persistence methods for:

- list
- get by id
- list by user id
- create
- update
- delete

### 4. Order Service

Add business logic for:

- fetching an order
- validating that `user_id` exists before creating an order
- updating an order
- deleting an order

### 5. Order Routes

Expose:

- `GET /api/v1/orders`
- `GET /api/v1/orders/{order_id}`
- `POST /api/v1/orders`
- `PATCH /api/v1/orders/{order_id}`
- `DELETE /api/v1/orders/{order_id}`

### 6. Order Client Support

Add a simple order-focused client to test the order endpoints manually.

---

## Recommended Implementation Order

Implement Phase 3 in this order:

1. `rest/app/models/order.py`
2. `rest/app/schemas/order.py`
3. `rest/app/repositories/order_repository.py`
4. `rest/app/services/order_service.py`
5. `rest/app/api/v1/orders.py`
6. route registration in `rest/app/main.py`
7. metadata registration in `rest/app/db/base.py`
8. order client and docs

This keeps the second resource aligned with the pattern already established by users.

---

## Do We Need A Lot Of Data?

No.

Phase 3 only needs a small number of users and orders to validate the resource flow.

---

## Recommended Test Dataset

A small dataset is enough:

- `2-3` users
- `3-10` orders

That is sufficient to verify:

- valid order creation
- invalid user rejection
- order retrieval
- order updates

---

## Boundaries For This Phase

Do not add these in Phase 3:

- aggregated user-order endpoints
- user delete protection based on orders
- middleware
- pagination or filtering

Phase 3 should focus on standalone order resource behavior plus user existence validation.

---

## Domain Knowledge Sources

Use these sources to understand the concepts behind this phase:

- FastAPI path/query/body docs: https://fastapi.tiangolo.com/tutorial/
- SQLAlchemy ORM querying guide: https://docs.sqlalchemy.org/en/20/orm/queryguide/
- SQLite docs: https://www.sqlite.org/docs.html
- HTTP semantics and status codes: https://httpwg.org/specs/rfc9110.html

---

## Expected Outcome

At the end of Phase 3, the project should have:

- a complete order CRUD flow
- user validation before order creation
- two working resources following the same layered architecture

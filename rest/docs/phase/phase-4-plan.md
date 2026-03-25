# Phase 4 Plan

## Objective

Phase 4 is about cross-resource workflows.

The goal is to demonstrate where REST starts becoming more involved by adding interactions that depend on both users and orders.

This phase should highlight the first real REST pain points in the project.

---

## Features To Implement

### 1. User Orders Endpoint

Add:

```text
GET /api/v1/users/{user_id}/orders
```

This endpoint should:

- validate that the user exists
- fetch the user’s orders
- return the combined result as an order list for that user

### 2. User Deletion Protection

Prevent deletion of a user if related orders exist.

This rule should:

- check for orders before deletion
- return a business error if orders are present

### 3. Service-Layer Coordination

Extend the user service so it can:

- load user orders from the order repository
- enforce delete protection

### 4. Cross-Resource Tests

Add tests for:

- retrieving orders for a user
- rejecting user deletion when orders exist

---

## Recommended Implementation Order

Implement Phase 4 in this order:

1. update `rest/app/services/user_service.py`
2. update `rest/app/api/v1/users.py`
3. add cross-resource tests
4. document REST pain points observed from this phase

This keeps the workflow logic in the service layer first and exposes it through the API only after it exists.

---

## Do We Need A Lot Of Data?

No.

Phase 4 only needs a few users and a few linked orders to prove the workflow behavior.

---

## Recommended Test Dataset

A very small dataset is enough:

- `2-3` users
- `1-5` orders linked to those users

That is sufficient to verify:

- `GET /users/{id}/orders`
- delete-blocking when orders exist

---

## Boundaries For This Phase

Do not add these in Phase 4:

- pagination
- filtering
- middleware
- standardized error response refactors
- caching

Phase 4 should stay focused on cross-resource orchestration only.

---

## Domain Knowledge Sources

Use these sources to understand the concepts behind this phase:

- FastAPI dependency injection docs: https://fastapi.tiangolo.com/tutorial/dependencies/
- SQLAlchemy ORM querying guide: https://docs.sqlalchemy.org/en/20/orm/queryguide/
- HTTP semantics and status codes: https://httpwg.org/specs/rfc9110.html
- REST resource design discussions: https://restfulapi.net/

---

## Expected Outcome

At the end of Phase 4, the project should have:

- a working `GET /api/v1/users/{user_id}/orders` endpoint
- user deletion blocked when related orders exist
- automated tests for both workflows
- clear examples of where REST begins to require extra orchestration

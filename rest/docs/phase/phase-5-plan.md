# Phase 5 Plan

## Objective

Phase 5 is about API quality, not new domain behavior.

The goal is to improve the current user and order flows by making the API:

- more consistent
- easier to observe
- easier to debug
- easier to test

This phase should stay focused on operational quality and avoid adding unrelated complexity.

---

## Features To Implement

### 1. Standardized Error Responses

Introduce one shared error response shape for handled failures.

Example:

```json
{
  "detail": "User with id 1 was not found.",
  "error_code": "user_not_found"
}
```

This should be used for:

- `404` not found errors
- `400` business rule or validation failures
- unexpected `500` errors where appropriate

### 2. Global Exception Handling

Move repeated error mapping logic out of route files and into centralized exception handlers.

This should reduce duplication in:

- `rest/app/api/v1/users.py`
- `rest/app/api/v1/orders.py`

### 3. Request Logging Middleware

Add logging middleware that records:

- HTTP method
- request path
- response status code
- processing time

This gives the project basic observability without adding external tooling.

### 4. Request Timing Middleware

Measure request duration for every request.

Use the timing in one or both of these ways:

- include it in logs
- expose it in a response header such as `X-Process-Time`

### 5. Pagination For List Endpoints

Add pagination to:

- `GET /api/v1/users`
- `GET /api/v1/orders`

Recommended query parameters:

- `page`
- `limit`

### 6. Filtering For Orders

Add basic filtering to:

- `GET /api/v1/orders`

Recommended initial filters:

- `user_id`
- `status`

---

## Recommended Implementation Order

Implement Phase 5 in this order:

1. shared error response schema
2. global exception handlers
3. request logging middleware
4. request timing middleware
5. pagination for users and orders
6. filtering for orders
7. tests for all Phase 5 behavior

This order keeps the work structured and prevents mixing cross-cutting concerns with endpoint behavior changes too early.

---

## Do We Need A Lot Of Data?

No. A large dataset is not required for the first implementation.

Use this rule of thumb:

- error handling: no extra data required
- middleware: no extra data required
- pagination: around `15-30` records is enough
- filtering: around `20-50` orders across a few users is enough

So the answer is no, you do not need a lot of data.

You only need enough records to make paging and filtering behavior visible.

---

## Recommended Test Dataset

For manual testing and API behavior checks, this is enough:

- `5` users
- `25` orders
- mixed order statuses such as:
  - `created`
  - `shipped`
  - `cancelled`

This dataset is small enough to manage and large enough to verify:

- pagination boundaries
- filtered results
- list ordering

If needed later, a simple seed script can be added. It is not required before Phase 5 starts.

---

## Boundaries For This Phase

Do not add these in Phase 5:

- caching
- authentication
- authorization
- advanced search
- background jobs
- complex analytics

Phase 5 should remain focused on API quality and observability.

---

## Domain Knowledge Sources

Use these sources to understand the concepts behind this phase:

- FastAPI User Guide: https://fastapi.tiangolo.com/
- FastAPI error handling: https://fastapi.tiangolo.com/tutorial/handling-errors/
- FastAPI middleware: https://fastapi.tiangolo.com/tutorial/middleware/
- FastAPI lifespan/events: https://fastapi.tiangolo.com/advanced/events/
- SQLAlchemy 2.0 docs: https://docs.sqlalchemy.org/en/20/
- HTTP semantics and status codes: https://httpwg.org/specs/rfc9110.html
- Python logging docs: https://docs.python.org/3/library/logging.html

---

## Expected Outcome

At the end of Phase 5, the API should have:

- cleaner error handling
- less duplicated route logic
- visible request logging
- measurable request timing
- paginated list endpoints
- basic order filtering

That should make the current REST implementation more realistic and easier to compare with the GraphQL and gRPC versions later.

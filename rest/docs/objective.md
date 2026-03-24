# REST Simulation Implementation Plan

## 1. Objective

Build a REST-based backend simulation that demonstrates how a small production-style system behaves when:

- resources are split across multiple services/modules
- data is stored in two separate databases
- client flows require both simple CRUD operations and cross-resource aggregation
- REST constraints begin to create friction compared with GraphQL and gRPC

This project should not be just a collection of endpoints. It should be structured to clearly show:

- resource-oriented API design
- service and repository separation
- multi-database coordination
- validation, error handling, pagination, filtering, and observability

---

## 2. Proposed Domain

Use an `Order Management` domain because it naturally supports:

- a `User` resource
- an `Order` resource
- one-to-many relationships
- cross-resource queries such as "fetch a user with all orders"

This keeps the project simple enough to build quickly while still exposing realistic REST limitations.

---

## 3. System Scope

### In Scope

- FastAPI application for REST endpoints
- separate user and order modules
- two SQLite databases
- SQLAlchemy models and persistence layer
- request validation with Pydantic schemas
- business logic layer for workflows
- CRUD endpoints for users
- CRUD endpoints for orders
- cross-resource endpoint for user orders
- pagination and filtering for list endpoints
- centralized error handling
- request logging and timing middleware
- versioned API routes such as `/api/v1/...`
- basic test coverage for key flows

### Out of Scope for Initial Version

- authentication and authorization
- background job processing
- distributed deployment
- external cache like Redis
- message queues
- container orchestration

These can be added later as stretch goals.

---

## 4. Architecture

### Layers

1. API Layer
   - exposes HTTP routes
   - validates input/output
   - maps domain errors to HTTP responses

2. Service Layer
   - contains business rules
   - coordinates repositories
   - handles cross-database workflows

3. Repository Layer
   - encapsulates database operations
   - isolates SQLAlchemy queries from services

4. Persistence Layer
   - maintains two separate databases:
     - `users.db`
     - `orders.db`

### High-Level Flow

```text
Client
  -> REST API
  -> Service Layer
  -> Repositories
  -> users.db / orders.db
```

---

## 5. Data Model

### User

Fields to implement:

- `id`
- `name`
- `email`
- `is_active`
- `created_at`

### Order

Fields to implement:

- `id`
- `user_id`
- `product_name`
- `quantity`
- `status`
- `created_at`

### Relationship Rule

- one user can have many orders
- user data and order data remain in different databases
- referential checks are enforced in application logic, not via cross-database foreign keys

---

## 6. API Surface

### User Endpoints

```text
GET    /api/v1/users
GET    /api/v1/users/{user_id}
POST   /api/v1/users
PATCH  /api/v1/users/{user_id}
DELETE /api/v1/users/{user_id}
```

### Order Endpoints

```text
GET    /api/v1/orders
GET    /api/v1/orders/{order_id}
POST   /api/v1/orders
PATCH  /api/v1/orders/{order_id}
DELETE /api/v1/orders/{order_id}
```

### Cross-Resource Endpoint

```text
GET /api/v1/users/{user_id}/orders
```

### Query Features

Implement on list endpoints where relevant:

- pagination: `page`, `limit`
- filtering: `user_id`, `status`
- optional sorting if time allows

---

## 7. Core Workflows

### Create User

- validate request body
- store user in `users.db`
- return `201 Created`

### Create Order

- validate request body
- verify that `user_id` exists in `users.db`
- create order in `orders.db`
- return `201 Created`

### Get User Orders

- fetch user from `users.db`
- fetch orders for that user from `orders.db`
- compose a single response

### Delete User

Decision for first version:

- prevent deletion if the user has existing orders
- return a validation/business error instead of silently cascading

This makes the multi-resource dependency explicit.

---

## 8. REST Behaviors to Demonstrate

The implementation should intentionally highlight common REST patterns and constraints.

### REST Strengths

- clean resource-based URLs
- clear HTTP semantics
- simple CRUD interactions

### REST Pain Points to Surface

- one screen may require multiple endpoints
- aggregation logic lives on the server or client
- cross-resource workflows require extra coordination
- service boundaries make consistency harder

These observations will later support comparison documents for GraphQL and gRPC.

---

## 9. Implementation Phases

### Phase 1: Project Foundation

Deliverables:

- FastAPI app bootstrap
- config and settings setup
- database initialization for two SQLite files
- SQLAlchemy base/models
- folder structure for api, services, repositories, schemas, db

Success criteria:

- application starts successfully
- both databases are created
- health check route responds

### Phase 2: User Resource

Deliverables:

- user model
- user schemas
- user repository
- user service
- user CRUD endpoints

Success criteria:

- full create/read/update/delete flow works for users
- invalid input returns proper `400` or `422`
- missing user returns `404`

### Phase 3: Order Resource

Deliverables:

- order model
- order schemas
- order repository
- order service
- order CRUD endpoints

Success criteria:

- orders can be created only for existing users
- order list and detail routes work correctly
- invalid `user_id` is rejected

### Phase 4: Cross-Database Workflows

Deliverables:

- `GET /api/v1/users/{user_id}/orders`
- service-level coordination between user and order modules
- business rule for user deletion with existing orders

Success criteria:

- aggregated response is correct
- cross-resource errors are handled consistently

### Phase 5: API Quality Improvements

Deliverables:

- pagination for list endpoints
- filtering for orders
- standardized error response format
- global exception handling
- request logging middleware
- request timing middleware

Success criteria:

- list endpoints support predictable query behavior
- logs provide basic request visibility
- runtime errors are converted into useful API responses

### Phase 6: Testing and Documentation

Deliverables:

- tests for user CRUD
- tests for order creation validation
- tests for cross-resource endpoint
- API usage examples in docs

Success criteria:

- critical workflows are covered by automated tests
- the project can be understood and run without reading source first

---

## 10. Suggested Directory Structure

```text
rest/
  app/
    main.py
    core/
      config.py
      exceptions.py
      middleware.py
    api/
      v1/
        users.py
        orders.py
    db/
      user_database.py
      order_database.py
      base.py
    models/
      user.py
      order.py
    schemas/
      user.py
      order.py
    repositories/
      user_repository.py
      order_repository.py
    services/
      user_service.py
      order_service.py
  docs/
    plan.md
  users.db
  orders.db
```

This structure keeps transport, business logic, and persistence concerns separated from the start.

---

## 11. Non-Functional Requirements

The implementation should also satisfy these baseline expectations:

- predictable HTTP status codes
- stateless request handling
- clear error messages
- modular code that can later be split into separate services
- simple local setup
- readable code intended for learning and comparison

---

## 12. Stretch Goals

Add these only after the core plan is complete:

- caching for selected GET routes
- API gateway simulation
- split user and order into separate FastAPI apps
- async communication simulation
- latency and failure injection for realism
- comparison notes showing how the same use case would look in GraphQL and gRPC

---

## 13. Final Expected Outcome

At the end of implementation, this REST project should provide:

- a clean multi-module FastAPI codebase
- two independent databases
- realistic CRUD and aggregation flows
- observable examples of where REST works well
- concrete examples of where REST becomes cumbersome

This will make the repository a strong baseline for later GraphQL and gRPC simulations.

---

## 14. Execution Reference

Use [`implementation.md`](C:\Users\USER\work\PERSONAL%20PROJECTS\REST-GraphQL-gRPC-Simulations\rest\docs\implementation.md) as the step-by-step execution guide for building this plan.

The intent is:

- `plan.md` defines what will be built
- `implementation.md` defines how to approach and sequence the work

# REST API Pain Points In This Project

The REST pain points in this project appear when one workflow needs data from more than one resource.

In the current setup:

- `users` live in one database
- `orders` live in another database
- the relationship is enforced in application logic, not by the database itself

That creates these practical REST pain points.

## 1. Cross-Resource Reads Need Extra Work

A simple question like "show me a user and all their orders" is no longer a single-resource lookup.

The backend has to:

- fetch the user from `users.db`
- fetch related orders from `orders.db`
- combine both into one response

That is why the project needs an extra endpoint like:

```text
GET /users/{user_id}/orders
```

## 2. Cross-Resource Writes Need Coordination

Creating an order is not just an insert into the orders table.

The service must:

- check whether the user exists in the user database
- then create the order in the order database

So even `POST /orders` becomes a coordinated workflow instead of isolated CRUD.

## 3. Business Rules Spread Across Resources

Deleting a user is no longer a simple delete operation.

The backend must:

- load the user
- check whether related orders exist in another database
- block deletion if orders are present

This means resource operations stop being simple single-resource actions and become orchestration logic.

## 4. More Endpoints Are Needed For Real Usage

REST stays clean when resources are independent. Once the client needs combined data, the basic CRUD endpoints are not enough.

That often leads to extra endpoints such as:

- `/users/{id}/orders`

This helps the client, but it also grows the API surface.

## 5. Consistency Is Managed In Application Code

There is no cross-database foreign key enforcing integrity here.

Correctness depends on the service layer:

- order creation must validate `user_id`
- user deletion must check for existing orders

If the application logic is wrong, invalid states can still happen.

## Summary

The main REST pain point in this project is that resource-oriented design is simple at first, but real workflows quickly require:

- aggregation
- cross-resource validation
- orchestration logic
- extra endpoints

That is the point where REST starts feeling more cumbersome for connected data flows.

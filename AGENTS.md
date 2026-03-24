# Repository Guidelines

## Project Structure & Module Organization

The repository currently contains project metadata at the root (`pyproject.toml`, `README.md`, `main.py`) and REST-specific work under [`rest/`](C:\Users\USER\work\PERSONAL%20PROJECTS\REST-GraphQL-gRPC-Simulations\rest). Planning documents live in [`rest/docs/`](C:\Users\USER\work\PERSONAL%20PROJECTS\REST-GraphQL-gRPC-Simulations\rest\docs), including `plan.md` and `implementation.md`.

Application code for the REST simulation should be added under `rest/app/` using the planned layered structure:

- `api/` for route handlers
- `services/` for business logic
- `repositories/` for database access
- `models/` and `schemas/` for SQLAlchemy/Pydantic types
- `db/` for database setup

Place automated tests in a top-level `tests/` directory once implementation begins.

## Build, Test, and Development Commands

- `uv run python main.py`: run the current root entrypoint.
- `uv run python -m pytest`: run the test suite once tests exist.
- `uv sync`: install dependencies from `pyproject.toml`.

If the REST app uses FastAPI/Uvicorn, prefer a command such as `uv run uvicorn rest.app.main:app --reload` for local development.

## Coding Style & Naming Conventions

Target Python `3.12+` and use 4-space indentation. Keep modules small and aligned with the architecture: routes should only handle HTTP concerns, services should hold workflow rules, and repositories should contain persistence logic.

Do not overcomplicate the implementation. Prefer simple, structured solutions over abstractions that are not yet needed. Build only what the current phase requires.

Naming patterns:

- files/modules: `snake_case.py`
- classes: `PascalCase`
- functions/variables: `snake_case`
- constants: `UPPER_SNAKE_CASE`

Prefer explicit, descriptive names like `user_service.py` over generic files like `utils.py`.

## Implementation Approach

Work incrementally. Do not generate large batches of code across many files at once.

Preferred workflow:

1. implement one file or one tightly scoped feature
2. stop and ask the user to review it
3. proceed only after that review to the next file or feature

This repository should evolve in small, inspectable steps. Favor clarity and structure over speed.

## Testing Guidelines

Use `pytest`. Name test files `test_<feature>.py` and keep test cases focused on behavior, not implementation details. Cover at least:

- user CRUD flows
- order creation validation
- cross-resource workflows such as `GET /users/{id}/orders`

## Commit & Pull Request Guidelines

Existing history uses short, direct commit subjects such as `initial commit for rest api dev for phase-1`. Keep commits imperative and scoped, for example: `add user service and repository`.

Pull requests should include:

- a brief summary of the change
- impacted paths or modules
- test status
- sample request/response output for API changes when relevant

## Architecture Notes

Treat [`rest/docs/plan.md`](C:\Users\USER\work\PERSONAL%20PROJECTS\REST-GraphQL-gRPC-Simulations\rest\docs\plan.md) as the source of truth for scope and [`rest/docs/implementation.md`](C:\Users\USER\work\PERSONAL%20PROJECTS\REST-GraphQL-gRPC-Simulations\rest\docs\implementation.md) as the execution order.

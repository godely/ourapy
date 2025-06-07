# Milestone 2: API Client Improvement Roadmap

This document outlines a set of focused tasks to enhance the Oura API Python client’s robustness, completeness, correctness, and code hygiene. These items build on the findings from **implementation_verification_report.md** and aim to be achievable within 5–10 discrete work items.

## Task 1: Unify endpoint URL handling
- Remove duplicate `/v2` prefixes in endpoint definitions and consolidate URL construction in `OuraClient._make_request`.
- Refactor all endpoint modules under `oura_api_client/api/` to use relative paths (e.g. `/usercollection/...`) and update corresponding tests.

## Task 2: Centralize query parameter construction
- Extract common logic for date conversion, pagination, and filtering out `None` values into a shared helper in `oura_api_client/utils`.
- Refactor each endpoint method to leverage the new utility instead of manual `params` dict assembly.

## Task 3: Standardize data models
- Choose a single modeling approach (either Pydantic or dataclasses) and migrate all existing models (`oura_api_client/models/`) accordingly.
- Remove inconsistent or duplicate model definitions and clear out any outdated TODO comments.

## Task 4: Enhance error handling and retry logic
- Introduce a custom exception hierarchy (e.g. `OuraAPIError`) that wraps HTTP errors and surfaces status codes/messages.
- Add optional retry/backoff support for transient failures (e.g. via `tenacity` or built‑in logic).

## Task 5: Expand HTTP method support for webhook management
- Extend `OuraClient._make_request` to support `POST`, `PUT`, `DELETE`, and `PATCH` methods.
- Implement full CRUD operations for webhook subscriptions in `oura_api_client/api/webhook.py`, including create/update/delete/renew.
- Add models and unit tests for webhook subscription management.

## Task 6: Increase test coverage across all endpoints
- Write unit tests for all currently untested endpoint modules: `daily_readiness`, `daily_spo2`, `sleep_time`, `rest_mode_period`, `daily_stress`, `daily_resilience`, `daily_cardiovascular_age`, `vo2_max`, `ring_configuration`, `personal`, `session`, `tag`, `enhanced_tag`, and `workout`.
- Cover success, failure, and raw‐response (`return_model=False`) paths, aiming for ≥90% coverage in `oura_api_client/api/` and `oura_api_client/models/`.

## Task 7: Implement pagination helpers
- Provide high‑level iterators or stream methods that automatically follow `next_token` to yield all items transparently (e.g. `client.heartrate.stream()`).
- Update examples in README to showcase seamless pagination.

## Task 8: Improve documentation and usage examples
- Update `README.md` to include all endpoint methods, parameters, and real‑world usage snippets (pagination, error handling, webhook management).
- Add a summary table of endpoints, valid parameters, and response models for quick reference.

## Task 9: Integrate CI/CD tooling
- Add GitHub Actions workflows for linting (black, flake8), type checking (mypy), and testing across supported Python versions.
- Include coverage reporting and status badges in `README.md`.

## Task 10: Versioning and release process
- Introduce a `__version__` attribute (e.g. in `oura_api_client/__init__.py`) and update `setup.py` accordingly.
- Add a `CHANGELOG.md` to track notable changes across releases.
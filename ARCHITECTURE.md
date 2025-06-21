# Ourapy Architecture & Critical Context

## Project Overview
Python client library for Oura Ring API v2, designed for simplicity and reliability.

## Key Architecture Decisions (Gustavo's Technical Direction)

### Error Handling Philosophy
- **Custom Exception Hierarchy**: Specific exceptions for different HTTP error codes
- **Retry Strategy**: Exponential backoff for transient failures only (5xx, timeouts, connection)
- **Rate Limit Compliance**: Respects Retry-After headers, max 5min wait
- **User Control**: Configurable via RetryConfig, can be disabled

### API Client Design
- **Single Entry Point**: OuraClient class with endpoint modules
- **Consistent Patterns**: All requests go through `_make_request()` method
- **URL Normalization**: Handles /v2 prefix duplication automatically
- **Type Safety**: Pydantic models for all responses

### Testing Strategy
- **Parallel Execution**: pytest-xdist for 94x speedup on multi-core systems
- **Mock-based**: No real API calls in CI, comprehensive error scenario coverage
- **Real API Validation**: Separate live testing scripts (gitignored)

## Critical Technical Context

### API Integration Notes
- **Time-Series Data**: Many fields use SampleModel structure {interval, items[], timestamp}
- **Rate Limiting**: API respects standard HTTP patterns with Retry-After headers

### Development Workflow Optimizations
- **Local Development**: Use `pytest -n auto` for parallel testing
- **CI Environment**: Standard sequential testing for stability
- **Debugging**: Systematic approaches documented in CLAUDE.md

### Code Organization
```
oura_api_client/
├── api/           # Endpoint modules (daily_activity, sleep, etc.)
├── models/        # Pydantic response models
├── exceptions.py  # Custom exception hierarchy
└── utils/         # Retry logic, query params, helpers
```

## Performance Characteristics
- **Local Testing**: Parallel execution with pytest-xdist (15-25 seconds for full suite)
- **Error Handling**: Minimal overhead per request, configurable retry behavior
- **Memory**: Minimal footprint, stateless design

## Integration Patterns
- **Authentication**: Bearer token in headers
- **Pagination**: next_token pattern for large datasets
- **Date Handling**: ISO format strings, automatic conversion utilities
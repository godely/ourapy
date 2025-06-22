# Error Handling Enhancement Summary

## What We Implemented

### 1. Custom Exception Hierarchy (`oura_api_client/exceptions.py`)
- **Base Exception**: `OuraAPIError` - Base class for all API errors with status code, endpoint, and response tracking
- **Specific Exceptions**:
  - `OuraAuthenticationError` (401)
  - `OuraAuthorizationError` (403)
  - `OuraNotFoundError` (404)
  - `OuraRateLimitError` (429) - Includes `retry_after` support
  - `OuraClientError` (4xx)
  - `OuraServerError` (5xx)
  - `OuraConnectionError` - Network connection failures
  - `OuraTimeoutError` - Request timeouts
- **Factory Function**: `create_api_error()` automatically creates the appropriate exception based on HTTP status code

### 2. Retry Logic (`oura_api_client/utils/retry.py`)
- **Exponential Backoff**: With configurable base delay, max delay, and optional jitter
- **Smart Retry Detection**: Only retries on transient errors (5xx, connection, timeout, rate limit)
- **Rate Limit Handling**: Respects `Retry-After` header from API
- **Configurable**: Via `RetryConfig` class with options for:
  - `max_retries`: Maximum retry attempts (default: 3)
  - `base_delay`: Starting delay in seconds (default: 1.0)
  - `max_delay`: Maximum delay between retries (default: 60.0)
  - `jitter`: Whether to add random jitter (default: true)
  - `enabled`: Toggle retry on/off (default: true)

### 3. Updated Client (`oura_api_client/api/client.py`)
- Integrated retry logic into `_make_request()` method
- Proper exception handling for all request types
- Support for both retry-enabled and direct request modes
- Clean separation of concerns with `_make_single_request()` and `_make_request_with_retry()`

### 4. Comprehensive Tests (`tests/test_error_handling.py`)
- 18 test cases covering:
  - Exception creation and behavior
  - Retry logic calculations
  - Client error handling
  - Rate limiting scenarios
  - Connection and timeout errors
  - Endpoint normalization
  - Retry configuration

## Usage Examples

### Basic Usage (Default Retry Enabled)
```python
client = OuraClient("your_token")
# Automatically retries on transient errors
```

### Custom Retry Configuration
```python
from oura_api_client import OuraClient, RetryConfig

retry_config = RetryConfig(
    max_retries=5,
    base_delay=2.0,
    max_delay=120.0,
    jitter=True
)
client = OuraClient("your_token", retry_config=retry_config)
```

### Disable Retry
```python
retry_config = RetryConfig(enabled=False)
client = OuraClient("your_token", retry_config=retry_config)
```

### Exception Handling
```python
from oura_api_client import (
    OuraClient,
    OuraAuthenticationError,
    OuraRateLimitError,
    OuraServerError
)

client = OuraClient("your_token")

try:
    data = client.daily_activity.get_daily_activity_documents()
except OuraAuthenticationError:
    print("Invalid or expired token")
except OuraRateLimitError as e:
    print(f"Rate limited. Retry after {e.retry_after} seconds")
except OuraServerError:
    print("Server error - request was automatically retried")
```

## Benefits
1. **Resilience**: Automatic retry on transient failures
2. **User Experience**: Clear, specific error messages
3. **Rate Limit Compliance**: Respects API rate limits
4. **Flexibility**: Configurable retry behavior
5. **Backward Compatible**: Existing code continues to work
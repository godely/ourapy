"""Custom exceptions for the Oura API client."""

from typing import Optional
import requests


class OuraAPIError(Exception):
    """Base exception class for Oura API errors."""
    
    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response: Optional[requests.Response] = None,
        endpoint: Optional[str] = None
    ):
        """Initialize OuraAPIError.
        
        Args:
            message: Error message
            status_code: HTTP status code if available
            response: Original HTTP response object
            endpoint: The API endpoint that failed
        """
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.response = response
        self.endpoint = endpoint
        
    def __str__(self) -> str:
        """Return string representation of the error."""
        parts = [self.message]
        if self.status_code:
            parts.append(f"Status: {self.status_code}")
        if self.endpoint:
            parts.append(f"Endpoint: {self.endpoint}")
        return " | ".join(parts)


class OuraAuthenticationError(OuraAPIError):
    """Raised when authentication fails (401 Unauthorized)."""
    pass


class OuraAuthorizationError(OuraAPIError):
    """Raised when authorization fails (403 Forbidden)."""
    pass


class OuraNotFoundError(OuraAPIError):
    """Raised when a resource is not found (404 Not Found)."""
    pass


class OuraRateLimitError(OuraAPIError):
    """Raised when rate limit is exceeded (429 Too Many Requests)."""
    
    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response: Optional[requests.Response] = None,
        endpoint: Optional[str] = None,
        retry_after: Optional[int] = None
    ):
        """Initialize OuraRateLimitError.
        
        Args:
            message: Error message
            status_code: HTTP status code
            response: Original HTTP response object
            endpoint: The API endpoint that failed
            retry_after: Seconds to wait before retrying (from Retry-After header)
        """
        super().__init__(message, status_code, response, endpoint)
        self.retry_after = retry_after


class OuraServerError(OuraAPIError):
    """Raised when server encounters an error (5xx status codes)."""
    pass


class OuraClientError(OuraAPIError):
    """Raised when client request is invalid (4xx status codes, except specific ones)."""
    pass


class OuraConnectionError(OuraAPIError):
    """Raised when connection to API fails."""
    pass


class OuraTimeoutError(OuraAPIError):
    """Raised when request times out."""
    pass


def _extract_error_message(response: requests.Response, status_code: int) -> str:
    """Extract error message from response.
    
    Args:
        response: HTTP response object
        status_code: HTTP status code
        
    Returns:
        Error message string
    """
    try:
        error_data = response.json()
        if isinstance(error_data, dict):
            message = error_data.get('error', error_data.get('message', ''))
            if message:
                return message
    except (ValueError, KeyError):
        pass
    return f"HTTP {status_code}: {response.reason}"


def _extract_retry_after(response: requests.Response) -> Optional[int]:
    """Extract retry-after value from response headers.
    
    Args:
        response: HTTP response object
        
    Returns:
        Retry-after value in seconds, or None
    """
    retry_after_header = response.headers.get('Retry-After')
    if retry_after_header:
        try:
            return int(retry_after_header)
        except ValueError:
            pass
    return None


def create_api_error(
    response: requests.Response,
    endpoint: Optional[str] = None,
    message: Optional[str] = None
) -> OuraAPIError:
    """Create appropriate OuraAPIError based on response status code.
    
    Args:
        response: HTTP response object
        endpoint: The API endpoint that failed
        message: Custom error message (will be auto-generated if not provided)
        
    Returns:
        Appropriate OuraAPIError subclass instance
    """
    status_code = response.status_code
    
    # Get error message
    if not message:
        message = _extract_error_message(response, status_code)
    
    # Map status codes to exception classes
    error_mapping = {
        401: OuraAuthenticationError,
        403: OuraAuthorizationError,
        404: OuraNotFoundError,
    }
    
    # Check specific status codes first
    if status_code in error_mapping:
        return error_mapping[status_code](message, status_code, response, endpoint)
    
    # Handle rate limit error with retry-after
    if status_code == 429:
        retry_after = _extract_retry_after(response)
        return OuraRateLimitError(message, status_code, response, endpoint, retry_after)
    
    # Handle ranges
    if 400 <= status_code < 500:
        return OuraClientError(message, status_code, response, endpoint)
    elif 500 <= status_code < 600:
        return OuraServerError(message, status_code, response, endpoint)
    else:
        return OuraAPIError(message, status_code, response, endpoint)

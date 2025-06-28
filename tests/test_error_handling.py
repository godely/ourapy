"""Tests for error handling and retry logic."""

import unittest
from unittest.mock import patch, MagicMock
import requests
from oura_api_client.api.client import OuraClient
from oura_api_client.exceptions import (
    OuraAPIError,
    OuraAuthenticationError,
    OuraAuthorizationError,
    OuraNotFoundError,
    OuraRateLimitError,
    OuraServerError,
    OuraClientError,
    OuraConnectionError,
    OuraTimeoutError,
    create_api_error,
)
from oura_api_client.utils import RetryConfig, exponential_backoff, should_retry


class TestExceptions(unittest.TestCase):
    """Test custom exception classes."""

    def test_oura_api_error(self):
        """Test OuraAPIError base class."""
        error = OuraAPIError("Test error", status_code=400, endpoint="/test")
        self.assertEqual(str(error), "Test error | Status: 400 | Endpoint: /test")
        self.assertEqual(error.message, "Test error")
        self.assertEqual(error.status_code, 400)
        self.assertEqual(error.endpoint, "/test")

    def test_oura_rate_limit_error(self):
        """Test OuraRateLimitError with retry_after."""
        error = OuraRateLimitError(
            "Rate limit exceeded", status_code=429, endpoint="/test", retry_after=60
        )
        self.assertEqual(error.retry_after, 60)
        self.assertEqual(error.status_code, 429)

    def test_create_api_error_with_json_response(self):
        """Test create_api_error with JSON error response."""
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.reason = "Unauthorized"
        mock_response.json.return_value = {"error": "Invalid token"}

        error = create_api_error(mock_response, "/test")
        self.assertIsInstance(error, OuraAuthenticationError)
        self.assertEqual(error.message, "Invalid token")
        self.assertEqual(error.status_code, 401)
        self.assertEqual(error.endpoint, "/test")

    def test_create_api_error_without_json(self):
        """Test create_api_error when response has no JSON."""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.reason = "Internal Server Error"
        mock_response.json.side_effect = ValueError("No JSON")

        error = create_api_error(mock_response, "/test")
        self.assertIsInstance(error, OuraServerError)
        self.assertEqual(error.message, "HTTP 500: Internal Server Error")

    def test_create_api_error_with_retry_after(self):
        """Test create_api_error for rate limit with Retry-After header."""
        mock_response = MagicMock()
        mock_response.status_code = 429
        mock_response.reason = "Too Many Requests"
        mock_response.headers = {"Retry-After": "120"}
        mock_response.json.return_value = {"error": "Rate limit exceeded"}

        error = create_api_error(mock_response, "/test")
        self.assertIsInstance(error, OuraRateLimitError)
        self.assertEqual(error.retry_after, 120)

    def test_create_api_error_status_mapping(self):
        """Test that create_api_error returns correct exception types."""
        test_cases = [
            (401, OuraAuthenticationError),
            (403, OuraAuthorizationError),
            (404, OuraNotFoundError),
            (429, OuraRateLimitError),
            (400, OuraClientError),
            (422, OuraClientError),
            (500, OuraServerError),
            (502, OuraServerError),
            (503, OuraServerError),
        ]

        for status_code, expected_type in test_cases:
            mock_response = MagicMock()
            mock_response.status_code = status_code
            mock_response.reason = f"Status {status_code}"
            mock_response.json.side_effect = ValueError()
            mock_response.headers = {}

            error = create_api_error(mock_response)
            self.assertIsInstance(error, expected_type)


class TestRetryLogic(unittest.TestCase):
    """Test retry utilities."""

    def test_exponential_backoff(self):
        """Test exponential backoff calculation."""
        # Test without jitter
        self.assertEqual(exponential_backoff(0, base_delay=1.0, jitter=False), 1.0)
        self.assertEqual(exponential_backoff(1, base_delay=1.0, jitter=False), 2.0)
        self.assertEqual(exponential_backoff(2, base_delay=1.0, jitter=False), 4.0)
        self.assertEqual(exponential_backoff(3, base_delay=1.0, jitter=False), 8.0)

        # Test max delay
        self.assertEqual(
            exponential_backoff(10, base_delay=1.0, max_delay=5.0, jitter=False), 5.0
        )

        # Test with jitter (should be within ±25% of base value)
        for attempt in range(5):
            delay = exponential_backoff(attempt, base_delay=1.0, jitter=True)
            expected = 1.0 * (2**attempt)
            self.assertGreaterEqual(delay, expected * 0.75)
            self.assertLessEqual(delay, expected * 1.25)

    def test_should_retry(self):
        """Test should_retry logic."""
        # Test max retries exceeded
        error = OuraServerError("Server error")
        self.assertFalse(should_retry(error, attempt=3, max_retries=3))
        self.assertTrue(should_retry(error, attempt=2, max_retries=3))

        # Test retryable errors
        retryable_errors = [
            OuraServerError("Server error"),
            OuraConnectionError("Connection failed"),
            OuraTimeoutError("Request timed out"),
            OuraRateLimitError("Rate limited", retry_after=60),
        ]

        for error in retryable_errors:
            self.assertTrue(should_retry(error, attempt=0, max_retries=3))

        # Test non-retryable errors
        non_retryable_errors = [
            OuraAuthenticationError("Invalid token"),
            OuraAuthorizationError("Forbidden"),
            OuraNotFoundError("Not found"),
            OuraClientError("Bad request"),
        ]

        for error in non_retryable_errors:
            self.assertFalse(should_retry(error, attempt=0, max_retries=3))

        # Test rate limit with large retry_after
        error = OuraRateLimitError("Rate limited", retry_after=600)
        self.assertFalse(should_retry(error, attempt=0, max_retries=3))


class TestOuraClientErrorHandling(unittest.TestCase):
    """Test OuraClient error handling."""

    def setUp(self):
        """Set up test client."""
        self.client = OuraClient("test_token")

    @patch("requests.get")
    def test_make_request_success(self, mock_get):
        """Test successful request."""
        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.json.return_value = {"data": "test"}
        mock_get.return_value = mock_response

        result = self.client._make_request("/test")
        self.assertEqual(result, {"data": "test"})
        mock_get.assert_called_once()

    @patch("requests.get")
    def test_make_request_http_error(self, mock_get):
        """Test request with HTTP error."""
        mock_response = MagicMock()
        mock_response.ok = False
        mock_response.status_code = 404
        mock_response.reason = "Not Found"
        mock_response.json.return_value = {"error": "Resource not found"}
        mock_get.return_value = mock_response

        with self.assertRaises(OuraNotFoundError) as cm:
            self.client._make_request("/test")

        self.assertEqual(cm.exception.message, "Resource not found")
        self.assertEqual(cm.exception.status_code, 404)
        self.assertEqual(cm.exception.endpoint, "/test")

    @patch("requests.get")
    def test_make_request_timeout(self, mock_get):
        """Test request timeout."""
        mock_get.side_effect = requests.exceptions.Timeout("Timeout")

        with self.assertRaises(OuraTimeoutError) as cm:
            self.client._make_request("/test")

        self.assertIn("timed out", cm.exception.message)
        self.assertEqual(cm.exception.endpoint, "/test")

    @patch("requests.get")
    def test_make_request_connection_error(self, mock_get):
        """Test connection error."""
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection failed")

        with self.assertRaises(OuraConnectionError) as cm:
            self.client._make_request("/test")

        self.assertIn("Failed to connect", cm.exception.message)
        self.assertEqual(cm.exception.endpoint, "/test")

    @patch("requests.get")
    def test_make_request_with_retry_success(self, mock_get):
        """Test successful retry after transient error."""
        # First call fails with server error, second succeeds
        mock_response_error = MagicMock()
        mock_response_error.ok = False
        mock_response_error.status_code = 500
        mock_response_error.reason = "Internal Server Error"
        mock_response_error.json.return_value = {}

        mock_response_success = MagicMock()
        mock_response_success.ok = True
        mock_response_success.json.return_value = {"data": "success"}

        mock_get.side_effect = [mock_response_error, mock_response_success]

        # Enable retry
        self.client.retry_config = RetryConfig(
            max_retries=3, base_delay=0.01, jitter=False  # Short delay for testing
        )

        result = self.client._make_request("/test")
        self.assertEqual(result, {"data": "success"})
        self.assertEqual(mock_get.call_count, 2)

    @patch("requests.get")
    @patch("time.sleep")
    def test_make_request_with_retry_exhausted(self, mock_sleep, mock_get):
        """Test retry exhaustion."""
        mock_response = MagicMock()
        mock_response.ok = False
        mock_response.status_code = 500
        mock_response.reason = "Internal Server Error"
        mock_response.json.return_value = {"error": "Server error"}
        mock_get.return_value = mock_response

        # Enable retry with limited attempts
        self.client.retry_config = RetryConfig(
            max_retries=2, base_delay=0.01, jitter=False
        )

        with self.assertRaises(OuraServerError) as cm:
            self.client._make_request("/test")

        self.assertEqual(cm.exception.message, "Server error")
        self.assertEqual(mock_get.call_count, 3)  # Initial + 2 retries

    @patch("requests.get")
    @patch("time.sleep")
    def test_make_request_with_rate_limit_retry(self, mock_sleep, mock_get):
        """Test retry with rate limit and Retry-After header."""
        mock_response_rate_limit = MagicMock()
        mock_response_rate_limit.ok = False
        mock_response_rate_limit.status_code = 429
        mock_response_rate_limit.reason = "Too Many Requests"
        mock_response_rate_limit.headers = {"Retry-After": "2"}
        mock_response_rate_limit.json.return_value = {"error": "Rate limited"}

        mock_response_success = MagicMock()
        mock_response_success.ok = True
        mock_response_success.json.return_value = {"data": "success"}

        mock_get.side_effect = [mock_response_rate_limit, mock_response_success]

        self.client.retry_config = RetryConfig(max_retries=3)

        result = self.client._make_request("/test")
        self.assertEqual(result, {"data": "success"})

        # Should have slept for the Retry-After duration
        mock_sleep.assert_called_once_with(2)

    @patch("requests.get")
    def test_make_request_no_retry_on_client_error(self, mock_get):
        """Test that client errors are not retried."""
        mock_response = MagicMock()
        mock_response.ok = False
        mock_response.status_code = 400
        mock_response.reason = "Bad Request"
        mock_response.json.return_value = {"error": "Invalid parameters"}
        mock_get.return_value = mock_response

        self.client.retry_config = RetryConfig(max_retries=3)

        with self.assertRaises(OuraClientError) as cm:
            self.client._make_request("/test")

        self.assertEqual(cm.exception.message, "Invalid parameters")
        self.assertEqual(mock_get.call_count, 1)  # No retries

    def test_make_request_endpoint_normalization(self):
        """Test endpoint normalization."""
        with patch("requests.get") as mock_get:
            mock_response = MagicMock()
            mock_response.ok = True
            mock_response.json.return_value = {}
            mock_get.return_value = mock_response

            # Test various endpoint formats
            test_cases = [
                ("/test", "https://api.ouraring.com/v2/test"),
                ("test", "https://api.ouraring.com/v2/test"),
                ("/v2/test", "https://api.ouraring.com/v2/test"),
                ("v2/test", "https://api.ouraring.com/v2/test"),
            ]

            for endpoint, expected_url in test_cases:
                mock_get.reset_mock()
                self.client._make_request(endpoint)
                actual_url = mock_get.call_args[0][0]
                self.assertEqual(actual_url, expected_url)

    def test_retry_config_disabled(self):
        """Test that retry can be disabled."""
        self.client.retry_config = RetryConfig(enabled=False)

        with patch("requests.get") as mock_get:
            mock_response = MagicMock()
            mock_response.ok = False
            mock_response.status_code = 500
            mock_response.reason = "Server Error"
            mock_response.json.return_value = {}
            mock_get.return_value = mock_response

            with self.assertRaises(OuraServerError):
                self.client._make_request("/test")

            # Should not retry when disabled
            self.assertEqual(mock_get.call_count, 1)


if __name__ == "__main__":
    unittest.main()

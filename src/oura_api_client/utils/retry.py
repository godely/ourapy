"""Retry utilities for handling transient failures."""

import time
import random
from typing import Callable
from ..exceptions import (
    OuraRateLimitError,
    OuraServerError,
    OuraConnectionError,
    OuraTimeoutError,
)


def exponential_backoff(
    attempt: int, base_delay: float = 1.0, max_delay: float = 60.0, jitter: bool = True
) -> float:
    """Calculate exponential backoff delay.

    Args:
        attempt: Current attempt number (0-based)
        base_delay: Base delay in seconds
        max_delay: Maximum delay in seconds
        jitter: Whether to add random jitter

    Returns:
        Delay in seconds
    """
    delay = base_delay * (2**attempt)
    delay = min(delay, max_delay)

    if jitter:
        # Add ±25% jitter
        jitter_range = delay * 0.25
        delay += random.uniform(-jitter_range, jitter_range)

    return max(0, delay)


def should_retry(exception: Exception, attempt: int, max_retries: int) -> bool:
    """Determine if an exception should trigger a retry.

    Args:
        exception: The exception that occurred
        attempt: Current attempt number (0-based)
        max_retries: Maximum number of retries allowed

    Returns:
        True if should retry, False otherwise
    """
    if attempt >= max_retries:
        return False

    # Retry on specific transient errors
    if isinstance(exception, (OuraServerError, OuraConnectionError, OuraTimeoutError)):
        return True

    # Retry on rate limit errors if retry_after is reasonable
    if isinstance(exception, OuraRateLimitError):
        if exception.retry_after and exception.retry_after <= 300:  # Max 5 minutes
            return True
        elif (
            not exception.retry_after
        ):  # No retry-after header, use exponential backoff
            return True

    return False


def retry_with_backoff(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    jitter: bool = True,
):
    """Decorator factory to add retry logic with exponential backoff.

    Args:
        max_retries: Maximum number of retries
        base_delay: Base delay for exponential backoff
        max_delay: Maximum delay between retries
        jitter: Whether to add random jitter

    Returns:
        Decorator function
    """

    def decorator(func: Callable) -> Callable:
        """Actual decorator that wraps the function.

        Args:
            func: Function to wrap

        Returns:
            Wrapped function with retry logic
        """

        def wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(max_retries + 1):  # +1 for initial attempt
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e

                    if not should_retry(e, attempt, max_retries):
                        raise

                    # Calculate delay
                    if isinstance(e, OuraRateLimitError) and e.retry_after:
                        delay = e.retry_after
                    else:
                        delay = exponential_backoff(
                            attempt, base_delay, max_delay, jitter
                        )

                    # Wait before retry
                    if delay > 0:
                        time.sleep(delay)

            # If we get here, all retries failed
            raise last_exception

        return wrapper

    return decorator


class RetryConfig:
    """Configuration for retry behavior."""

    def __init__(
        self,
        max_retries: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 60.0,
        jitter: bool = True,
        enabled: bool = True,
    ):
        """Initialize retry configuration.

        Args:
            max_retries: Maximum number of retries
            base_delay: Base delay for exponential backoff
            max_delay: Maximum delay between retries
            jitter: Whether to add random jitter
            enabled: Whether retry is enabled
        """
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.jitter = jitter
        self.enabled = enabled

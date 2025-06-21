"""Oura API Client - A Python library for the Oura Ring API."""

from .api.client import OuraClient
from .exceptions import (
    OuraAPIError,
    OuraAuthenticationError,
    OuraAuthorizationError,
    OuraNotFoundError,
    OuraRateLimitError,
    OuraServerError,
    OuraClientError,
    OuraConnectionError,
    OuraTimeoutError
)
from .utils import RetryConfig

__version__ = "0.1.0"

__all__ = [
    "OuraClient",
    "OuraAPIError",
    "OuraAuthenticationError",
    "OuraAuthorizationError",
    "OuraNotFoundError",
    "OuraRateLimitError",
    "OuraServerError",
    "OuraClientError",
    "OuraConnectionError",
    "OuraTimeoutError",
    "RetryConfig"
]

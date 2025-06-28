"""Utilities for building query parameters for Oura API requests."""

from datetime import date
from typing import Optional, Union, Dict, Any


def convert_date_to_string(date_param: Optional[Union[str, date]]) -> Optional[str]:
    """Convert a date parameter to ISO format string if it's a date object.

    Args:
        date_param: Date parameter that can be a string, date object, or None

    Returns:
        ISO format date string or None
    """
    if isinstance(date_param, date):
        return date_param.isoformat()
    return date_param


def build_query_params(
    start_date: Optional[Union[str, date]] = None,
    end_date: Optional[Union[str, date]] = None,
    next_token: Optional[str] = None,
    **kwargs: Any
) -> Dict[str, Any]:
    """Build query parameters dictionary for API requests.

    This function handles common query parameter patterns:
    - Converts date objects to ISO format strings
    - Filters out None values
    - Supports additional parameters via kwargs

    Args:
        start_date: Start date for filtering (string or date object)
        end_date: End date for filtering (string or date object)
        next_token: Token for pagination
        **kwargs: Additional query parameters

    Returns:
        Dictionary of query parameters with None values filtered out
    """
    params = {
        "start_date": convert_date_to_string(start_date),
        "end_date": convert_date_to_string(end_date),
        "next_token": next_token,
        **kwargs,
    }

    # Filter out None values
    return {k: v for k, v in params.items() if v is not None}

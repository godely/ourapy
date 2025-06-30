"""Pagination utilities for streaming data from Oura API endpoints."""

from typing import Iterator, Callable, TypeVar, Any, Optional, Union
from datetime import date

# Type variables for generic pagination
T = TypeVar('T')  # For individual data items
ResponseType = TypeVar('ResponseType')  # For response objects


def stream_paginated_data(
    fetch_function: Callable[..., ResponseType],
    start_date: Optional[Union[str, date]] = None,
    end_date: Optional[Union[str, date]] = None,
    **kwargs: Any
) -> Iterator[T]:
    """
    Stream all paginated data from an API endpoint automatically.

    This function handles the pagination logic by following next_token
    until all data is retrieved, yielding individual items one by one.

    Args:
        fetch_function: The endpoint method to call (e.g., get_daily_sleep_documents)
        start_date: Optional start date for filtering
        end_date: Optional end date for filtering
        **kwargs: Additional parameters to pass to the fetch function

    Yields:
        Individual data items from the API response

    Example:
        >>> for sleep_record in stream_paginated_data(
        ...     client.daily_sleep.get_daily_sleep_documents,
        ...     start_date="2024-01-01"
        ... ):
        ...     print(sleep_record.score)
    """
    next_token = None

    while True:
        # Call the fetch function with current pagination token
        response = fetch_function(
            start_date=start_date,
            end_date=end_date,
            next_token=next_token,
            **kwargs
        )

        # Yield each individual item from the current page
        for item in response.data:
            yield item

        # Check if there are more pages
        if not response.next_token:
            break

        next_token = response.next_token

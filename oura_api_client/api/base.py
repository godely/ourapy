from typing import Iterator, Callable, TypeVar, Any, Optional, Union
from datetime import date
from ..utils.pagination import stream_paginated_data

T = TypeVar('T')


class BaseRouter:
    def __init__(self, client):
        self.client = client
    
    def _stream_documents(
        self,
        fetch_function: Callable[..., Any],
        start_date: Optional[Union[str, date]] = None,
        end_date: Optional[Union[str, date]] = None,
        **kwargs: Any
    ) -> Iterator[T]:
        """
        Stream all documents from a paginated endpoint.

        Args:
            fetch_function: The endpoint method to call for fetching documents
            start_date: Optional start date for filtering
            end_date: Optional end date for filtering
            **kwargs: Additional parameters to pass to the fetch function

        Yields:
            Individual document items from the API response
        """
        return stream_paginated_data(
            fetch_function,
            start_date=start_date,
            end_date=end_date,
            **kwargs
        )

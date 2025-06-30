"""Heart rate endpoint implementations."""

from typing import Optional, Dict, Any, Union, Iterator
from datetime import date

from .base import BaseRouter
from ..models.heartrate import HeartRateResponse, HeartRateSample


class HeartRateEndpoints(BaseRouter):
    """Heart rate related API endpoints."""

    def get_heartrate(
        self,
        start_date: Optional[Union[str, date]] = None,
        end_date: Optional[Union[str, date]] = None,
        next_token: Optional[str] = None,
        return_model: bool = True,
    ) -> Union[Dict[str, Any], HeartRateResponse]:
        """Get heart rate data for a specified date range.

        Args:
            start_date: Start date in YYYY-MM-DD format or date object
            end_date: End date in YYYY-MM-DD format or date object
            next_token: Token for pagination
            return_model: Whether to return a parsed model or raw dict

        Returns:
            Union[Dict[str, Any], HeartRateResponse]: Heart rate data
        """
        params = {}
        if start_date:
            if isinstance(start_date, date):
                params["start_date"] = start_date.isoformat()
            else:
                params["start_date"] = start_date
        if end_date:
            if isinstance(end_date, date):
                params["end_date"] = end_date.isoformat()
            else:
                params["end_date"] = end_date
        if next_token:
            params["next_token"] = next_token

        response = self.client._make_request(
            "/usercollection/heartrate", params=params
        )

        if return_model:
            return HeartRateResponse.from_dict(response)

        return response

    def stream(
        self,
        start_date: Optional[Union[str, date]] = None,
        end_date: Optional[Union[str, date]] = None,
    ) -> Iterator[HeartRateSample]:
        """
        Stream all Heart Rate data automatically handling pagination.
        
        Args:
            start_date: Start date for the period.
            end_date: End date for the period.
            
        Yields:
            HeartRateSample: Individual heart rate data points.
            
        Example:
            >>> for hr_sample in client.heartrate.stream(start_date="2024-01-01"):
            ...     print(f"Heart rate: {hr_sample.bpm} at {hr_sample.timestamp}")
        """
        return self._stream_documents(
            self.get_heartrate,
            start_date=start_date,
            end_date=end_date
        )

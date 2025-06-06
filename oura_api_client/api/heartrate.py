"""Heart rate endpoint implementations."""

from typing import Optional, Dict, Any, Union

from ..models.heartrate import HeartRateResponse


class HeartRateEndpoints:
    """Heart rate related API endpoints."""

    def __init__(self, client):
        """Initialize with a reference to the main client.

        Args:
            client: The OuraClient instance
        """
        self.client = client

    def get_heartrate(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        return_model: bool = True,
    ) -> Union[Dict[str, Any], HeartRateResponse]:
        """Get heart rate data for a specified date range.

        Args:
            start_date (str, optional): Start date in YYYY-MM-DD format
            end_date (str, optional): End date in YYYY-MM-DD format
            return_model (bool): Whether to return a parsed model or raw dict

        Returns:
            Union[Dict[str, Any], HeartRateResponse]: Heart rate data
        """
        params = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date

        response = self.client._make_request(
            "/usercollection/heartrate", params=params
        )

        if return_model:
            return HeartRateResponse.from_dict(response)

        return response

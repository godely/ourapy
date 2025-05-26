from typing import Optional, Union
from datetime import date
from oura_api_client.api.base import BaseRouter
from oura_api_client.models.sleep_time import SleepTimeResponse, SleepTimeModel

class SleepTime(BaseRouter):
    def get_sleep_time_documents(
        self,
        start_date: Optional[Union[str, date]] = None,
        end_date: Optional[Union[str, date]] = None,
        next_token: Optional[str] = None,
    ) -> SleepTimeResponse:
        """
        Get sleep time documents.

        Args:
            start_date: Start date for the period.
            end_date: End date for the period.
            next_token: Token for pagination.

        Returns:
            SleepTimeResponse: Response containing sleep time data.
        """
        if isinstance(start_date, date):
            start_date = start_date.isoformat()
        if isinstance(end_date, date):
            end_date = end_date.isoformat()
        params = {
            "start_date": start_date if start_date else None,
            "end_date": end_date if end_date else None,
            "next_token": next_token if next_token else None,
        }
        params = {k: v for k, v in params.items() if v is not None}
        response = self.client._make_request("/v2/usercollection/sleep_time", params=params)
        return SleepTimeResponse(**response)

    def get_sleep_time_document(self, document_id: str) -> SleepTimeModel:
        """
        Get a single sleep time document.
        Note: The Oura API documentation for v2 does not explicitly list a
        GET /v2/usercollection/sleep_time/{document_id} endpoint.
        This method is included for completeness based on common API patterns
        but may not be supported by the actual Oura API.

        Args:
            document_id: ID of the document.

        Returns:
            SleepTimeModel: Response containing sleep time data.
        """
        # This endpoint might not be available in Oura API v2 for sleep_time.
        # Proceeding with the assumption it might exist or for future compatibility.
        response = self.client._make_request(f"/v2/usercollection/sleep_time/{document_id}")
        return SleepTimeModel(**response)

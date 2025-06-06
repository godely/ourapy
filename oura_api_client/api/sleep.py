from typing import Optional, Union
from datetime import date  # Keep date for start/end_date
from oura_api_client.api.base import BaseRouter
from oura_api_client.models.sleep import SleepResponse, SleepModel  # Updated model import


class Sleep(BaseRouter):  # Renamed class to Sleep
    def get_sleep_documents(  # Renamed method
        self,
        start_date: Optional[Union[str, date]] = None,  # Changed parameter name for clarity
        end_date: Optional[Union[str, date]] = None,   # Changed parameter name for clarity
        next_token: Optional[str] = None,
    ) -> SleepResponse:  # Updated return type
        """
        Get sleep documents.

        Args:
            start_date: Start date for the period.
            end_date: End date for the period.
            next_token: Token for pagination.

        Returns:
            SleepResponse: Response containing sleep data.
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
        # Corrected endpoint URL from daily_sleep to sleep
        response = self.client._make_request(
            "/v2/usercollection/sleep", params=params
        )
        return SleepResponse(**response)

    def get_sleep_document(self, document_id: str) -> SleepModel:  # Renamed method and updated return type
        """
        Get a single sleep document.

        Args:
            document_id: ID of the document.

        Returns:
            SleepModel: Response containing sleep data.
        """
        # Corrected endpoint URL from daily_sleep to sleep
        response = self.client._make_request(
            f"/v2/usercollection/sleep/{document_id}"
        )
        return SleepModel(**response)

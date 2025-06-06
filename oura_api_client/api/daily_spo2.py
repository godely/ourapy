from typing import Optional, Union
from datetime import date
from oura_api_client.api.base import BaseRouter
from oura_api_client.models.daily_spo2 import DailySpO2Response, DailySpO2Model


class DailySpo2(BaseRouter):  # Renamed class to DailySpo2
    def get_daily_spo2_documents(  # Renamed method
        self,
        start_date: Optional[Union[str, date]] = None,
        end_date: Optional[Union[str, date]] = None,
        next_token: Optional[str] = None,
    ) -> DailySpO2Response:  # Updated return type
        """
        Get daily SpO2 documents.

        Args:
            start_date: Start date for the period.
            end_date: End date for the period.
            next_token: Token for pagination.

        Returns:
            DailySpO2Response: Response containing daily SpO2 data.
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
        response = self.client._make_request("/v2/usercollection/daily_spo2", params=params)
        return DailySpO2Response(**response)

    def get_daily_spo2_document(self, document_id: str) -> DailySpO2Model:  # Renamed method and updated return type
        """
        Get a single daily SpO2 document.

        Args:
            document_id: ID of the document.

        Returns:
            DailySpO2Model: Response containing daily SpO2 data.
        """
        response = self.client._make_request(f"/v2/usercollection/daily_spo2/{document_id}")
        return DailySpO2Model(**response)

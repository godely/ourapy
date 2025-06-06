from typing import Optional, Union
from datetime import date
from oura_api_client.api.base import BaseRouter
from oura_api_client.models.daily_activity import DailyActivityResponse, DailyActivityModel


class DailyActivity(BaseRouter):
    def get_daily_activity_documents(
        self,
        start_date: Optional[Union[str, date]] = None,
        end_date: Optional[Union[str, date]] = None,
        next_token: Optional[str] = None,
    ) -> DailyActivityResponse:
        """
        Get daily activity documents.

        Args:
            start_date: Start date for the period.
            end_date: End date for the period.
            next_token: Token for pagination.

        Returns:
            DailyActivityResponse: Response containing daily activity data.
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
        response = self.client._make_request("/v2/usercollection/daily_activity", params=params)
        return DailyActivityResponse(**response)

    def get_daily_activity_document(self, document_id: str) -> DailyActivityModel:
        """
        Get a single daily activity document.

        Args:
            document_id: ID of the document.

        Returns:
            DailyActivityModel: Response containing daily activity data.
        """
        response = self.client._make_request(f"/v2/usercollection/daily_activity/{document_id}")
        return DailyActivityModel(**response)

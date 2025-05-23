from typing import Optional, Union
from datetime import date
from oura_api_client.api.base import BaseRouter
from oura_api_client.models.daily_readiness import DailyReadinessResponse, DailyReadinessModel

class DailyReadiness(BaseRouter):
    def get_daily_readiness_documents(
        self,
        start_date: Optional[Union[str, date]] = None,
        end_date: Optional[Union[str, date]] = None,
        next_token: Optional[str] = None,
    ) -> DailyReadinessResponse:
        """
        Get daily readiness documents.

        Args:
            start_date: Start date for the period.
            end_date: End date for the period.
            next_token: Token for pagination.

        Returns:
            DailyReadinessResponse: Response containing daily readiness data.
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
        response = self.client._make_request("/v2/usercollection/daily_readiness", params=params)
        return DailyReadinessResponse(**response)

    def get_daily_readiness_document(self, document_id: str) -> DailyReadinessModel:
        """
        Get a single daily readiness document.

        Args:
            document_id: ID of the document.

        Returns:
            DailyReadinessModel: Response containing daily readiness data.
        """
        response = self.client._make_request(f"/v2/usercollection/daily_readiness/{document_id}")
        return DailyReadinessModel(**response)

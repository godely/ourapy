from typing import Optional, Union
from datetime import date
from oura_api_client.api.base import BaseRouter
from oura_api_client.models.daily_stress import (
    DailyStressResponse,
    DailyStressModel
)



class DailyStress(BaseRouter):
    def get_daily_stress_documents(
        self,
        start_date: Optional[Union[str, date]] = None,
        end_date: Optional[Union[str, date]] = None,
        next_token: Optional[str] = None,
    ) -> DailyStressResponse:
        """
        Get daily stress documents.

        Args:
            start_date: Start date for the period.
            end_date: End date for the period.
            next_token: Token for pagination.

        Returns:
            DailyStressResponse: Response containing daily stress data.
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
        response = self.client._make_request(
            "/v2/usercollection/daily_stress", params=params
        )
        return DailyStressResponse(**response)

    def get_daily_stress_document(self, document_id: str) -> DailyStressModel:
        """
        Get a single daily stress document.

        Args:
            document_id: ID of the document.

        Returns:
            DailyStressModel: Response containing daily stress data.
        """
        response = self.client._make_request(
            f"/v2/usercollection/daily_stress/{document_id}"
        )
        return DailyStressModel(**response)

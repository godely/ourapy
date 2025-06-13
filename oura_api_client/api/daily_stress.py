from typing import Optional, Union
from datetime import date
from oura_api_client.api.base import BaseRouter
from oura_api_client.utils import build_query_params
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
        params = build_query_params(start_date, end_date, next_token)
        response = self.client._make_request(
            "/usercollection/daily_stress", params=params
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
            f"/usercollection/daily_stress/{document_id}"
        )
        return DailyStressModel(**response)

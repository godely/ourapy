from typing import Optional, Union
from datetime import date
from oura_api_client.api.base import BaseRouter
from oura_api_client.utils import build_query_params
from oura_api_client.models.daily_resilience import (
    DailyResilienceResponse,
    DailyResilienceModel
)


class DailyResilience(BaseRouter):
    def get_daily_resilience_documents(
        self,
        start_date: Optional[Union[str, date]] = None,
        end_date: Optional[Union[str, date]] = None,
        next_token: Optional[str] = None,
    ) -> DailyResilienceResponse:
        """
        Get daily resilience documents.

        Args:
            start_date: Start date for the period.
            end_date: End date for the period.
            next_token: Token for pagination.

        Returns:
            DailyResilienceResponse: Response containing daily resilience data.
        """
        params = build_query_params(start_date, end_date, next_token)
        response = self.client._make_request(
            "/usercollection/daily_resilience", params=params
        )
        return DailyResilienceResponse(**response)

    def get_daily_resilience_document(
        self, document_id: str
    ) -> DailyResilienceModel:
        """
        Get a single daily resilience document.

        Args:
            document_id: ID of the document.

        Returns:
            DailyResilienceModel: Response containing daily resilience data.
        """
        response = self.client._make_request(
            f"/usercollection/daily_resilience/{document_id}"
        )
        return DailyResilienceModel(**response)

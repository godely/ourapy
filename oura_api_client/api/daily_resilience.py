from typing import Optional, Union
from datetime import date
from oura_api_client.api.base import BaseRouter
from oura_api_client.models.daily_resilience import (
    DailyResilienceResponse,
    DailyResilienceModel
)

<<<<<<< HEAD

=======
>>>>>>> cd7b1320f6e9ecc96b943f9eaa71c4a664f66e3f

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
            "/v2/usercollection/daily_resilience", params=params
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
            f"/v2/usercollection/daily_resilience/{document_id}"
        )
        return DailyResilienceModel(**response)

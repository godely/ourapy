from typing import Optional, Union
from datetime import date
from oura_api_client.api.base import BaseRouter
from oura_api_client.utils import build_query_params
from oura_api_client.models.daily_cardiovascular_age import (
    DailyCardiovascularAgeResponse,
    DailyCardiovascularAgeModel
)


class DailyCardiovascularAge(BaseRouter):
    def get_daily_cardiovascular_age_documents(
        self,
        start_date: Optional[Union[str, date]] = None,
        end_date: Optional[Union[str, date]] = None,
        next_token: Optional[str] = None,
    ) -> DailyCardiovascularAgeResponse:
        """
        Get daily cardiovascular age documents.

        Args:
            start_date: Start date for the period.
            end_date: End date for the period.
            next_token: Token for pagination.

        Returns:
            DailyCardiovascularAgeResponse: Response containing daily
                cardiovascular age data.
        """
        params = build_query_params(start_date, end_date, next_token)
        response = self.client._make_request(
            "/usercollection/daily_cardiovascular_age", params=params
        )
        return DailyCardiovascularAgeResponse(**response)

    def get_daily_cardiovascular_age_document(
        self, document_id: str
    ) -> DailyCardiovascularAgeModel:
        """
        Get a single daily cardiovascular age document.

        Args:
            document_id: ID of the document.

        Returns:
            DailyCardiovascularAgeModel: Response containing daily
                cardiovascular age data.
        """
        response = self.client._make_request(
            f"/usercollection/daily_cardiovascular_age/{document_id}"
        )
        return DailyCardiovascularAgeModel(**response)

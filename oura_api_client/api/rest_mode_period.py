from typing import Optional, Union
from datetime import date
from oura_api_client.api.base import BaseRouter
from oura_api_client.utils import build_query_params
from oura_api_client.models.rest_mode_period import (
    RestModePeriodResponse,
    RestModePeriodModel
)


class RestModePeriod(BaseRouter):
    def get_rest_mode_period_documents(
        self,
        start_date: Optional[Union[str, date]] = None,
        end_date: Optional[Union[str, date]] = None,
        next_token: Optional[str] = None,
    ) -> RestModePeriodResponse:
        """
        Get rest_mode_period documents.

        Args:
            start_date: Start date for the period.
            end_date: End date for the period.
            next_token: Token for pagination.

        Returns:
            RestModePeriodResponse: Response containing rest_mode_period data.
        """
        params = build_query_params(start_date, end_date, next_token)
        response = self.client._make_request(
            "/usercollection/rest_mode_period", params=params
        )
        return RestModePeriodResponse(**response)

    def get_rest_mode_period_document(
        self, document_id: str
    ) -> RestModePeriodModel:
        """
        Get a single rest_mode_period document.

        Args:
            document_id: ID of the document.

        Returns:
            RestModePeriodModel: Response containing rest_mode_period data.
        """
        response = self.client._make_request(
            f"/usercollection/rest_mode_period/{document_id}"
        )
        return RestModePeriodModel(**response)

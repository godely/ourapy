from typing import Optional, Union
from datetime import date
from oura_api_client.api.base import BaseRouter
from oura_api_client.models.rest_mode_period import RestModePeriodResponse, RestModePeriodModel

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
        response = self.client._make_request("/v2/usercollection/rest_mode_period", params=params)
        return RestModePeriodResponse(**response)

    def get_rest_mode_period_document(self, document_id: str) -> RestModePeriodModel:
        """
        Get a single rest_mode_period document.

        Args:
            document_id: ID of the document.

        Returns:
            RestModePeriodModel: Response containing rest_mode_period data.
        """
        response = self.client._make_request(f"/v2/usercollection/rest_mode_period/{document_id}")
        return RestModePeriodModel(**response)

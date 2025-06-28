from typing import Optional, Union
from datetime import date
from oura_api_client.api.base import BaseRouter
from oura_api_client.models.vo2_max import Vo2MaxResponse, Vo2MaxModel
from oura_api_client.utils import build_query_params


class Vo2Max(BaseRouter):
    def get_vo2_max_documents(
        self,
        start_date: Optional[Union[str, date]] = None,
        end_date: Optional[Union[str, date]] = None,
        next_token: Optional[str] = None,
    ) -> Vo2MaxResponse:
        """
        Get VO2 max documents.

        Args:
            start_date: Start date for the period.
            end_date: End date for the period.
            next_token: Token for pagination.

        Returns:
            Vo2MaxResponse: Response containing VO2 max data.
        """
        params = build_query_params(start_date, end_date, next_token)
        response = self.client._make_request("/usercollection/vO2_max", params=params)
        return Vo2MaxResponse(**response)

    def get_vo2_max_document(self, document_id: str) -> Vo2MaxModel:
        """
        Get a single VO2 max document.

        Args:
            document_id: ID of the document.

        Returns:
            Vo2MaxModel: Response containing VO2 max data.
        """
        response = self.client._make_request(f"/usercollection/vO2_max/{document_id}")
        return Vo2MaxModel(**response)

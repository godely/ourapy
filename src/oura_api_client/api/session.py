from typing import Optional, Union
from datetime import date  # Using date for start_date and end_date

# as per other endpoints
from oura_api_client.api.base import BaseRouter
from oura_api_client.models.session import SessionResponse, SessionModel
from oura_api_client.utils import build_query_params


class Session(BaseRouter):
    def get_session_documents(
        self,
        start_date: Optional[Union[str, date]] = None,  # Changed from
        # start_datetime for consistency
        end_date: Optional[Union[str, date]] = None,  # Changed from
        # end_datetime for consistency
        next_token: Optional[str] = None,
    ) -> SessionResponse:
        """
        Get session documents.

        Args:
            start_date: Start date for the period.
            end_date: End date for the period.
            next_token: Token for pagination.

        Returns:
            SessionResponse: Response containing session data.
        """
        params = build_query_params(start_date, end_date, next_token)
        response = self.client._make_request("/usercollection/session", params=params)
        return SessionResponse(**response)

    def get_session_document(self, document_id: str) -> SessionModel:
        """
        Get a single session document.

        Args:
            document_id: ID of the document.

        Returns:
            SessionModel: Response containing session data.
        """
        response = self.client._make_request(f"/usercollection/session/{document_id}")
        return SessionModel(**response)

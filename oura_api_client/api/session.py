from typing import Optional, Union
from datetime import date  # Using date for start_date and end_date as per other endpoints
from oura_api_client.api.base import BaseRouter
from oura_api_client.models.session import SessionResponse, SessionModel


class Session(BaseRouter):
    def get_session_documents(
        self,
        start_date: Optional[Union[str, date]] = None,  # Changed from start_datetime for consistency
        end_date: Optional[Union[str, date]] = None,   # Changed from end_datetime for consistency
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
        response = self.client._make_request("/v2/usercollection/session", params=params)
        return SessionResponse(**response)

    def get_session_document(self, document_id: str) -> SessionModel:
        """
        Get a single session document.

        Args:
            document_id: ID of the document.

        Returns:
            SessionModel: Response containing session data.
        """
        response = self.client._make_request(f"/v2/usercollection/session/{document_id}")
        return SessionModel(**response)

from typing import Optional, Union
from datetime import date # Using date for start_date and end_date
from oura_api_client.api.base import BaseRouter
from oura_api_client.models.tag import TagResponse, TagModel

class Tag(BaseRouter):
    def get_tag_documents(
        self,
        start_date: Optional[Union[str, date]] = None,
        end_date: Optional[Union[str, date]] = None,
        next_token: Optional[str] = None,
    ) -> TagResponse:
        """
        Get tag documents.

        Args:
            start_date: Start date for the period.
            end_date: End date for the period.
            next_token: Token for pagination.

        Returns:
            TagResponse: Response containing tag data.
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
        response = self.client._make_request("/v2/usercollection/tag", params=params)
        return TagResponse(**response)

    def get_tag_document(self, document_id: str) -> TagModel:
        """
        Get a single tag document.

        Args:
            document_id: ID of the document.

        Returns:
            TagModel: Response containing tag data.
        """
        response = self.client._make_request(f"/v2/usercollection/tag/{document_id}")
        return TagModel(**response)

from typing import Optional, Union
from datetime import date  # Using date for start_date and end_date
from oura_api_client.api.base import BaseRouter
from oura_api_client.utils import build_query_params
from oura_api_client.models.enhanced_tag import EnhancedTagResponse, EnhancedTagModel


class EnhancedTag(BaseRouter):
    def get_enhanced_tag_documents(
        self,
        start_date: Optional[Union[str, date]] = None,
        end_date: Optional[Union[str, date]] = None,
        next_token: Optional[str] = None,
    ) -> EnhancedTagResponse:
        """
        Get enhanced_tag documents.

        Args:
            start_date: Start date for the period.
            end_date: End date for the period.
            next_token: Token for pagination.

        Returns:
            EnhancedTagResponse: Response containing enhanced_tag data.
        """
        params = build_query_params(start_date, end_date, next_token)
        response = self.client._make_request(
            "/usercollection/enhanced_tag", params=params
        )
        return EnhancedTagResponse(**response)

    def get_enhanced_tag_document(self, document_id: str) -> EnhancedTagModel:
        """
        Get a single enhanced_tag document.

        Args:
            document_id: ID of the document.

        Returns:
            EnhancedTagModel: Response containing enhanced_tag data.
        """
        response = self.client._make_request(
            f"/usercollection/enhanced_tag/{document_id}"
        )
        return EnhancedTagModel(**response)

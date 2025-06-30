from typing import Optional, Union, Iterator
from datetime import date
from oura_api_client.api.base import BaseRouter
from oura_api_client.utils import build_query_params
from oura_api_client.models.daily_readiness import (
    DailyReadinessResponse,
    DailyReadinessModel
)


class DailyReadiness(BaseRouter):
    def get_daily_readiness_documents(
        self,
        start_date: Optional[Union[str, date]] = None,
        end_date: Optional[Union[str, date]] = None,
        next_token: Optional[str] = None,
    ) -> DailyReadinessResponse:
        """
        Get daily readiness documents.

        Args:
            start_date: Start date for the period.
            end_date: End date for the period.
            next_token: Token for pagination.

        Returns:
            DailyReadinessResponse: Response containing daily readiness data.
        """
        params = build_query_params(start_date, end_date, next_token)
        response = self.client._make_request(
            "/usercollection/daily_readiness", params=params
        )
        return DailyReadinessResponse(**response)

    def get_daily_readiness_document(
        self, document_id: str
    ) -> DailyReadinessModel:
        """
        Get a single daily readiness document.

        Args:
            document_id: ID of the document.

        Returns:
            DailyReadinessModel: Response containing daily readiness data.
        """
        response = self.client._make_request(
            f"/usercollection/daily_readiness/{document_id}"
        )
        return DailyReadinessModel(**response)

    def stream(
        self,
        start_date: Optional[Union[str, date]] = None,
        end_date: Optional[Union[str, date]] = None,
    ) -> Iterator[DailyReadinessModel]:
        """
        Stream all daily readiness documents automatically handling pagination.
        
        Args:
            start_date: Start date for the period.
            end_date: End date for the period.
            
        Yields:
            DailyReadinessModel: Individual daily readiness documents.
            
        Example:
            >>> for readiness in client.daily_readiness.stream(start_date="2024-01-01"):
            ...     print(f"Readiness score: {readiness.score}")
        """
        return self._stream_documents(
            self.get_daily_readiness_documents,
            start_date=start_date,
            end_date=end_date
        )

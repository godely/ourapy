from typing import Optional, Union, Iterator
from datetime import date
from oura_api_client.api.base import BaseRouter
from oura_api_client.models.daily_activity import DailyActivityResponse, DailyActivityModel
from oura_api_client.utils import build_query_params


class DailyActivity(BaseRouter):
    def get_daily_activity_documents(
        self,
        start_date: Optional[Union[str, date]] = None,
        end_date: Optional[Union[str, date]] = None,
        next_token: Optional[str] = None,
    ) -> DailyActivityResponse:
        """
        Get daily activity documents.

        Args:
            start_date: Start date for the period.
            end_date: End date for the period.
            next_token: Token for pagination.

        Returns:
            DailyActivityResponse: Response containing daily activity data.
        """
        params = build_query_params(start_date, end_date, next_token)
        response = self.client._make_request(
            "/usercollection/daily_activity", params=params
        )
        return DailyActivityResponse(**response)

    def get_daily_activity_document(
        self, document_id: str
    ) -> DailyActivityModel:
        """
        Get a single daily activity document.

        Args:
            document_id: ID of the document.

        Returns:
            DailyActivityModel: Response containing daily activity data.
        """
        response = self.client._make_request(
            f"/usercollection/daily_activity/{document_id}"
        )
        return DailyActivityModel(**response)

    def stream(
        self,
        start_date: Optional[Union[str, date]] = None,
        end_date: Optional[Union[str, date]] = None,
    ) -> Iterator[DailyActivityModel]:
        """
        Stream all daily activity documents automatically handling pagination.
        
        Args:
            start_date: Start date for the period.
            end_date: End date for the period.
            
        Yields:
            DailyActivityModel: Individual daily activity documents.
            
        Example:
            >>> for activity in client.daily_activity.stream(start_date="2024-01-01"):
            ...     print(f"Steps: {activity.steps}")
        """
        return self._stream_documents(
            self.get_daily_activity_documents,
            start_date=start_date,
            end_date=end_date
        )

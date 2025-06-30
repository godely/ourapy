from typing import Optional, Union, Iterator
from datetime import date
from oura_api_client.api.base import BaseRouter
from oura_api_client.utils import build_query_params
from oura_api_client.models.daily_sleep import (
    DailySleepResponse,
    DailySleepModel
)


class DailySleep(BaseRouter):
    def get_daily_sleep_documents(
        self,
        start_date: Optional[Union[str, date]] = None,
        end_date: Optional[Union[str, date]] = None,
        next_token: Optional[str] = None,
    ) -> DailySleepResponse:
        """
        Get daily sleep documents.

        Args:
            start_date: Start date for the period.
            end_date: End date for the period.
            next_token: Token for pagination.

        Returns:
            DailySleepResponse: Response containing daily sleep data.
        """
        params = build_query_params(start_date, end_date, next_token)
        response = self.client._make_request(
            "/usercollection/daily_sleep", params=params
        )
        return DailySleepResponse(**response)

    def get_daily_sleep_document(self, document_id: str) -> DailySleepModel:
        """
        Get a single daily sleep document.

        Args:
            document_id: ID of the document.

        Returns:
            DailySleepModel: Response containing daily sleep data.
        """
        response = self.client._make_request(
            f"/usercollection/daily_sleep/{document_id}"
        )
        return DailySleepModel(**response)

    def stream(
        self,
        start_date: Optional[Union[str, date]] = None,
        end_date: Optional[Union[str, date]] = None,
    ) -> Iterator[DailySleepModel]:
        """
        Stream all daily sleep documents automatically handling pagination.
        
        Args:
            start_date: Start date for the period.
            end_date: End date for the period.
            
        Yields:
            DailySleepModel: Individual daily sleep documents.
            
        Example:
            >>> for sleep_record in client.daily_sleep.stream(start_date="2024-01-01"):
            ...     print(f"Sleep score: {sleep_record.score}")
        """
        return self._stream_documents(
            self.get_daily_sleep_documents,
            start_date=start_date,
            end_date=end_date
        )

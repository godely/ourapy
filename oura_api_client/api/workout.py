from typing import Optional, Union
from datetime import date  # Using date for start_date and end_date
from oura_api_client.api.base import BaseRouter
from oura_api_client.models.workout import WorkoutResponse, WorkoutModel


class Workout(BaseRouter):
    def get_workout_documents(
        self,
        start_date: Optional[Union[str, date]] = None,
        end_date: Optional[Union[str, date]] = None,
        next_token: Optional[str] = None,
    ) -> WorkoutResponse:
        """
        Get workout documents.

        Args:
            start_date: Start date for the period.
            end_date: End date for the period.
            next_token: Token for pagination.

        Returns:
            WorkoutResponse: Response containing workout data.
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
        response = self.client._make_request(
            "/v2/usercollection/workout", params=params
        )
        return WorkoutResponse(**response)

    def get_workout_document(self, document_id: str) -> WorkoutModel:
        """
        Get a single workout document.

        Args:
            document_id: ID of the document.

        Returns:
            WorkoutModel: Response containing workout data.
        """
        response = self.client._make_request(
            f"/v2/usercollection/workout/{document_id}"
        )
        return WorkoutModel(**response)

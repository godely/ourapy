from typing import Optional, Union
from datetime import date  # Using date for start_date and end_date
from oura_api_client.api.base import BaseRouter
from oura_api_client.models.workout import WorkoutResponse, WorkoutModel
from oura_api_client.utils import build_query_params


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
        params = build_query_params(start_date, end_date, next_token)
        response = self.client._make_request(
            "/usercollection/workout", params=params
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
            f"/usercollection/workout/{document_id}"
        )
        return WorkoutModel(**response)

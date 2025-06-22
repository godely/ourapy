"""Personal information endpoint implementations."""

from typing import Dict, Any, Union

from ..models.personal import PersonalInfo


class PersonalEndpoints:
    """Personal information related API endpoints."""

    def __init__(self, client):
        """Initialize with a reference to the main client.

        Args:
            client: The OuraClient instance
        """
        self.client = client

    def get_personal_info(
        self, return_model: bool = True
    ) -> Union[Dict[str, Any], PersonalInfo]:
        """Get personal information for the authenticated user.

        Args:
            return_model (bool): Whether to return a parsed model or raw dict

        Returns:
            Union[Dict[str, Any], PersonalInfo]: Personal information
        """
        response = self.client._make_request("/usercollection/personal_info")

        if return_model:
            return PersonalInfo.from_dict(response)

        return response

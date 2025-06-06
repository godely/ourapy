from typing import Optional, Union  # Union is not strictly needed here but kept for consistency
from datetime import date  # date is not used by ring_configuration but kept for consistency
from oura_api_client.api.base import BaseRouter
from oura_api_client.models.ring_configuration import RingConfigurationResponse, RingConfigurationModel


class RingConfiguration(BaseRouter):
    def get_ring_configuration_documents(
        self,
        # Ring Configuration usually doesn't have start/end_date or pagination in typical REST APIs
        # as it often returns a single current configuration or a list of all historical ones.
        # However, if the API supports it (e.g. for historical configurations):
        start_date: Optional[Union[str, date]] = None,  # Kept for potential future use or specific API design
        end_date: Optional[Union[str, date]] = None,  # Kept for potential future use
        next_token: Optional[str] = None,
    ) -> RingConfigurationResponse:
        """
        Get ring configuration documents.
        Note: Oura API v2 documentation for Ring Configuration typically implies a single
        document or a list not filterable by date for general configurations.
        Date parameters are included here for structural consistency if the API were to support it.

        Args:
            start_date: Start date for filtering (if supported by API).
            end_date: End date for filtering (if supported by API).
            next_token: Token for pagination (if supported by API).

        Returns:
            RingConfigurationResponse: Response containing ring configuration data.
        """
        params = {}
        if start_date:
            if isinstance(start_date, date):
                params["start_date"] = start_date.isoformat()
            else:
                params["start_date"] = start_date
        if end_date:
            if isinstance(end_date, date):
                params["end_date"] = end_date.isoformat()
            else:
                params["end_date"] = end_date
        if next_token:
            params["next_token"] = next_token

        # Remove None params manually as empty dict evaluates to False
        final_params = {k: v for k, v in params.items() if v is not None}

        response = self.client._make_request("/v2/usercollection/ring_configuration", params=final_params if final_params else None)
        return RingConfigurationResponse(**response)

    def get_ring_configuration_document(self, document_id: str) -> RingConfigurationModel:
        """
        Get a single ring configuration document.

        Args:
            document_id: ID of the document (specific ring's configuration ID).

        Returns:
            RingConfigurationModel: Response containing ring configuration data.
        """
        response = self.client._make_request(f"/v2/usercollection/ring_configuration/{document_id}")
        return RingConfigurationModel(**response)

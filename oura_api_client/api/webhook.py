from typing import Optional, List
from oura_api_client.api.base import BaseRouter
from oura_api_client.models.webhook import (
    WebhookSubscriptionModel,
    # WebhookListResponse, # Removed as API returns List directly
    WebhookSubscriptionCreateRequest,
    WebhookSubscriptionUpdateRequest,
    WebhookOperation,
    ExtApiV2DataType
)


class Webhook(BaseRouter):
    def _get_webhook_headers(self) -> dict:
        """Helper to construct headers for webhook requests."""
        if (not hasattr(self.client, 'client_id') or
                not hasattr(self.client, 'client_secret') or
                self.client.client_id is None or
                self.client.client_secret is None):
            # This is a fallback or error case. Ideally, the OuraClient
            # should be initialized with client_id and client_secret if
            # webhook management is to be used. For now, we'll raise an error
            # or return base headers, but a production client would need
            # proper handling.
            raise ValueError(
                "client_id and client_secret must be set in OuraClient "
                "for webhook operations."
            )

        # Merge with existing base headers (like Content-Type if needed,
        # or other default headers). For this specific API, it seems only
        # x-client-id and x-client-secret are custom. The base _make_request
        # should handle common headers like Authorization if that was the
        # case, but webhook auth is different.
        headers = {
            "x-client-id": self.client.client_id,
            "x-client-secret": self.client.client_secret,
        }
        # Add other necessary headers like Content-Type for POST/PUT if
        # not handled by _make_request when json_data is present. Typically,
        # requests library does this automatically.
        return headers

    def list_webhook_subscriptions(self) -> List[WebhookSubscriptionModel]:
        """
        List all existing webhook subscriptions.
        API Path: GET /v2/webhook/subscription
        """
        headers = self._get_webhook_headers()
        response_data = self.client._make_request(
            "/webhook/subscription",
            headers=headers
        )
        # API returns a list of subscriptions directly
        return [WebhookSubscriptionModel(**item) for item in response_data]

    def create_webhook_subscription(
        self,
        callback_url: str,
        event_type: WebhookOperation,
        data_type: ExtApiV2DataType,
        verification_token: str,  # Made non-optional as per updated
        # model reflecting spec
    ) -> WebhookSubscriptionModel:
        """
        Create a new webhook subscription.
        API Path: POST /v2/webhook/subscription
        """
        headers = self._get_webhook_headers()
        # Ensure Content-Type is set for POST with JSON body, if not
        # handled by _make_request
        if 'Content-Type' not in headers:
            headers['Content-Type'] = 'application/json'

        request_body = WebhookSubscriptionCreateRequest(
            callback_url=callback_url,
            event_type=event_type,
            data_type=data_type,
            verification_token=verification_token,
        )
        response_data = self.client._make_request(
            "/webhook/subscription",
            method="POST",
            json_data=request_body.model_dump(
                by_alias=True
            ),  # exclude_none=True is default for model_dump
            headers=headers
        )
        return WebhookSubscriptionModel(**response_data)

    def get_webhook_subscription(
        self, subscription_id: str
    ) -> WebhookSubscriptionModel:
        """
        Get details for a specific webhook subscription.
        API Path: GET /v2/webhook/subscription/{subscription_id}
        """
        headers = self._get_webhook_headers()
        response_data = self.client._make_request(
            f"/webhook/subscription/{subscription_id}",
            headers=headers
        )
        return WebhookSubscriptionModel(**response_data)

    def update_webhook_subscription(
        self,
        subscription_id: str,
        verification_token: str,  # Required
        callback_url: Optional[str] = None,
        event_type: Optional[WebhookOperation] = None,
        data_type: Optional[ExtApiV2DataType] = None,
    ) -> WebhookSubscriptionModel:
        """
        Update an existing webhook subscription.
        API Path: PUT /v2/webhook/subscription/{subscription_id}
        """
        headers = self._get_webhook_headers()
        if 'Content-Type' not in headers:
            headers['Content-Type'] = 'application/json'

        request_body = WebhookSubscriptionUpdateRequest(
            verification_token=verification_token,  # Now required
            callback_url=callback_url,
            event_type=event_type,
            data_type=data_type,
        )
        response_data = self.client._make_request(
            f"/webhook/subscription/{subscription_id}",
            method="PUT",
            json_data=request_body.model_dump(
                by_alias=True, exclude_none=True
            ),
            headers=headers
        )
        return WebhookSubscriptionModel(**response_data)

    def delete_webhook_subscription(self, subscription_id: str) -> None:
        """
        Delete a webhook subscription.
        API Path: DELETE /v2/webhook/subscription/{subscription_id}
        """
        headers = self._get_webhook_headers()
        self.client._make_request(
            f"/webhook/subscription/{subscription_id}",
            method="DELETE",
            headers=headers
        )
        return None

    def renew_webhook_subscription(
        self, subscription_id: str
    ) -> WebhookSubscriptionModel:
        """
        Renew an existing webhook subscription.
        API Path: PUT /v2/webhook/subscription/renew/{subscription_id}
        """
        headers = self._get_webhook_headers()
        # Some APIs might require Content-Type even for PUTs without a
        # body, but typically not. If it's needed, _make_request or
        # requests lib handles it, or it can be added here.
        # if 'Content-Type' not in headers:
        #      headers['Content-Type'] = 'application/json'

        response_data = self.client._make_request(
            f"/webhook/subscription/renew/{subscription_id}",
            method="PUT",
            headers=headers
            # No json_data for this specific renew endpoint as per typical
            # renew patterns, unless the spec implies a body, which it does
            # not for this path.
        )
        return WebhookSubscriptionModel(**response_data)

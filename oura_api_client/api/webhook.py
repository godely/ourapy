from typing import Optional, List # Added List
from oura_api_client.api.base import BaseRouter
from oura_api_client.models.webhook import (
    WebhookSubscriptionModel,
    WebhookListResponse,
    WebhookSubscriptionCreateRequest,
    WebhookSubscriptionUpdateRequest
)

class Webhook(BaseRouter):
    def list_webhook_subscriptions(self) -> WebhookListResponse:
        """
        List all existing webhook subscriptions.
        Note: Oura API v2 for webhooks does not use pagination (next_token).

        Returns:
            WebhookListResponse: Response containing a list of webhook subscriptions.
        """
        response = self.client._make_request("/v2/usercollection/webhook")
        return WebhookListResponse(**response)

    def create_webhook_subscription(
        self,
        callback_url: str,
        event_types: List[str],
        verification_token: Optional[str] = None,
    ) -> WebhookSubscriptionModel:
        """
        Create a new webhook subscription.

        Args:
            callback_url: The URL where webhook notifications will be sent.
            event_types: A list of event types to subscribe to.
            verification_token: An optional token to verify the callback URL.

        Returns:
            WebhookSubscriptionModel: The created webhook subscription details.
        """
        request_body = WebhookSubscriptionCreateRequest(
            callback_url=callback_url,
            event_types=event_types,
            verification_token=verification_token,
        )
        # Pydantic's model_dump(by_alias=True) ensures correct field names are used in the JSON
        response = self.client._make_request(
            "/v2/usercollection/webhook",
            method="POST",
            json_data=request_body.model_dump(by_alias=True, exclude_none=True)
        )
        return WebhookSubscriptionModel(**response)

    def get_webhook_subscription(self, subscription_id: str) -> WebhookSubscriptionModel:
        """
        Get details for a specific webhook subscription.

        Args:
            subscription_id: The ID of the webhook subscription.

        Returns:
            WebhookSubscriptionModel: Details of the webhook subscription.
        """
        response = self.client._make_request(f"/v2/usercollection/webhook/{subscription_id}")
        return WebhookSubscriptionModel(**response)

    def update_webhook_subscription(
        self,
        subscription_id: str,
        callback_url: Optional[str] = None,
        event_types: Optional[List[str]] = None,
        verification_token: Optional[str] = None,
    ) -> WebhookSubscriptionModel:
        """
        Update an existing webhook subscription.

        Args:
            subscription_id: The ID of the webhook subscription to update.
            callback_url: The new callback URL.
            event_types: The new list of event types.
            verification_token: The new verification token.

        Returns:
            WebhookSubscriptionModel: The updated webhook subscription details.
        """
        request_body = WebhookSubscriptionUpdateRequest(
            callback_url=callback_url,
            event_types=event_types,
            verification_token=verification_token,
        )
        # Pydantic's model_dump(by_alias=True, exclude_none=True) ensures correct field names and omits unset optionals
        response = self.client._make_request(
            f"/v2/usercollection/webhook/{subscription_id}",
            method="PUT",
            json_data=request_body.model_dump(by_alias=True, exclude_none=True)
        )
        return WebhookSubscriptionModel(**response)

    def delete_webhook_subscription(self, subscription_id: str) -> None:
        """
        Delete a webhook subscription.

        Args:
            subscription_id: The ID of the webhook subscription to delete.

        Returns:
            None. The API returns a 204 No Content on success.
        """
        self.client._make_request(
            f"/v2/usercollection/webhook/{subscription_id}",
            method="DELETE"
        )
        return None

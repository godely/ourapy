from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class WebhookEventModel(BaseModel): # New model for events within a subscription
    event_type: str = Field(alias="event_type") # e.g., "oura_webhook_test.test_event" or specific data types
    # Additional fields for an event could be 'timestamp', 'user_id', 'data_id' if provided by API
    # For now, keeping it simple as per typical webhook event structures.

class WebhookSubscriptionModel(BaseModel):
    id: str # Webhook subscription ID
    created_at: datetime = Field(alias="created_at")
    updated_at: datetime = Field(None, alias="updated_at") # Optional, as it might not be updated
    verification_token: Optional[str] = Field(None, alias="verification_token") # Only present on creation/update
    callback_url: str = Field(alias="callback_url")
    subscribed_events: Optional[List[WebhookEventModel]] = Field(None, alias="subscribed_events")
    # The OpenAPI spec indicates 'event_types' as a list of strings for creation,
    # but a successful response for GET might detail them as objects or just list strings.
    # Using WebhookEventModel for subscribed_events if the API returns more detail than just strings.
    # If it's just strings, this would be:
    # subscribed_events: Optional[List[str]] = Field(None, alias="subscribed_events")
    # For now, assuming a list of simple event type strings as per common webhook patterns for listing subscriptions.
    # Re-adjusting based on typical GET response: usually lists event type strings.
    event_types: Optional[List[str]] = Field(None, alias="event_types")


class WebhookSubscriptionCreateRequest(BaseModel): # For POST request body
    callback_url: str = Field(alias="callback_url")
    verification_token: Optional[str] = Field(None, alias="verification_token")
    event_types: List[str] = Field(alias="event_types")

class WebhookSubscriptionUpdateRequest(BaseModel): # For PUT request body
    callback_url: Optional[str] = Field(None, alias="callback_url")
    verification_token: Optional[str] = Field(None, alias="verification_token")
    event_types: Optional[List[str]] = Field(None, alias="event_types")

# Response for listing multiple webhooks
class WebhookListResponse(BaseModel):
    data: List[WebhookSubscriptionModel]
    # Oura's list webhooks endpoint does not use next_token based on v2 spec
    # next_token: Optional[str] = None

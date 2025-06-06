from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum


class WebhookEventModel(BaseModel):  # New model for events within a subscription
    event_type: str = Field(alias="event_type")  # e.g., "oura_webhook_test.test_event" or specific data types
    # Additional fields for an event could be 'timestamp', 'user_id', 'data_id' if provided by API
    # For now, keeping it simple as per typical webhook event structures.


class WebhookSubscriptionModel(BaseModel):
    id: str  # Webhook subscription ID
    created_at: datetime = Field(alias="created_at")
    updated_at: datetime = Field(alias="updated_at")  # Optional, as it might not be updated
    verification_token: Optional[str] = Field(alias="verification_token")  # Only present on creation/update
    callback_url: str = Field(alias="callback_url")
    subscribed_events: Optional[List[WebhookEventModel]] = Field(alias="subscribed_events")
    # The OpenAPI spec indicates 'event_types' as a list of strings for creation,
    # but a successful response for GET might detail them as objects or just list strings.
    # Using WebhookEventModel for subscribed_events if the API returns more detail than just strings.
    # If it's just strings, this would be:
    # subscribed_events: Optional[List[str]] = Field(alias="subscribed_events")
    # For now, assuming a list of simple event type strings as per common webhook patterns for listing subscriptions.
    # Re-adjusting based on typical GET response: usually lists event type strings.
    event_types: Optional[List[str]] = Field(alias="event_types")


class WebhookOperation(str, Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"


class ExtApiV2DataType(str, Enum):
    TAG = "tag"
    ENHANCED_TAG = "enhanced_tag"
    WORKOUT = "workout"
    SESSION = "session"
    SLEEP = "sleep"
    DAILY_SLEEP = "daily_sleep"
    DAILY_READINESS = "daily_readiness"
    DAILY_ACTIVITY = "daily_activity"
    DAILY_SPO2 = "daily_spo2"
    SLEEP_TIME = "sleep_time"
    REST_MODE_PERIOD = "rest_mode_period"
    RING_CONFIGURATION = "ring_configuration"
    DAILY_STRESS = "daily_stress"
    DAILY_CARDIOVASCULAR_AGE = "daily_cardiovascular_age"
    DAILY_RESILIENCE = "daily_resilience"
    VO2_MAX = "vo2_max"
    # Note: The OpenAPI spec does not list "heartrate" under ExtApiV2DataType for webhooks,
    # but it is a general data type. If webhooks support it, it should be added.
    # For now, sticking to the types explicitly listed under Webhook components.


class WebhookSubscriptionModel(BaseModel):
    id: str = Field(..., description="Webhook subscription ID")
    callback_url: str = Field(..., alias="callback_url")
    event_type: WebhookOperation = Field(..., alias="event_type")
    data_type: ExtApiV2DataType = Field(..., alias="data_type")
    # Assuming created_at and updated_at are not part of the GET response based on spec example for WebhookSubscriptionModel
    # If they are, they should be added back. The spec for WebhookSubscriptionModel shows:
    # id, callback_url, event_type, data_type, expiration_time
    expiration_time: datetime = Field(..., alias="expiration_time")
    # verification_token is not part of the response for GET /subscription or GET /subscription/{id}


class WebhookSubscriptionCreateRequest(BaseModel): # For POST request body
    callback_url: str = Field(..., alias="callback_url")
    verification_token: str = Field(..., alias="verification_token") # Made required as per spec
    event_type: WebhookOperation = Field(..., alias="event_type")
    data_type: ExtApiV2DataType = Field(..., alias="data_type")


class WebhookSubscriptionUpdateRequest(BaseModel): # For PUT request body
    verification_token: str = Field(..., alias="verification_token") # Required
    callback_url: Optional[str] = Field(None, alias="callback_url")
    event_type: Optional[WebhookOperation] = Field(None, alias="event_type")
    data_type: Optional[ExtApiV2DataType] = Field(None, alias="data_type")

# No longer using WebhookListResponse as the API returns a direct list.
# class WebhookListResponse(BaseModel):
#     data: List[WebhookSubscriptionModel]

# Model for the renew response (same as WebhookSubscriptionModel)
WebhookRenewResponse = WebhookSubscriptionModel

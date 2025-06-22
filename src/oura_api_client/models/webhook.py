from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


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


class WebhookSubscriptionCreateRequest(BaseModel):  # For POST request body
    callback_url: str = Field(..., alias="callback_url")
    verification_token: str = Field(
        ..., alias="verification_token"
    )  # Made required as per spec
    event_type: WebhookOperation = Field(..., alias="event_type")
    data_type: ExtApiV2DataType = Field(..., alias="data_type")


class WebhookSubscriptionUpdateRequest(BaseModel):  # For PUT request body
    verification_token: str = Field(..., alias="verification_token")  # Required
    callback_url: Optional[str] = Field(None, alias="callback_url")
    event_type: Optional[WebhookOperation] = Field(None, alias="event_type")
    data_type: Optional[ExtApiV2DataType] = Field(None, alias="data_type")


# No longer using WebhookListResponse as the API returns a direct list.
# class WebhookListResponse(BaseModel):
#     data: List[WebhookSubscriptionModel]

# Model for the renew response (same as WebhookSubscriptionModel)
WebhookRenewResponse = WebhookSubscriptionModel

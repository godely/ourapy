from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, date

# MomentType and MomentMood are enums, but Pydantic uses Literal for this
from typing import Literal


class SessionModel(BaseModel):
    id: str
    day: date  # Added day based on common patterns in other models
    start_datetime: datetime = Field(alias="start_datetime")
    end_datetime: datetime = Field(alias="end_datetime")
    type: Literal[
        "breathing_exercise",
        "meditation",
        "nap",
        "note",
        "oura_guided_meditation",
        "relaxation",
        "rest",
        "session_other",  # New type
        "sleep_sound",  # New type
        "timer",  # New type
        "workout"
    ]
    # Optional fields based on typical session data
    mood: Optional[Literal[
        "bad",
        "good",
        "great",
        "okay",
        "poor",
        "sensory_other",  # New mood
        "stressful",
        "thankful",
        "tired",
        "undefined"
    ]] = None
    heart_rate: Optional[str] = Field(None, alias="heart_rate")  # Assuming string, adjust if complex
    heart_rate_variability: Optional[str] = Field(None, alias="heart_rate_variability")  # Assuming string
    motion_count: Optional[int] = Field(None, alias="motion_count")
    # New fields from OpenAPI spec for Session
    breathing_rate: Optional[float] = Field(None, alias="breathing_rate")
    duration: Optional[int] = Field(None, alias="duration")
    energy: Optional[float] = Field(None, alias="energy")
    hrv_data: Optional[str] = Field(None, alias="hrv_data")  # Assuming string
    label: Optional[str] = Field(None, alias="label")
    readiness_score_delta: Optional[int] = Field(

        None, alias="readiness_score_delta"

    )
    skin_temperature: Optional[float] = Field(None, alias="skin_temperature")
    sleep_score_delta: Optional[int] = Field(None, alias="sleep_score_delta")
    stress: Optional[float] = Field(None, alias="stress")


class SessionResponse(BaseModel):
    data: List[SessionModel]
    next_token: Optional[str] = None

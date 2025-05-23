from pydantic import BaseModel, Field
from typing import List, Optional # Added List
from datetime import date, datetime

class ReadinessContributors(BaseModel):
    activity_balance: Optional[int] = Field(None, alias="activity_balance")
    body_temperature: Optional[int] = Field(None, alias="body_temperature")
    hrv_balance: Optional[int] = Field(None, alias="hrv_balance")
    previous_day_activity: Optional[int] = Field(None, alias="previous_day_activity")
    previous_night: Optional[int] = Field(None, alias="previous_night")
    recovery_index: Optional[int] = Field(None, alias="recovery_index")
    resting_heart_rate: Optional[int] = Field(None, alias="resting_heart_rate")
    sleep_balance: Optional[int] = Field(None, alias="sleep_balance")

class DailyReadinessModel(BaseModel):
    id: str
    contributors: ReadinessContributors
    day: date
    score: Optional[int] = Field(None, alias="score")
    temperature_deviation: Optional[float] = Field(None, alias="temperature_deviation") # Deprecated
    temperature_trend_deviation: Optional[float] = Field(None, alias="temperature_trend_deviation")
    timestamp: datetime
    # New fields from OpenAPI spec not in original snippet
    activity_class_5_min: Optional[str] = Field(None, alias="activity_class_5_min") # New
    hrv_balance_data: Optional[str] = Field(None, alias="hrv_balance_data") # New, assuming string, adjust if different type
    spo2_percentage: Optional[float] = Field(None, alias="spo2_percentage") # New
    # Fields from original DailyActivity/Sleep that might be relevant or were missed in initial Readiness scope
    # Assuming these are not part of readiness based on typical Oura data separation,
    # but including as comments if they need to be reviewed from a more comprehensive spec
    # sleep_average: Optional[int] = Field(None, alias="sleep_average") # Example if there was a sleep_average field
    # readiness_score_delta: Optional[int] = Field(None, alias="readiness_score_delta") # This was in sleep, likely not here

class DailyReadinessResponse(BaseModel):
    data: List[DailyReadinessModel]
    next_token: Optional[str] = None

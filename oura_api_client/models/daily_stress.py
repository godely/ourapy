from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date, datetime


class DailyStressModel(BaseModel):
    id: str
    day: date
    stress_high: Optional[int] = Field(
        None, alias="stress_high"
    )  # Duration of high stress in seconds
    stress_low: Optional[int] = Field(
        None, alias="stress_low"
    )   # Duration of low stress in seconds
    stress_medium: Optional[int] = Field(
        None, alias="stress_medium"
    )  # Duration of medium stress in seconds
    timestamp: datetime  # Timestamp of the summary
    # Based on OpenAPI spec, additional fields:
    recovery_high: Optional[int] = Field(
        None, alias="recovery_high"
    )  # Duration of high recovery in seconds
    recovery_low: Optional[int] = Field(
        None, alias="recovery_low"
    )   # Duration of low recovery in seconds
    recovery_medium: Optional[int] = Field(
        None, alias="recovery_medium"
    )  # Duration of medium recovery in seconds
    day_summary: Optional[str] = Field(
        None, alias="day_summary"
    )  # Summary of the day's stress


class DailyStressResponse(BaseModel):
    data: List[DailyStressModel]
    next_token: Optional[str] = None

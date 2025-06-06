from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date, datetime


class DailyStressModel(BaseModel):
    id: str
    day: date
    stress_high: Optional[int] = Field(None, alias="stress_high")  # Duration of high stress in seconds
    stress_score: Optional[int] = None  # Stress score
    stress_medium: Optional[int] = Field(None, alias="stress_medium")  # Duration of medium stress in seconds
    timestamp: datetime  # Timestamp of the summary
    # Based on OpenAPI spec, additional fields might include:
    # recovery_high: Optional[int] = Field(None, alias="recovery_high")  # Duration of high recovery in seconds
    # recovery_low: Optional[int] = Field(None, alias="recovery_low")   # Duration of low recovery in seconds
    # recovery_medium: Optional[int] = Field(None, alias="recovery_medium")  # Duration of medium recovery in seconds
    # daytime_stress_score: Optional[int] = Field(None, alias="daytime_stress_score")  # Overall stress score
    # daytime_stress_score: Optional[int] = Field(None, alias="daytime_stress_score")  # Overall stress score
    # Deprecated fields like `rest_mode_state` are not included unless specified as current.


class DailyStressResponse(BaseModel):
    data: List[DailyStressModel]
    next_token: Optional[str] = None

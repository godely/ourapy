from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date, datetime


class DailyCardiovascularAgeModel(BaseModel):
    id: str
    day: date
    # Based on typical cardiovascular age report from Oura:
    cardiovascular_age: Optional[int] = None  # Age in years
    age_difference: Optional[int] = None  # Difference from chronological age
    age_upper_bound: Optional[float] = Field(None, alias="age_upper_bound")  # Upper bound of the estimated age range
    # Other potential fields, depending on API detail:
    # arterial_stiffness_index: Optional[float] = Field(None, alias="arterial_stiffness_index")
    confidence: Optional[float] = None  # Confidence score
    # pulse_wave_velocity: Optional[float] = Field(None, alias="pulse_wave_velocity")
    timestamp: datetime  # Timestamp of the summary


class DailyCardiovascularAgeResponse(BaseModel):
    data: List[DailyCardiovascularAgeModel]
    source: Optional[str] = None  # Data source

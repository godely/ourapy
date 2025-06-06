from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date, datetime


class DailyCardiovascularAgeModel(BaseModel):
    id: str
    day: date
    # Based on typical cardiovascular age report from Oura:
<<<<<<< HEAD
    cardiovascular_age: Optional[int] = None  # Age in years
    age_difference: Optional[int] = None  # Difference from chronological age
    age_upper_bound: Optional[float] = Field(None, alias="age_upper_bound")  # Upper bound of the estimated age range
    # Other potential fields, depending on API detail:
    # arterial_stiffness_index: Optional[float] = Field(None, alias="arterial_stiffness_index")
    confidence: Optional[float] = None  # Confidence score
    # pulse_wave_velocity: Optional[float] = Field(None, alias="pulse_wave_velocity")
=======
    cardiovascular_age: Optional[float] = Field(
        None, alias="cardiovascular_age"
    )  # The user's estimated cardiovascular age
    age_lower_bound: Optional[float] = Field(
        None, alias="age_lower_bound"
    )  # Lower bound of the estimated age range
    age_upper_bound: Optional[float] = Field(
        None, alias="age_upper_bound"
    )  # Upper bound of the estimated age range
    # Other potential fields, depending on API detail:
    # arterial_stiffness_index: Optional[float] = Field(
    #     None, alias="arterial_stiffness_index"
    # )
    # pulse_wave_velocity: Optional[float] = Field(
    #     None, alias="pulse_wave_velocity"
    # )
>>>>>>> cd7b1320f6e9ecc96b943f9eaa71c4a664f66e3f
    timestamp: datetime  # Timestamp of the summary


class DailyCardiovascularAgeResponse(BaseModel):
    data: List[DailyCardiovascularAgeModel]
    source: Optional[str] = None  # Data source

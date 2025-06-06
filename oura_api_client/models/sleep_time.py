from pydantic import BaseModel, Field
from typing import List, Optional
<<<<<<< HEAD
from datetime import date, datetime
=======
from datetime import date, datetime  # Added datetime
>>>>>>> cd7b1320f6e9ecc96b943f9eaa71c4a664f66e3f

# Enum-like fields will be handled with Literal as per previous patterns if needed,
# but based on the provided snippet, direct enum models are not explicitly requested here.


class SleepTimeWindow(BaseModel):
<<<<<<< HEAD
    day_light_saving_time: Optional[int] = Field(None, alias="day_light_saving_time")  # New
    end_offset: Optional[int] = Field(None, alias="end_offset")  # Offset from midnight in seconds
    start_offset: Optional[int] = Field(None, alias="start_offset")  # Offset from midnight in seconds
=======
    day_light_saving_time: Optional[int] = Field(
     None, alias="day_light_saving_time"
 )  # New
    end_offset: Optional[int] = Field(

        None, alias="end_offset"

    )  # Offset from midnight in seconds
    start_offset: Optional[int] = Field(

        None, alias="start_offset"

    )  # Offset from midnight in seconds
>>>>>>> cd7b1320f6e9ecc96b943f9eaa71c4a664f66e3f


class SleepTimeRecommendation(BaseModel):
    # Based on common sleep recommendation data, specific fields might vary
    # For now, keeping it simple. If a detailed spec is available, adjust.
    recommendation: Optional[str] = None  # e.g., "go_to_bed_earlier", "maintain_consistent_schedule"
    # Could also include specific time recommendations if the API provides them:
    # recommended_bedtime_start: Optional[datetime] = None
    # recommended_bedtime_end: Optional[datetime] = None


class SleepTimeStatus(BaseModel):
    # Based on common sleep status data, specific fields might vary
    status: Optional[str] = None  # e.g., "optimal", "slightly_early", "late"
    # Could also include deviation from ideal if provided:
    # deviation_minutes: Optional[int] = None


class SleepTimeModel(BaseModel):
    id: str  # Though API doc says no ID, a unique identifier per record is standard
    day: date
<<<<<<< HEAD
    optimal_bedtime: Optional[SleepTimeWindow] = Field(None, alias="optimal_bedtime")
    recommendation: Optional[SleepTimeRecommendation] = Field(None, alias="recommendation")  # Using the new model
    status: Optional[SleepTimeStatus] = Field(None, alias="status")  # Using the new model
    # Assuming timestamp might be relevant for when the record was created or last updated
    timestamp: Optional[datetime] = Field(None, alias="timestamp")  # Added timestamp
=======
    optimal_bedtime: Optional[SleepTimeWindow] = Field(
     None, alias="optimal_bedtime"
 )
    recommendation: Optional[SleepTimeRecommendation] = Field(

        None, alias="recommendation"

    )  # Using the new model
    status: Optional[SleepTimeStatus] = Field(

        None, alias="status"

    )  # Using the new model
    # Assuming timestamp might be relevant for when the record was created or last updated
    timestamp: Optional[datetime] = Field(

        None, alias="timestamp"

    )  # Added timestamp
>>>>>>> cd7b1320f6e9ecc96b943f9eaa71c4a664f66e3f


class SleepTimeResponse(BaseModel):
    data: List[SleepTimeModel]
    next_token: Optional[str] = None

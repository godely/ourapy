from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date, datetime


class Vo2MaxModel(BaseModel):
    id: str
    day: date
    vo2_max: Optional[float] = Field(
        None, alias="vo2_max"
    )  # User's estimated VO2 max in mL/kg/min
    # Based on typical VO2 max reports, additional context might be provided:
    # fitness_level: Optional[str] = Field(
    #     None, alias="fitness_level"
    # )  # e.g., "excellent", "good", "fair"
    # source: Optional[str] = Field(
    #     None, alias="source"
    # )  # e.g., "estimated_from_workout", "manual_entry"
    timestamp: datetime  # Timestamp of the summary


class Vo2MaxResponse(BaseModel):
    data: List[Vo2MaxModel]
    next_token: Optional[str] = None

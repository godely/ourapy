from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date, datetime


class DailyCardiovascularAgeModel(BaseModel):
    id: str
    day: date
    # Based on OpenAPI spec:
    vascular_age: Optional[float] = Field(
        None, alias="vascular_age"
    )  # The user's estimated vascular age
    cardiovascular_age: Optional[float] = Field(
        None, alias="cardiovascular_age"
    )  # The user's estimated cardiovascular age
    age_lower_bound: Optional[float] = Field(
        None, alias="age_lower_bound"
    )  # Lower bound of the estimated age range
    age_upper_bound: Optional[float] = Field(
        None, alias="age_upper_bound"
    )  # Upper bound of the estimated age range
    timestamp: datetime  # Timestamp of the summary


class DailyCardiovascularAgeResponse(BaseModel):
    data: List[DailyCardiovascularAgeModel]
    next_token: Optional[str] = None  # Pagination token
    source: Optional[str] = None  # Data source

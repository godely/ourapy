from pydantic import BaseModel, Field
from typing import List, Optional

from datetime import date, datetime


class ResilienceContributors(BaseModel):
    sleep_recovery: Optional[float] = Field(None, alias="sleep_recovery")
    daytime_recovery: Optional[float] = Field(None, alias="daytime_recovery")
    stress: Optional[float] = Field(None, alias="stress")


class DailyResilienceModel(BaseModel):
    id: str
    day: date
    resilience_score: Optional[float] = Field(
        None, alias="resilience_score"
    )  # Overall resilience score
    contributors: Optional[ResilienceContributors] = Field(
        None, alias="contributors"
    )  # Resilience contributors
    level: Optional[str] = Field(None, alias="level")  # Resilience level
    timestamp: datetime  # Timestamp of the summary


class DailyResilienceResponse(BaseModel):
    data: List[DailyResilienceModel]
    next_token: Optional[str] = None

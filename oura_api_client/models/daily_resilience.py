from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date, datetime

class DailyResilienceModel(BaseModel):
    id: str
    day: date
    resilience_score: Optional[float] = Field(None, alias="resilience_score") # Overall resilience score
    # Based on typical resilience metrics, fields could include:
    # stress_regulation: Optional[float] = Field(None, alias="stress_regulation")
    # recovery_patterns: Optional[float] = Field(None, alias="recovery_patterns")
    # emotional_balance: Optional[float] = Field(None, alias="emotional_balance")
    # These are examples; actual fields depend on the Oura API's definition of resilience.
    # For now, focusing on a core `resilience_score`.
    timestamp: datetime # Timestamp of the summary

class DailyResilienceResponse(BaseModel):
    data: List[DailyResilienceModel]
    next_token: Optional[str] = None

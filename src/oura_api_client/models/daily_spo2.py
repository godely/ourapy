from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date, datetime  # Added datetime


class DailySpO2AggregatedValuesModel(
    BaseModel
):  # Renamed from Spo2Readings to DailySpO2AggregatedValuesModel for clarity
    average: Optional[float] = Field(None, alias="average")  # Percentage


class DailySpO2Model(BaseModel):
    id: str
    day: date
    spo2_percentage: Optional[float] = Field(
        None, alias="spo2_percentage"
    )  # Overall percentage for the day, if available
    # The above field seems redundant if aggregated_values.average is the main source
    # Kept for now as per some interpretations of daily summary vs. detailed readings
    aggregated_values: Optional[DailySpO2AggregatedValuesModel] = Field(
        None, alias="aggregated_values"
    )  # New nested model for clarity
    # Assuming timestamp might be relevant for when the daily record was created or last updated
    timestamp: Optional[datetime] = Field(None, alias="timestamp")  # Added timestamp


class DailySpO2Response(BaseModel):
    data: List[DailySpO2Model]
    next_token: Optional[str] = None

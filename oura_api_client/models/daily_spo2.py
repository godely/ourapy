from pydantic import BaseModel, Field
from typing import List, Optional
<<<<<<< HEAD
from datetime import date, datetime


class DailySpO2AggregatedValuesModel(BaseModel):  # Renamed from Spo2Readings to DailySpO2AggregatedValuesModel for clarity
    average: Optional[float] = Field(None, alias="average")  # Percentage
=======
from datetime import date, datetime  # Added datetime


class DailySpO2AggregatedValuesModel(BaseModel):  # Renamed from Spo2Readings to DailySpO2AggregatedValuesModel for clarity
    average: Optional[float] = Field(
     None, alias="average"
 )  # Percentage
>>>>>>> cd7b1320f6e9ecc96b943f9eaa71c4a664f66e3f


class DailySpO2Model(BaseModel):
    id: str
    day: date
<<<<<<< HEAD
    spo2_percentage: Optional[float] = None  # Overall percentage for the day, if available
    # The above field seems redundant if aggregated_values.average is the main source
    # Kept for now as per some interpretations of daily summary vs. detailed readings
    aggregated_values: Optional[DailySpO2AggregatedValuesModel] = Field(None, alias="aggregated_values")  # New nested model for clarity
    # Assuming timestamp might be relevant for when the daily record was created or last updated
    timestamp: Optional[datetime] = Field(None, alias="timestamp")  # Added timestamp
=======
    spo2_percentage: Optional[float] = Field(



    None, alias="spo2_percentage"



)  # Overall percentage for the day, if available
    # The above field seems redundant if aggregated_values.average is the main source
    # Kept for now as per some interpretations of daily summary vs. detailed readings
    aggregated_values: Optional[DailySpO2AggregatedValuesModel] = Field(

        None, alias="aggregated_values"

    )  # New nested model for clarity
    # Assuming timestamp might be relevant for when the daily record was created or last updated
    timestamp: Optional[datetime] = Field(

        None, alias="timestamp"

    )  # Added timestamp
>>>>>>> cd7b1320f6e9ecc96b943f9eaa71c4a664f66e3f


class DailySpO2Response(BaseModel):
    data: List[DailySpO2Model]
    next_token: Optional[str] = None

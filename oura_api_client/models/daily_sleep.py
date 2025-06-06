from pydantic import BaseModel, Field
from typing import List, Optional

from datetime import date, datetime


<<<<<<< HEAD
class SleepContributors(BaseModel):
    deep_sleep: Optional[int] = Field(None, alias="deep_sleep")  # deep sleep in minutes
=======

class SleepContributors(BaseModel):
    deep_sleep: Optional[int] = Field(
     None, alias="deep_sleep"
 )
>>>>>>> cd7b1320f6e9ecc96b943f9eaa71c4a664f66e3f
    efficiency: Optional[int] = Field(None, alias="efficiency")
    latency: Optional[int] = Field(None, alias="latency")
    rem_sleep: Optional[int] = Field(None, alias="rem_sleep")  # REM sleep in minutes
    restfulness: Optional[int] = Field(None, alias="restfulness")
    timing: Optional[int] = Field(None, alias="timing")
    total_sleep: Optional[int] = Field(None, alias="total_sleep")  # Total sleep in minutes






class DailySleepModel(BaseModel):
    id: str
    contributors: SleepContributors
    day: date
    timestamp: datetime
    score: Optional[int] = Field(




    None, alias="score"




)
    bedtime_end: Optional[datetime] = Field(None, alias="bedtime_end")
    bedtime_start: Optional[datetime] = Field(None, alias="bedtime_start")
    breath_average: Optional[float] = Field(None, alias="breath_average")
    deep_sleep_duration: Optional[int] = Field(

        None, alias="deep_sleep_duration"

    )
    efficiency: Optional[int] = Field(None, alias="efficiency")
    heart_rate_average: Optional[float] = Field(

        None, alias="heart_rate_average"

    )
    heart_rate_lowest: Optional[float] = Field(

        None, alias="heart_rate_lowest"

    )
    hypnogram_5_min: Optional[str] = Field(None, alias="hypnogram_5_min")
    latency: Optional[int] = Field(None, alias="latency")
    light_sleep_duration: Optional[int] = Field(

        None, alias="light_sleep_duration"

    )
    low_battery_alert: Optional[bool] = Field(None, alias="low_battery_alert")
    readiness_score_delta: Optional[int] = Field(

        None, alias="readiness_score_delta"

    )
    rem_sleep_duration: Optional[int] = Field(

        None, alias="rem_sleep_duration"

    )
    restless_periods: Optional[int] = Field(None, alias="restless_periods")
<<<<<<< HEAD
    sleep_phase_5_min: Optional[str] = Field(None, alias="sleep_phase_5_min")  # Deprecated
    time_in_bed: Optional[int] = Field(None, alias="time_in_bed")
    total_sleep_duration: Optional[int] = Field(None, alias="total_sleep_duration")
    type: Optional[str] = Field(None, alias="type")  # Enum: "deleted", "long_sleep", "main_sleep", "nap", "rest"
    average_hrv: Optional[float] = Field(None, alias="average_hrv")
    awake_time: Optional[int] = Field(None, alias="awake_time")
    hr_60_second_average: Optional[List[int]] = Field(None, alias="hr_60_second_average")  # New in v2.10
    hrv_4_hour_average: Optional[List[float]] = Field(None, alias="hrv_4_hour_average")  # New in v2.10
    readiness: Optional[str] = Field(None, alias="readiness")  # New in v2.10, but type not specified, assuming string for now
    temperature_delta: Optional[float] = Field(None, alias="temperature_delta")
    temperature_deviation: Optional[float] = Field(None, alias="temperature_deviation")  # Deprecated
    temperature_trend_deviation: Optional[float] = Field(None, alias="temperature_trend_deviation")
=======
    sleep_phase_5_min: Optional[str] = Field(

        None, alias="sleep_phase_5_min"

    )  # Deprecated
    time_in_bed: Optional[int] = Field(None, alias="time_in_bed")
    total_sleep_duration: Optional[int] = Field(

        None, alias="total_sleep_duration"

    )
    type: Optional[str] = Field(

        None, alias="type"

    )  # Enum: "deleted", "long_sleep", "main_sleep", "nap", "rest"
    average_hrv: Optional[float] = Field(None, alias="average_hrv")
    awake_time: Optional[int] = Field(None, alias="awake_time")
    hr_60_second_average: Optional[List[int]] = Field(

        None, alias="hr_60_second_average"

    )  # New in v2.10
    hrv_4_hour_average: Optional[List[float]] = Field(

        None, alias="hrv_4_hour_average"

    )  # New in v2.10
    readiness: Optional[str] = Field(

        None, alias="readiness"

    )  # New in v2.10, but type not specified, assuming string for now
    temperature_delta: Optional[float] = Field(

        None, alias="temperature_delta"

    )
    temperature_deviation: Optional[float] = Field(

        None, alias="temperature_deviation"

    )  # Deprecated
    temperature_trend_deviation: Optional[float] = Field(

        None, alias="temperature_trend_deviation"

    )

>>>>>>> cd7b1320f6e9ecc96b943f9eaa71c4a664f66e3f


class DailySleepResponse(BaseModel):
    data: List[DailySleepModel]
    next_token: Optional[str] = None

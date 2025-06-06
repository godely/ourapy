from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date, datetime  # Added date
from oura_api_client.models.daily_readiness import ReadinessContributors  # Reusing ReadinessContributors
from oura_api_client.models.daily_sleep import SleepContributors  # Reusing SleepContributors


class SleepModel(BaseModel):
    id: str
    average_breath: Optional[float] = Field(None, alias="average_breath")  # New based on common sleep metrics
    average_heart_rate: Optional[float] = Field(None, alias="average_heart_rate")
    average_hrv: Optional[int] = Field(None, alias="average_hrv")  # Changed type to int based on typical HRV units
    awake_time: Optional[int] = Field(None, alias="awake_time")
    bedtime_end: Optional[datetime] = Field(None, alias="bedtime_end")
    bedtime_start: Optional[datetime] = Field(None, alias="bedtime_start")
    day: date  # Added day
    deep_sleep_duration: Optional[int] = Field(None, alias="deep_sleep_duration")
    efficiency: Optional[int] = Field(None, alias="efficiency")
    heart_rate: Optional[str] = Field(None, alias="heart_rate")  # Assuming string for heart_rate, adjust if it's a more complex type
    hrv: Optional[str] = Field(None, alias="hrv")  # Assuming string for hrv, adjust if it's a more complex type
    latency: Optional[int] = Field(None, alias="latency")
    light_sleep_duration: Optional[int] = Field(

        None, alias="light_sleep_duration"

    )
    low_battery_alert: Optional[bool] = Field(None, alias="low_battery_alert")
    lowest_heart_rate: Optional[int] = Field(None, alias="lowest_heart_rate")  # Changed type to int
    movement_30_sec: Optional[str] = Field(None, alias="movement_30_sec")
    period: Optional[int] = Field(None, alias="period")
    readiness: Optional[ReadinessContributors] = Field(None, alias="readiness")  # Reused ReadinessContributors
    readiness_score_delta: Optional[int] = Field(None, alias="readiness_score_delta")
    rem_sleep_duration: Optional[int] = Field(None, alias="rem_sleep_duration")
    restless_periods: Optional[int] = Field(None, alias="restless_periods")  # Added from daily_sleep
    # score is usually part of daily summaries, but can be part of a detailed sleep document
    score: Optional[int] = Field(

        None, alias="score"

    )
    sleep_phase_5_min: Optional[str] = Field(None, alias="sleep_phase_5_min")
    sleep_score_delta: Optional[int] = Field(None, alias="sleep_score_delta")  # New, similar to readiness_score_delta
    sleep_algorithm_version: Optional[str] = Field(None, alias="sleep_algorithm_version")  # New
    temperature_delta: Optional[float] = Field(None, alias="temperature_delta")
    temperature_deviation: Optional[float] = Field(None, alias="temperature_deviation")  # Deprecated in daily_readiness
    temperature_trend_deviation: Optional[float] = Field(None, alias="temperature_trend_deviation")  # From daily_readiness
    time_in_bed: Optional[int] = Field(None, alias="time_in_bed")
    total_sleep_duration: Optional[int] = Field(None, alias="total_sleep_duration")
    type: Optional[str] = Field(None, alias="type")  # From daily_sleep (e.g. "main_sleep", "nap")
    # contributors from daily_sleep.py, as requested by the task
    contributors: SleepContributors


class SleepResponse(BaseModel):
    data: List[SleepModel]
    next_token: Optional[str] = None

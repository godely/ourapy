from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date, datetime


class SleepContributors(BaseModel):
    """Sleep contributors model for sleep data."""

    deep_sleep: Optional[int] = Field(None, alias="deep_sleep")
    efficiency: Optional[int] = Field(None, alias="efficiency")
    latency: Optional[int] = Field(None, alias="latency")
    rem_sleep: Optional[int] = Field(None, alias="rem_sleep")
    restfulness: Optional[int] = Field(None, alias="restfulness")
    timing: Optional[int] = Field(None, alias="timing")
    total_sleep: Optional[int] = Field(None, alias="total_sleep")


class ReadinessContributors(BaseModel):
    """Readiness contributors model for sleep data."""

    activity_balance: Optional[int] = Field(None, alias="activity_balance")
    body_temperature: Optional[int] = Field(None, alias="body_temperature")
    hrv_balance: Optional[int] = Field(None, alias="hrv_balance")
    previous_day_activity: Optional[int] = Field(None, alias="previous_day_activity")
    previous_night: Optional[int] = Field(None, alias="previous_night")
    recovery_index: Optional[int] = Field(None, alias="recovery_index")
    resting_heart_rate: Optional[int] = Field(None, alias="resting_heart_rate")
    sleep_balance: Optional[int] = Field(None, alias="sleep_balance")


class SleepModel(BaseModel):
    id: str
    average_breath: Optional[float] = Field(None, alias="average_breath")
    average_heart_rate: Optional[float] = Field(None, alias="average_heart_rate")
    average_hrv: Optional[int] = Field(None, alias="average_hrv")
    awake_time: Optional[int] = Field(None, alias="awake_time")
    bedtime_end: Optional[datetime] = Field(None, alias="bedtime_end")
    bedtime_start: Optional[datetime] = Field(None, alias="bedtime_start")
    day: date
    deep_sleep_duration: Optional[int] = Field(None, alias="deep_sleep_duration")
    efficiency: Optional[int] = Field(None, alias="efficiency")
    heart_rate: Optional[str] = Field(None, alias="heart_rate")
    hrv: Optional[str] = Field(None, alias="hrv")
    latency: Optional[int] = Field(None, alias="latency")
    light_sleep_duration: Optional[int] = Field(None, alias="light_sleep_duration")
    low_battery_alert: Optional[bool] = Field(None, alias="low_battery_alert")
    lowest_heart_rate: Optional[int] = Field(None, alias="lowest_heart_rate")
    movement_30_sec: Optional[str] = Field(None, alias="movement_30_sec")
    period: Optional[int] = Field(None, alias="period")
    readiness: Optional[ReadinessContributors] = Field(None, alias="readiness")
    readiness_score_delta: Optional[int] = Field(None, alias="readiness_score_delta")
    rem_sleep_duration: Optional[int] = Field(None, alias="rem_sleep_duration")
    restless_periods: Optional[int] = Field(None, alias="restless_periods")
    score: Optional[int] = Field(None, alias="score")
    sleep_phase_5_min: Optional[str] = Field(None, alias="sleep_phase_5_min")
    sleep_score_delta: Optional[int] = Field(None, alias="sleep_score_delta")
    sleep_algorithm_version: Optional[str] = Field(
        None, alias="sleep_algorithm_version"
    )
    temperature_delta: Optional[float] = Field(None, alias="temperature_delta")
    temperature_deviation: Optional[float] = Field(None, alias="temperature_deviation")
    temperature_trend_deviation: Optional[float] = Field(
        None, alias="temperature_trend_deviation"
    )
    time_in_bed: Optional[int] = Field(None, alias="time_in_bed")
    total_sleep_duration: Optional[int] = Field(None, alias="total_sleep_duration")
    type: Optional[str] = Field(None, alias="type")
    contributors: SleepContributors


class SleepResponse(BaseModel):
    data: List[SleepModel]
    next_token: Optional[str] = None

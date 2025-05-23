from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date, datetime

class ActivityContributors(BaseModel):
    meet_daily_targets: Optional[int] = Field(None, alias="meet_daily_targets")
    move_every_hour: Optional[int] = Field(None, alias="move_every_hour")
    recovery_time: Optional[int] = Field(None, alias="recovery_time")
    stay_active: Optional[int] = Field(None, alias="stay_active")
    training_frequency: Optional[int] = Field(None, alias="training_frequency")
    training_volume: Optional[int] = Field(None, alias="training_volume")

class DailyActivityModel(BaseModel):
    id: str
    class_5_min: Optional[str] = Field(None, alias="class_5_min")
    score: Optional[int] = Field(None, alias="score")
    active_calories: Optional[int] = Field(None, alias="active_calories")
    average_met_minutes: Optional[float] = Field(None, alias="average_met_minutes")
    contributors: Optional[ActivityContributors] = Field(None, alias="contributors")
    equivalent_walking_distance: Optional[int] = Field(None, alias="equivalent_walking_distance")
    high_activity_met_minutes: Optional[int] = Field(None, alias="high_activity_met_minutes")
    high_activity_time: Optional[int] = Field(None, alias="high_activity_time")
    inactivity_alerts: Optional[int] = Field(None, alias="inactivity_alerts")
    low_activity_met_minutes: Optional[int] = Field(None, alias="low_activity_met_minutes")
    low_activity_time: Optional[int] = Field(None, alias="low_activity_time")
    medium_activity_met_minutes: Optional[int] = Field(None, alias="medium_activity_met_minutes")
    medium_activity_time: Optional[int] = Field(None, alias="medium_activity_time")
    met: Optional[str] = Field(None, alias="met")
    meters_to_target: Optional[int] = Field(None, alias="meters_to_target")
    non_wear_time: Optional[int] = Field(None, alias="non_wear_time")
    resting_time: Optional[int] = Field(None, alias="resting_time")
    sedentary_met_minutes: Optional[int] = Field(None, alias="sedentary_met_minutes")
    sedentary_time: Optional[int] = Field(None, alias="sedentary_time")
    steps: Optional[int] = Field(None, alias="steps")
    target_calories: Optional[int] = Field(None, alias="target_calories")
    target_meters: Optional[int] = Field(None, alias="target_meters")
    total_calories: Optional[int] = Field(None, alias="total_calories")
    day: date
    timestamp: datetime

class DailyActivityResponse(BaseModel):
    data: List[DailyActivityModel]
    next_token: Optional[str] = None

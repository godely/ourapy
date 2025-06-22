#** Final Oura API V2 Blueprint for Python
#* This document provides a comprehensive, redesigned blueprint for the Oura API V2, engineered for a general-purpose Python library. It is the result of a critical analysis of the official OpenAPI specification and incorporates feedback to create robust, developer-friendly data models and documentation.
#* This is a developer-focused blueprint, not a formal OpenAPI spec, designed for direct translation into Pydantic models.
# 
# 1. Core Data ModelsThese are the foundational Pydantic-style models. They are designed to be intuitive, type-safe, and cover the entire surface of the Oura V2 API data endpoints.

from datetime import date, datetime, timedelta
from enum import Enum
from typing import List, Optional, Dict

# ===================================================================
# ENUMERATION MODELS
# ===================================================================

class ScoreContributor(str, Enum):
    """Enumeration for factors contributing to a readiness or sleep score."""
    ACTIVITY_BALANCE = "activity_balance"
    BODY_TEMPERATURE = "body_temperature"
    HRV_BALANCE = "hrv_balance"
    PREVIOUS_DAY_ACTIVITY = "previous_day_activity"
    PREVIOUS_NIGHT = "previous_night"
    RECOVERY_INDEX = "recovery_index"
    RESTING_HEART_RATE = "resting_heart_rate"
    SLEEP_BALANCE = "sleep_balance"
    DEEP_SLEEP = "deep_sleep"
    EFFICIENCY = "efficiency"
    LATENCY = "latency"
    REM_SLEEP = "rem_sleep"
    RESTFULNESS = "restfulness"
    TIMING = "timing"
    TOTAL_SLEEP = "total_sleep"

class ActivityLevel(str, Enum):
    """Enumeration for activity intensity levels."""
    NON_WEAR = "non_wear"
    REST = "rest"
    INACTIVE = "inactive"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class SleepPhase(str, Enum):
    """Enumeration for sleep phases."""
    AWAKE = "awake"
    LIGHT = "light"
    DEEP = "deep"
    REM = "rem"

class SessionType(str, Enum):
    """Enumeration for session/moment types."""
    BREATHING = "breathing"
    MEDITATION = "meditation"
    NAP = "nap"
    RELAXATION = "relaxation"
    REST = "rest"
    BODY_STATUS = "body_status"

class WorkoutSource(str, Enum):
    """Enumeration for the source of a workout entry."""
    AUTODETECTED = "autodetected"
    CONFIRMED = "confirmed"
    MANUAL = "manual"
    WORKOUT_HEART_RATE = "workout_heart_rate"

class ResilienceLevel(str, Enum):
    """Enumeration for long-term resilience levels."""
    LIMITED = "limited"
    ADEQUATE = "adequate"
    SOLID = "solid"
    STRONG = "strong"
    EXCEPTIONAL = "exceptional"

class RingDesign(str, Enum):
    """Enumeration for Oura Ring designs."""
    BALANCE = "balance"
    BALANCE_DIAMOND = "balance_diamond"
    HERITAGE = "heritage"
    HORIZON = "horizon"

class RingColor(str, Enum):
    """Enumeration for Oura Ring colors."""
    BRUSHED_SILVER = "brushed_silver"
    GLOSSY_BLACK = "glossy_black"
    GLOSSY_GOLD = "glossy_gold"
    GLOSSY_WHITE = "glossy_white"
    GUCCI = "gucci"
    MATT_GOLD = "matt_gold"
    ROSE = "rose"
    SILVER = "silver"
    STEALTH_BLACK = "stealth_black"
    TITANIUM = "titanium"

class RingHardwareType(str, Enum):
    """Enumeration for Oura Ring hardware generations."""
    GEN1 = "gen1"
    GEN2 = "gen2"
    GEN2M = "gen2m"
    GEN3 = "gen3"

# ===================================================================
# SHARED & REUSABLE MODELS
# ===================================================================

class TimeInterval:
    """A reusable model to represent a time interval with a start and optional end."""
    start: datetime
    end: Optional[datetime] = None

    @property
    def duration(self) -> Optional[timedelta]:
        """Calculates the duration of the interval if an end time is present."""
        if self.end:
            return self.end - self.start
        return None

class TimeSeries:
    """A generic model for time-series data like heart rate or HRV."""
    timestamp: datetime # Start time of the first sample.
    interval_seconds: int # Number of seconds between items.
    items: List[Optional[float]] # The list of sampled data points.

class HeartRateSample:
    """Represents a single heart rate measurement at a point in time."""
    bpm: int
    source: str
    timestamp: datetime

# ===================================================================
# PRIMARY DATA MODELS
# ===================================================================

class PersonalInfo:
    """Represents the user's core biological and demographic information."""
    id: str
    age: Optional[int] = None
    weight_kg: Optional[float] = None
    height_m: Optional[float] = None
    biological_sex: Optional[str] = None
    email: Optional[str] = None

class RingConfiguration:
    """Represents the configuration and hardware details of a user's Oura Ring."""
    id: str
    color: Optional[RingColor] = None
    design: Optional[RingDesign] = None
    firmware_version: Optional[str] = None
    hardware_type: Optional[RingHardwareType] = None
    size: Optional[int] = None
    set_up_at: Optional[datetime] = None

class DailyReadiness:
    """Represents the user's readiness score for a single day."""
    id: str
    day: date
    score: Optional[int] = None
    contributors: Dict[ScoreContributor, int]
    temperature_deviation_celsius: Optional[float] = None
    temperature_trend_deviation_celsius: Optional[float] = None

class DailyActivity:
    """Represents the user's activity summary for a single day."""
    id: str
    day: date
    score: Optional[int] = None
    active_calories: Optional[int] = None
    total_calories: Optional[int] = None
    steps: Optional[int] = None
    equivalent_walking_distance_meters: Optional[int] = None
    non_wear_time: Optional[timedelta] = None
    resting_time: Optional[timedelta] = None
    inactive_time: Optional[timedelta] = None
    low_activity_time: Optional[timedelta] = None
    medium_activity_time: Optional[timedelta] = None
    high_activity_time: Optional[timedelta] = None
    target_calories: Optional[int] = None
    target_meters: Optional[int] = None

class DailySleep:
    """Represents consolidated sleep data for a single sleep period."""
    id: str
    day: date
    bedtime: TimeInterval
    score: Optional[int] = None
    contributors: Dict[ScoreContributor, int]
    total_sleep_duration: Optional[timedelta] = None
    time_in_bed: Optional[timedelta] = None
    sleep_efficiency: Optional[int] = None
    latency: Optional[timedelta] = None
    awake_time: Optional[timedelta] = None
    light_sleep_time: Optional[timedelta] = None
    rem_sleep_time: Optional[timedelta] = None
    deep_sleep_time: Optional[timedelta] = None
    resting_heart_rate: Optional[int] = None
    average_heart_rate: Optional[float] = None
    average_hrv: Optional[int] = None
    hrv_timeseries: Optional[TimeSeries] = None
    heart_rate_timeseries: Optional[TimeSeries] = None
    
class EnhancedTag:
    """Represents a user-created tag for logging events, habits, or feelings."""
    id: str
    interval: TimeInterval
    tag_type_code: Optional[str] = None
    comment: Optional[str] = None
    custom_name: Optional[str] = None

class Workout:
    """Represents a single workout session."""
    id: str
    interval: TimeInterval
    activity: str
    intensity: str
    source: WorkoutSource
    calories: Optional[float] = None
    distance_meters: Optional[float] = None
    label: Optional[str] = None

class Session:
    """Represents a mindfulness, nap, or other session."""
    id: str
    interval: TimeInterval
    day: date
    type: SessionType
    mood: Optional[str] = None
    heart_rate_timeseries: Optional[TimeSeries] = None
    hrv_timeseries: Optional[TimeSeries] = None

class DailySpo2:
    """Represents the user's blood oxygen saturation (SpO2) summary for a single day."""
    id: str
    day: date
    average_spo2_percentage: Optional[float] = None

class DailyStress:
    """Represents the user's stress and recovery summary for a single day."""
    id: str
    day: date
    stress_high_duration: Optional[timedelta] = None
    recovery_high_duration: Optional[timedelta] = None
    
class DailyResilience:
    """Represents the user's resilience summary for a single day."""
    id: str
    day: date
    level: Optional[ResilienceLevel] = None

class CardiovascularAge:
    """Represents the user's cardiovascular age assessment."""
    id: str
    day: date
    vascular_age: Optional[float] = None

class VO2Max:
    """Represents the user's VO2 Max assessment (maximal oxygen uptake)."""
    id: str
    day: date
    vo2_max: Optional[float] = None

class HeartRateData:
    """Represents a collection of heart rate measurements over a time interval."""
    data: List[HeartRateSample]
    next_token: Optional[str] = None


# 2. API Client DefinitionThis section defines the methods for a comprehensive client, with detailed documentation suitable for a high-quality library.# python
# Base URL for all API calls: https://api.ouraring.com/v2/usercollection

class OuraApiClient:
    """A conceptual Python client for interacting with the optimized Oura API models."""

    def get_personal_info(self) -> PersonalInfo:
        """
        Retrieves the user's basic biological and demographic information.
        
        This data changes infrequently and is suitable for caching.

        Returns:
            PersonalInfo: An object containing the user's age, weight, height, etc.
        """
        pass
        
    def get_ring_configurations(self) -> List[RingConfiguration]:
        """
        Retrieves a list of all rings ever associated with the user's account.

        Returns:
            List[RingConfiguration]: A list of objects, each detailing a specific ring's
                                     hardware, color, size, and firmware version.
        """
        pass

    def get_daily_readiness(self, start_date: date, end_date: Optional[date] = None) -> List[DailyReadiness]:
        """
        Retrieves daily readiness summaries for a given date range.

        Args:
            start_date: The first day of the query range.
            end_date: The last day of the query range. If None, queries for start_date only.

        Returns:
            List[DailyReadiness]: A list of readiness objects, one for each day in the range.
        """
        pass

    def get_daily_activity(self, start_date: date, end_date: Optional[date] = None) -> List[DailyActivity]:
        """
        Retrieves daily activity summaries for a given date range.

        Args:
            start_date: The first day of the query range.
            end_date: The last day of the query range. If None, queries for start_date only.

        Returns:
            List[DailyActivity]: A list of activity objects, one for each day in the range.
        """
        pass

    def get_daily_sleep(self, start_date: date, end_date: Optional[date] = None) -> List[DailySleep]:
        """
        Retrieves comprehensive sleep data for a given date range.

        Note: A robust implementation of this method should intelligently query both
        the `/daily_sleep` and `/sleep` endpoints to construct the complete `DailySleep` model.
        
        Args:
            start_date: The first day of the query range.
            end_date: The last day of the query range. If None, queries for start_date only.

        Returns:
            List[DailySleep]: A list of sleep objects, one for each sleep period in the range.
        """
        pass

    def get_daily_spo2(self, start_date: date, end_date: Optional[date] = None) -> List[DailySpo2]:
        """
        Retrieves daily blood oxygen saturation (SpO2) summaries.

        Args:
            start_date: The first day of the query range.
            end_date: The last day of the query range. If None, queries for start_date only.

        Returns:
            List[DailySpo2]: A list of SpO2 objects, one for each day in the range.
        """
        pass

    def get_daily_stress(self, start_date: date, end_date: Optional[date] = None) -> List[DailyStress]:
        """
        Retrieves daily stress and recovery summaries.

        Args:
            start_date: The first day of the query range.
            end_date: The last day of the query range. If None, queries for start_date only.

        Returns:
            List[DailyStress]: A list of stress objects, one for each day in the range.
        """
        pass

    def get_daily_resilience(self, start_date: date, end_date: Optional[date] = None) -> List[DailyResilience]:
        """
        Retrieves daily resilience summaries.

        Args:
            start_date: The first day of the query range.
            end_date: The last day of the query range. If None, queries for start_date only.

        Returns:
            List[DailyResilience]: A list of resilience objects, one for each day in the range.
        """
        pass

    def get_cardiovascular_age(self, start_date: date, end_date: Optional[date] = None) -> List[CardiovascularAge]:
        """
        Retrieves cardiovascular age assessments.

        Args:
            start_date: The first day of the query range.
            end_date: The last day of the query range. If None, queries for start_date only.

        Returns:
            List[CardiovascularAge]: A list of cardiovascular age objects.
        """
        pass

    def get_vo2_max(self, start_date: date, end_date: Optional[date] = None) -> List[VO2Max]:
        """
        Retrieves VO2 Max assessments.

        Args:
            start_date: The first day of the query range.
            end_date: The last day of the query range. If None, queries for start_date only.

        Returns:
            List[VO2Max]: A list of VO2 Max assessment objects.
        """
        pass

    def get_heart_rate(self, start_datetime: datetime, end_datetime: Optional[datetime] = None) -> HeartRateData:
        """
        Retrieves high-resolution, time-series heart rate data.

        Args:
            start_datetime: The start timestamp of the query range.
            end_datetime: The end timestamp of the query range.

        Returns:
            HeartRateData: An object containing a list of heart rate samples.
        """
        pass

    def get_workouts(self, start_date: date, end_date: Optional[date] = None) -> List[Workout]:
        """
        Retrieves user-logged workouts for a given date range.

        Args:
            start_date: The first day of the query range.
            end_date: The last day of the query range. If None, queries for start_date only.

        Returns:
            List[Workout]: A list of workout objects.
        """
        pass

    def get_sessions(self, start_date: date, end_date: Optional[date] = None) -> List[Session]:
        """
        Retrieves mindfulness, nap, and other guided/unguided sessions.

        Args:
            start_date: The first day of the query range.
            end_date: The last day of the query range. If None, queries for start_date only.

        Returns:
            List[Session]: A list of session objects.
        """
        pass
    
    def get_enhanced_tags(self, start_date: date, end_date: Optional[date] = None) -> List[EnhancedTag]:
        """
        Retrieves user-created tags for logging events, habits, or feelings.

        Args:
            start_date: The first day of the query range.
            end_date: The last day of the query range. If None, queries for start_date only.

        Returns:
            List[EnhancedTag]: A list of tag objects.
        """
        pass

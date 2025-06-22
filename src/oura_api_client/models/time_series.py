from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import datetime


class TimeSeriesData(BaseModel):
    """
    Time series data structure for various Oura metrics.

    This model represents time-series data with a consistent structure across different
    endpoints. The timestamp is automatically converted from ISO 8601 format to Unix
    timestamp for easier programmatic use.
    """

    interval: int = Field(
        ..., description="Interval in seconds between the sampled items."
    )
    items: List[Optional[float]] = Field(
        ...,
        description="Recorded sample items. Null values indicate missing data points.",
    )
    timestamp: int = Field(
        ...,
        description="Unix timestamp (seconds since epoch) when the sample recording started.",
    )

    @field_validator("timestamp", mode="before")
    @classmethod
    def parse_timestamp(cls, v):
        """Convert ISO 8601 timestamp string to unix timestamp."""
        if isinstance(v, str):
            dt = datetime.fromisoformat(v.replace("Z", "+00:00"))
            return int(dt.timestamp())
        return v

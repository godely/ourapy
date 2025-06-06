"""Models for heart rate data."""

from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime


@dataclass

class HeartRateSample:
    """Represents a single heart rate data point."""

    timestamp: datetime
    bpm: int
    source: str

    @classmethod
    def from_dict(cls, data: dict) -> "HeartRateSample":
        """Create a HeartRateSample from API response dictionary.

        Args:
            data: Dictionary containing heart rate data

        Returns:
            HeartRateSample: Instantiated object
        """
        return cls(
            timestamp=datetime.fromisoformat(data["timestamp"]),
            bpm=data["bpm"],
            source=data["source"],
        )


@dataclass

class HeartRateResponse:
    """Represents the full heart rate response."""

    data: List[HeartRateSample]
    next_token: Optional[str] = None

    @classmethod
    def from_dict(cls, response: dict) -> "HeartRateResponse":
        """Create a HeartRateResponse from API response dictionary.

        Args:
            response: Dictionary containing API response

        Returns:
            HeartRateResponse: Instantiated object
        """
        return cls(
            data=[HeartRateSample.from_dict(item) for item in response.get("data", [])],
            next_token=response.get("next_token"),
        )

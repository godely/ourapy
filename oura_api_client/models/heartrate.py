"""Models for heart rate data."""

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class HeartRateSample(BaseModel):
    """Represents a single heart rate data point."""
    
    timestamp: datetime
    bpm: int
    source: str

    @classmethod
    def from_dict(cls, data: dict) -> "HeartRateSample":
        """Create a HeartRateSample from API response dictionary.
        
        Note: This method is kept for backward compatibility.
        Pydantic can parse directly from dict using HeartRateSample(**data)
        
        Args:
            data: Dictionary containing heart rate data
            
        Returns:
            HeartRateSample: Instantiated object
        """
        return cls(**data)


class HeartRateResponse(BaseModel):
    """Represents the full heart rate response."""
    
    data: List[HeartRateSample]
    next_token: Optional[str] = None

    @classmethod
    def from_dict(cls, response: dict) -> "HeartRateResponse":
        """Create a HeartRateResponse from API response dictionary.
        
        Note: This method is kept for backward compatibility.
        Pydantic can parse directly from dict using HeartRateResponse(**response)
        
        Args:
            response: Dictionary containing API response
            
        Returns:
            HeartRateResponse: Instantiated object
        """
        return cls(**response)

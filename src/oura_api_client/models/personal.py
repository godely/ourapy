"""Models for personal information data."""

from pydantic import BaseModel
from typing import Optional
from datetime import date


class PersonalInfo(BaseModel):
    """Represents personal information for a user."""

    id: str
    email: str
    age: int
    weight: Optional[float] = None
    height: Optional[float] = None
    biological_sex: Optional[str] = None
    birth_date: Optional[date] = None

    @classmethod
    def from_dict(cls, data: dict) -> "PersonalInfo":
        """Create a PersonalInfo object from API response dictionary.

        Note: This method is kept for backward compatibility.
        Pydantic can parse directly from dict using PersonalInfo(**data)

        Args:
            data: Dictionary containing personal info data

        Returns:
            PersonalInfo: Instantiated object
        """
        return cls(**data)

"""Models for personal information data."""

from dataclasses import dataclass
from typing import Optional
from datetime import date


@dataclass

class PersonalInfo:
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

        Args:
            data: Dictionary containing personal info data

        Returns:
            PersonalInfo: Instantiated object
        """
        birth_date = None
        if data.get("birth_date"):
            birth_date = date.fromisoformat(data["birth_date"])

        return cls(
            id=data["id"],
            email=data["email"],
            age=data["age"],
            weight=data.get("weight"),
            height=data.get("height"),
            biological_sex=data.get("biological_sex"),
            birth_date=birth_date,
        )

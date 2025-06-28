from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date, datetime  # Added date

# WorkoutIntensity and WorkoutSource are enums, but Pydantic uses Literal for this
from typing import Literal


class WorkoutModel(BaseModel):
    id: str
    activity: str  # Name of the activity
    calories: Optional[float] = None
    day: date
    distance: Optional[float] = None  # Meters
    end_datetime: datetime = Field(alias="end_datetime")
    energy: Optional[float] = Field(None, alias="energy")  # Kilojoules
    intensity: Literal[
        "easy", "hard", "moderate", "restorative"  # New based on common workout apps
    ]
    label: Optional[str] = None
    source: Literal[
        "apple_health",
        "auto_detected",
        "google_fit",
        "health_connect",  # New based on Android ecosystem
        "manual",
        "strava",  # New based on common integrations
        "oura_app",  # New for workouts logged directly in Oura
    ]
    start_datetime: datetime = Field(alias="start_datetime")
    # New fields from OpenAPI spec for Workout, if any, would be added here.
    # For now, using a common set of fields for workout tracking.
    # Example:
    # route_coordinates: Optional[str] = Field(
    #     None, alias="route_coordinates"
    # )  # If GPS data was available


class WorkoutResponse(BaseModel):
    data: List[WorkoutModel]
    next_token: Optional[str] = None

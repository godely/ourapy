from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date, datetime


class EnhancedTagModel(BaseModel):
    id: str
<<<<<<< HEAD
    tag_type_code: str  # e.g., "common_cold", "period"
    start_time: datetime = Field(alias="start_time")
    end_time: Optional[datetime] = Field(None, alias="end_time")
    start_day: Optional[date] = Field(None, alias="start_day")  # New based on typical usage
    end_day: Optional[date] = Field(None, alias="end_day")  # New based on typical usage
    comment: Optional[str] = None  # Based on OpenAPI spec, there might be other fields,
=======
    tag_type_code: str = Field(
     alias="tag_type_code"
 )  # e.g., "common_cold", "period"
    start_time: datetime = Field(alias="start_time")
    end_time: Optional[datetime] = Field(None, alias="end_time")
    start_day: Optional[date] = Field(

        None, alias="start_day"

    )  # New based on typical usage
    end_day: Optional[date] = Field(

        None, alias="end_day"

    )  # New based on typical usage
    comment: Optional[str] = None
    # Based on OpenAPI spec, there might be other fields,
>>>>>>> cd7b1320f6e9ecc96b943f9eaa71c4a664f66e3f
    # but these are the core ones usually associated with enhanced tags.
    # If a more detailed spec is available, other fields like 'icon' or 'source' could be added.


class EnhancedTagResponse(BaseModel):
    data: List[EnhancedTagModel]
    next_token: Optional[str] = None

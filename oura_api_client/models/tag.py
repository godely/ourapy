from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime


class TagModel(BaseModel):
    id: str
    day: date
    text: Optional[str] = None  # Optional based on OpenAPI spec
    timestamp: datetime  # Changed from Optional[datetime] to datetime as it's usually present
    # New fields from OpenAPI spec for Tag
    # Assuming 'tag_type_code' and 'start_time', 'end_time' might be part
    # of a more detailed spec,
    # but the provided snippet for Tag is simple.
    # For now, sticking to id, day, text, timestamp as core.
    # If more fields like 'tag_type_code', 'start_time', 'end_time' are
    # confirmed, they can be added.
    # Example of what they might look like if added:
    # tag_type_code: Optional[str] = Field(None, alias="tag_type_code")
    # start_time: Optional[datetime] = Field(None, alias="start_time")
    # end_time: Optional[datetime] = Field(None, alias="end_time")


class TagResponse(BaseModel):
    data: List[TagModel]
    next_token: Optional[str] = None

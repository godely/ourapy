from pydantic import BaseModel, Field
<<<<<<< HEAD
from typing import List, Optional, Literal
from datetime import datetime


=======
from typing import List, Optional
from datetime import datetime
# Enum-like fields will be handled with Literal
from typing import Literal
>>>>>>> cd7b1320f6e9ecc96b943f9eaa71c4a664f66e3f


class RingConfigurationModel(BaseModel):
    id: str
    # Fields based on OpenAPI spec for RingConfiguration
    # Using Literal for fields that are described as enums
    color: Optional[Literal[
        "black",
        "brushed_titanium",  # New
        "gold",
        "graphite",  # New
        "rose_gold",
        "silver",
        "stealth_black"  # Typo in spec? "stealth" is common, "stealth_black" is more specific
    ]] = Field(None, alias="color")
    design: Optional[Literal[
        "balance",  # New
        "gucci",  # New
        "heritage",
        "horizon"
    ]] = Field(

        None, alias="design"

    )
    firmware_version: Optional[str] = Field(None, alias="firmware_version")
    hardware_type: Optional[Literal[
        "gen1",
        "gen2",
        "gen2m",
        "gen3"
    ]] = Field(

        None, alias="hardware_type"

    )
    # 'id' is already included
<<<<<<< HEAD
    set_up_at: Optional[datetime] = Field(None, alias="set_up_at")  # Changed from setup_at for Pythonic convention
    size: Optional[int] = Field(None, alias="size")
=======
    set_up_at: Optional[datetime] = Field(

        None, alias="set_up_at"

    )  # Changed from setup_at for Pythonic convention
    size: Optional[int] = Field(

        None, alias="size"

    )
>>>>>>> cd7b1320f6e9ecc96b943f9eaa71c4a664f66e3f

    # RingColor, RingDesign, RingHardwareType are effectively defined by Literals above
    # No separate models needed for them if they are just choices for a field.
    # If they had more complex structures (e.g., RingColor having RGB values),
    # then separate models would be appropriate. The task implies they are simple enums.


class RingConfigurationResponse(BaseModel):
    data: List[RingConfigurationModel]
    next_token: Optional[str] = None

# api/models/location.py

from pydantic import BaseModel, Field
from typing import Optional


class Location(BaseModel):
    lat: Optional[float] = Field(
        ..., example=34.0522, description="The latitude of the location"
    )
    long: Optional[float] = Field(
        ..., example=-118.2437, description="The longitude of the location"
    )
    resolved_address: Optional[str] = Field(
        None,
        example="7 Elm St. New Haven, CT, 06510",
        description="The resolved address of the location",
    )

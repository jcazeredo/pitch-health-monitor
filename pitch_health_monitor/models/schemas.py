from typing import Literal
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from enum import Enum

class Location(BaseModel):
    city: str = Field(..., description="Name of the city")
    country: str = Field(..., description="Name of the country")
    latitude: float = Field(..., description="Latitude coordinate of the location")
    longitude: float = Field(..., description="Longitude coordinate of the location")

class TurfType(str, Enum):
    natural = "natural"
    artificial = "artificial"
    hybrid = "hybrid"

class Pitch(BaseModel):
    schema_version: Literal[1] = 1
    uuid: UUID = Field(..., description="UUID of the pitch")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Date and time when the pitch was created")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Date and time when the pitch was last updated")    
    last_checked_at: datetime = Field(..., description="Date and time when the pitch condition was last checked")   

    name: str = Field(..., description="Name of the pitch")
    location: Location = Field(..., description="Location of the pitch")
    turf_type: TurfType = Field(..., description="Type of turf")
    last_maintenance_date: datetime = Field(..., description="Date and time of the last maintenance")
    next_scheduled_maintenance: datetime = Field(..., description="Date and time of the next scheduled maintenance")
    current_condition: int = Field(..., ge=1, le=10, description="Current condition rating of the pitch (from 1 to 10)")
    replacement_date: datetime = Field(..., description="Date and time for scheduled replacement of the pitch")

    current_consecutive_rain_hours: int = Field(default=0, description="Duration of the current cycle of consecutive rain hours")
    current_consecutive_drying_hours: int = Field(default=0, description="Duration of the current cycle of consecutive drying hours")

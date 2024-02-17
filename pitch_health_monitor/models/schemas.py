from typing import Literal
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from enum import Enum

class Location(BaseModel):
    city: str
    country: str

class TurfType(str, Enum):
    natural = "natural"
    artificial = "artificial"
    hybrid = "hybrid"

class PitchSchema(BaseModel):
    schema_version: Literal[1] = 1
    uuid: UUID = Field(..., description="UUID of the pitch")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Date and time when the pitch was created")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Date and time when the pitch was last updated")
    
    name: str = Field(..., description="Name of the pitch")
    location: Location = Field(..., description="Location of the pitch")
    turf_type: TurfType = Field(..., description="Type of turf")
    last_maintenance_date: datetime = Field(..., description="Date and time of the last maintenance")
    next_scheduled_maintenance: datetime = Field(..., description="Date and time of the next scheduled maintenance")
    current_condition: int = Field(..., ge=1, le=10, description="Current condition rating of the pitch (from 1 to 10)")
    replacement_date: datetime = Field(..., description="Date and time for scheduled replacement of the pitch")
    

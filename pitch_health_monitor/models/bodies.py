
from datetime import datetime

from pydantic import BaseModel, Field

from pitch_health_monitor.models.schemas import Location, TurfType

class CreatePitchRequest(BaseModel):
    name: str = Field(..., description="Name of the pitch")
    location: Location = Field(..., description="Location of the pitch (city and country)")
    turf_type: TurfType = Field(..., description="Type of turf (e.g., Natural, Artificial, Hybrid)")
    last_maintenance_date: datetime = Field(..., description="Date and time of the last maintenance")
    next_scheduled_maintenance: datetime = Field(..., description="Date and time of the next scheduled maintenance")
    current_condition: int = Field(1, ge=1, le=10, description="Current condition rating of the pitch (from 1 to 10)")
    replacement_date: datetime = Field(..., description="Date and time for scheduled replacement of the pitch")

class UpdatePitchRequest(BaseModel):
    name: str = Field(None, description="Name of the pitch")
    location: Location = Field(None, description="Location of the pitch (city and country)")
    turf_type: TurfType = Field(None, description="Type of turf (e.g., Natural, Artificial, Hybrid)")
    last_maintenance_date: datetime = Field(None, description="Date and time of the last maintenance")
    next_scheduled_maintenance: datetime = Field(None, description="Date and time of the next scheduled maintenance")
    current_condition: int = Field(None, ge=1, le=10, description="Current condition rating of the pitch (from 1 to 10)")
    replacement_date: datetime = Field(None, description="Date and time for scheduled replacement of the pitch")
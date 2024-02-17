
from datetime import datetime

from pydantic import BaseModel, Field

from pitch_health_monitor.models.schemas import Location, TurfType

class CreatePitchRequest(BaseModel):
    name: str = Field(..., example="Fritz-Walter-Stadion", description="Name of the pitch")
    location: Location = Field(..., example=Location(city="Kaiserslautern", country="Germany", latitude=49.43432260240235, longitude=7.7766827641282985), description="Location of the pitch (city and country)")
    turf_type: TurfType = Field(..., example=TurfType.natural, description="Type of turf (e.g., Natural, Artificial, Hybrid)")
    current_condition: int = Field(10, ge=1, le=10, example=10, description="Current condition rating of the pitch (from 1 to 10)")

class UpdatePitchRequest(BaseModel):
    name: str = Field(None, example="Fritz-Walter-Stadion", description="Name of the pitch")
    location: Location = Field(None, example=Location(city="Kaiserslautern", country="Germany", latitude=49.43432260240235, longitude=7.7766827641282985), description="Location of the pitch (city and country)")
    turf_type: TurfType = Field(None, example=TurfType.natural, description="Type of turf (e.g., Natural, Artificial, Hybrid)")
    current_condition: int = Field(None, ge=1, le=10, example=10, description="Current condition rating of the pitch (from 1 to 10)")
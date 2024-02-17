from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from pitch_health_monitor.models.schemas import Location, TurfType


class PitchResponse(BaseModel):
    uuid: UUID = Field(..., description="UUID of the pitch")
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Date and time when the pitch was created",
    )
    last_checked_at: Optional[datetime] = Field(
        None, description="Date and time when the pitch condition was last checked"
    )

    name: str = Field(
        ..., example="Fritz-Walter-Stadion", description="Name of the pitch"
    )
    location: Location = Field(
        ...,
        example=Location(
            city="Kaiserslautern",
            country="Germany",
            latitude=49.43432260240235,
            longitude=7.7766827641282985,
        ),
        description="Location of the pitch",
    )
    turf_type: TurfType = Field(
        ..., example=TurfType.natural, description="Type of turf"
    )
    current_condition: int = Field(
        ...,
        ge=1,
        le=10,
        example=10,
        description="Current condition rating of the pitch (from 1 to 10)",
    )

    last_maintenance_date: Optional[datetime] = Field(
        None, description="Date and time of the last maintenance"
    )
    next_scheduled_maintenance: Optional[datetime] = Field(
        None, description="Date and time of the next scheduled maintenance"
    )
    replacement_date: Optional[datetime] = Field(
        None, description="Date and time for scheduled replacement of the pitch"
    )

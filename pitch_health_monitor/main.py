import asyncio
from contextlib import asynccontextmanager
from datetime import datetime
from typing import List
from fastapi import FastAPI, HTTPException, Path, Body
from pitch_health_monitor.database.db_methods import (
    get_all_pitches_from_db,
    get_pitch_from_db,
    create_pitch_in_db,
    update_pitch_in_db,
    delete_pitch_from_db,
)
from pitch_health_monitor.services.pitch_monitor.maintenance_utils import (
    perform_maintenance,
)
from pitch_health_monitor.services.pitch_monitor.processor import (
    process_all_pitches_periodically,
)
from starlette.status import (
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_400_BAD_REQUEST,
)
from dotenv import load_dotenv
from uuid import UUID, uuid4
from pitch_health_monitor.models.bodies import CreatePitchRequest, UpdatePitchRequest
from pitch_health_monitor.models.responses import PitchResponse
from pitch_health_monitor.models.schemas import Pitch

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start the routine that will process all pitches health status
    asyncio.create_task(process_all_pitches_periodically())

    yield


app = FastAPI(lifespan=lifespan)


@app.post(
    "/pitches/", response_model=UUID, description="Create a new pitch", tags=["Pitches"]
)
def create_pitch(pitch_request: CreatePitchRequest) -> UUID:

    new_pitch = Pitch(
        uuid=uuid4(),
        name=pitch_request.name,
        location=pitch_request.location,
        turf_type=pitch_request.turf_type,
        current_condition=pitch_request.current_condition,
    )

    if not create_pitch_in_db(new_pitch):
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create new pitch",
        )

    return new_pitch.uuid


@app.put(
    "/pitches/{pitch_id}",
    response_model=None,
    description="Update a pitch by its ID",
    tags=["Pitches"],
)
def update_pitch(pitch_id: UUID, pitch_request: UpdatePitchRequest) -> None:

    if not update_pitch_in_db(pitch_id, pitch_request):
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="Pitch not found or not updated"
        )


@app.delete(
    "/pitches/{pitch_id}",
    response_model=None,
    description="Delete a pitch by its ID",
    tags=["Pitches"],
)
def delete_pitch(pitch_id: UUID) -> None:

    if not delete_pitch_from_db(pitch_id):
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="Pitch not found or not deleted"
        )


@app.get(
    "/pitches/",
    response_model=List[PitchResponse],
    description="Retrieve all pitches",
    tags=["Pitches"],
)
def get_all_pitches() -> List[PitchResponse]:

    pitches = get_all_pitches_from_db()
    pitch_responses = [
        PitchResponse.model_validate(pitch.model_dump()) for pitch in pitches
    ]

    return pitch_responses


@app.get(
    "/pitches/{pitch_id}",
    response_model=PitchResponse,
    description="Retrieve a pitch by its ID",
    tags=["Pitches"],
)
def get_pitch(
    pitch_id: UUID = Path(..., description="The ID of the pitch to retrieve"),
) -> PitchResponse:

    pitch = get_pitch_from_db(pitch_id)

    if pitch is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Pitch not found")
    pitch_response = PitchResponse.model_validate(pitch)

    return pitch_response


@app.get(
    "/pitches/maintenance-required",
    response_model=List[PitchResponse],
    tags=["Maintenance"],
)
def get_pitches_needing_maintenance() -> List[PitchResponse]:

    maintenance_required_filter = {"current_condition": {"$gt": 2, "$lt": 10}}

    pitches = get_all_pitches_from_db(maintenance_required_filter)

    return [PitchResponse.model_validate(pitch.model_dump()) for pitch in pitches]


@app.get(
    "/pitches/turf-replacement-required",
    response_model=List[PitchResponse],
    tags=["Maintenance"],
)
def get_pitches_needing_turf_replacement() -> List[PitchResponse]:

    turf_replacement_required_filter = {"current_condition": {"$lte": 2}}

    pitches = get_all_pitches_from_db(turf_replacement_required_filter)

    return [PitchResponse.model_validate(pitch.model_dump()) for pitch in pitches]


@app.post(
    "/pitches/{pitch_id}/schedule-turf-replacement",
    response_model=None,
    tags=["Maintenance"],
)
def schedule_turf_replacement(
    pitch_id: UUID,
    replacement_date: datetime = Body(
        ...,
        embed=True,
        description="The future date when turf replacement is scheduled. Must be a datetime object in the future.",
    ),
) -> None:

    pitch = get_pitch_from_db(pitch_id)
    if pitch is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Pitch not found")

    # Check if the provided replacement date is in the future
    if replacement_date <= datetime.utcnow():
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Replacement date must be in the future",
        )

    # Set the replacement date for the pitch
    pitch.replacement_date = replacement_date

    # Update the pitch record in the database
    update_pitch_in_db(pitch_id, pitch)


@app.post(
    "/pitches/{pitch_id}/execute-maintenance", response_model=None, tags=["Maintenance"]
)
def execute_maintenance(pitch_id: UUID) -> None:

    pitch = get_pitch_from_db(pitch_id)
    if pitch is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Pitch not found")

    # Check if there is a scheduled maintenance date and it is due (today or in the past)
    if (
        pitch.next_scheduled_maintenance is None
        or pitch.next_scheduled_maintenance > datetime.utcnow()
    ):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="No due maintenance scheduled for this pitch",
        )

    pitch = perform_maintenance(pitch)

    update_pitch_in_db(pitch_id, pitch)

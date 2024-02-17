from fastapi import FastAPI, HTTPException, Path
from starlette.status import HTTP_404_NOT_FOUND
from dotenv import load_dotenv
from uuid import UUID, uuid4
from pitch_health_monitor.models.bodies import CreatePitchRequest, UpdatePitchRequest
from pitch_health_monitor.models.responses import PitchResponse

from pitch_health_monitor.models.schemas import PitchSchema
from .database import pitches_collection

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

@app.post("/pitches/", response_model=UUID, description="Create a new pitch")
def create_pitch(pitch_request: CreatePitchRequest) -> UUID:

    new_pitch = PitchSchema(
        uuid=uuid4(),
        name=pitch_request.name,
        location=pitch_request.location,
        turf_type=pitch_request.turf_type,
        last_maintenance_date=pitch_request.last_maintenance_date,
        next_scheduled_maintenance=pitch_request.next_scheduled_maintenance,
        current_condition=pitch_request.current_condition,
        replacement_date=pitch_request.replacement_date
    )

    pitches_collection.insert_one(new_pitch.model_dump())

    return new_pitch.uuid

@app.get("/pitches/{pitch_id}", response_model=PitchResponse, description="Retrieve a pitch by its ID")
def get_pitch(pitch_id: UUID = Path(..., description="The ID of the pitch to retrieve")) -> PitchResponse:

    pitch_data = pitches_collection.find_one({"uuid": pitch_id})

    if pitch_data is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Pitch not found")

    pitch_response = PitchResponse.model_validate(pitch_data)

    return pitch_response

@app.put("/pitches/{pitch_id}", response_model=None, description="Update a pitch by its ID")
def update_pitch(pitch_id: UUID, pitch_request: UpdatePitchRequest) -> None:
    updated_pitch = PitchSchema(
        uuid=pitch_id,
        name=pitch_request.name,
        location=pitch_request.location,
        turf_type=pitch_request.turf_type,
        last_maintenance_date=pitch_request.last_maintenance_date,
        next_scheduled_maintenance=pitch_request.next_scheduled_maintenance,
        current_condition=pitch_request.current_condition,
        replacement_date=pitch_request.replacement_date
    )
    result = pitches_collection.update_one({"uuid": pitch_id}, {"$set": updated_pitch.model_dump()})

    if result.modified_count == 0:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Pitch not found")

@app.delete("/pitches/{pitch_id}", response_model=None, description="Delete a pitch by its ID")
def delete_pitch(pitch_id: UUID) -> None:

    result = pitches_collection.delete_one({"uuid": pitch_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Pitch not found")
    
    return pitch_id
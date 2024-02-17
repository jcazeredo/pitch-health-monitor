from typing import List, Optional
from uuid import UUID
from pitch_health_monitor.models.schemas import Pitch
from . import db_client

pitches_collection = db_client.get_database().get_collection('pitches')

def update_pitch_in_db(pitch_uuid: UUID, pitch: Pitch) -> bool:
    """
    Update a pitch object in the database.

    Args:
        pitch_uuid: The UUID of the pitch object to delete from the database.
        pitch: The pitch object to update in the database.

    Returns:
        bool: True if the pitch was successfully updated, False otherwise.
    """

    result = pitches_collection.update_one({"uuid": pitch_uuid}, {"$set": pitch.model_dump()})

    return result.modified_count > 0

def create_pitch_in_db(pitch: Pitch) -> bool:
    """
    Create a new pitch object in the database.
    
    Args:
        pitch: The pitch object to create in the database.

    Returns:
        bool: True if the pitch was successfully created, False otherwise.
    """

    result = pitches_collection.insert_one(pitch.model_dump())

    return result.acknowledged

def delete_pitch_from_db(pitch_uuid: UUID) -> bool:
    """
    Delete a pitch object from the database.

    Args:
        pitch_uuid: The UUID of the pitch object to delete from the database.

    Returns:
        bool: True if the pitch was successfully deleted, False otherwise.
    """

    result = pitches_collection.delete_one({"uuid": pitch_uuid})

    return result.deleted_count > 0

def get_pitch_from_db(pitch_id: UUID) -> Optional[Pitch]:
    """
    Retrieve a pitch from the database by its ID.

    Args:
        pitch_id: The ID of the pitch to retrieve.

    Returns:
        Optional[Pitch]: The retrieved pitch object, or None if not found.
    """

    return pitches_collection.find_one({"uuid": pitch_id})

def get_all_pitches_from_db() -> List[Pitch]:
    """
    Retrieve all pitches from the database.

    Returns:
        List[Pitch]: A list of all pitch objects.
    """

    return [Pitch.model_validate(pitch) for pitch in pitches_collection.find({})]
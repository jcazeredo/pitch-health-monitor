from ast import Dict
from typing import List, Optional
from uuid import UUID
from pitch_health_monitor.models.schemas import Pitch
from . import db_client

pitches_collection = db_client.get_database().get_collection("pitches")


def update_pitch_in_db(pitch_uuid: UUID, pitch: Pitch) -> bool:
    """
    Update a pitch object in the database.

    Args:
        pitch_uuid: The UUID of the pitch object to delete from the database.
        pitch: The pitch object to update in the database.

    Returns:
        bool: True if the pitch was successfully updated, False otherwise.
    """

    result = pitches_collection.update_one(
        {"uuid": pitch_uuid}, {"$set": pitch.model_dump()}
    )

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


def get_pitch_from_db(
    pitch_id: UUID, filters: Optional[Dict] = None
) -> Optional[Pitch]:
    """
    Retrieve a pitch from the database by its ID and optional additional filters.

    Args:
        pitch_id: The ID of the pitch to retrieve.
        filters: Optional dictionary of additional filter criteria.

    Returns:
        Optional[Pitch]: The retrieved pitch object, or None if not found.
    """

    query = {"uuid": pitch_id}

    # If additional filters are provided, update the query with these filters
    if filters:
        query.update(filters)

    return pitches_collection.find_one(query)


def get_all_pitches_from_db(filters: Optional[Dict] = None) -> List[Pitch]:
    """
    Retrieve all pitches from the database with optional filtering.

    Args:
        filters: Optional dictionary of filter criteria.

    Returns:
        List[Pitch]: A list of pitch objects that match the filter criteria.
    """

    # Use an empty dictionary if no filters are provided
    query_filters = filters if filters is not None else {}

    # Retrieve pitches from the database that match the filter criteria
    pitches = pitches_collection.find(query_filters)

    # Convert each pitch document into a Pitch object
    return [Pitch.model_validate(pitch) for pitch in pitches]

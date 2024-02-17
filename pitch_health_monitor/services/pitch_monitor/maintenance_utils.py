from datetime import datetime, timedelta
from pitch_health_monitor.models.schemas import Pitch

from pitch_health_monitor.services.pitch_monitor.constants import DRYING_TIME


def reschedule_due_to_rain(pitch: Pitch, is_raining_now: bool) -> Pitch:
    """
    Reschedule the pitch maintenance due to rain, if it is raining and maintenance is scheduled soon.

    Args:
        pitch: The pitch object to check and possibly reschedule.
        is_raining_now (bool): Indicates whether it is currently raining.

    Returns:
        The updated pitch object with possibly rescheduled maintenance.
    """

    if is_raining_now and _is_maintenance_soon(pitch):
        pitch.next_scheduled_maintenance = datetime.utcnow() + timedelta(
            hours=DRYING_TIME[pitch.turf_type]
        )

    return pitch


def schedule_regular_maintenance(pitch: Pitch) -> Pitch:
    """
    Schedule regular maintenance for the pitch if its condition is below a certain threshold and no maintenance is scheduled.

    Args:
        pitch: The pitch object to schedule maintenance for.

    Returns:
        The updated pitch object with scheduled maintenance.
    """

    if (
        pitch.next_scheduled_maintenance is None
        and pitch.current_condition > 2
        and pitch.current_condition < 10
    ):
        pitch.next_scheduled_maintenance = datetime.utcnow() + timedelta(
            hours=DRYING_TIME[pitch.turf_type]
        )

    return pitch


def cancel_maintenance_if_needed(pitch: Pitch) -> Pitch:
    """
    Cancel any scheduled maintenance if the pitch condition is below a critical threshold.

    Args:
        pitch: The pitch object to cancel maintenance for if needed.

    Returns:
        The updated pitch object with possibly canceled maintenance.
    """

    if pitch.current_condition <= 2:
        pitch.next_scheduled_maintenance = None

    return pitch


def _is_maintenance_soon(pitch: Pitch) -> bool:
    """
    Check if the maintenance for the pitch is scheduled soon.

    Args:
        pitch: The pitch object to check for upcoming maintenance.

    Returns:
        A boolean indicating whether maintenance is scheduled soon.
    """

    return (
        pitch.next_scheduled_maintenance is not None
        and pitch.next_scheduled_maintenance > datetime.utcnow()
    )

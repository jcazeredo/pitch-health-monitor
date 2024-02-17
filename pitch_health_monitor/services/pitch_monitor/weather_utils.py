from pitch_health_monitor.models.schemas import Pitch
from pitch_health_monitor.services.pitch_monitor.constants import RAIN_TOLERANCE


def update_weather_status(pitch: Pitch, is_raining_now: bool) -> bool:
    """
    Update the pitch's weather status based on current weather conditions.

    Args:
        pitch: The pitch object to update.
        is_raining_now (bool): Indicates whether it is currently raining.

    Returns:
        The updated pitch object with the new weather status.
    """

    if is_raining_now:
        pitch.current_consecutive_rain_hours += 1

    return pitch


def apply_rain_damage(pitch: Pitch) -> Pitch:
    """
    Apply damage to the pitch's condition based on the amount of rain it has received and its turf type's tolerance.

    Args:
        pitch: The pitch object to apply rain damage to.

    Returns:
        The updated pitch object with adjusted condition due to rain damage.
    """

    tolerance_hours = RAIN_TOLERANCE[pitch.turf_type]

    if pitch.current_consecutive_rain_hours >= tolerance_hours:
        pitch.current_condition = max(1, pitch.current_condition - 2)
        pitch.current_consecutive_rain_hours = 0

    return pitch

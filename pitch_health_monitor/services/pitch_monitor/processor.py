import asyncio
from datetime import datetime
import os
from pitch_health_monitor.database.db_methods import (
    update_pitch_in_db,
    get_all_pitches_from_db,
)
from pitch_health_monitor.models.schemas import Pitch
from pitch_health_monitor.services.pitch_monitor.maintenance_utils import (
    cancel_maintenance_if_needed,
    reschedule_due_to_rain,
    schedule_regular_maintenance,
)
from pitch_health_monitor.services.pitch_monitor.weather_utils import (
    apply_rain_damage,
    update_weather_status,
)
from pitch_health_monitor.services.weather import OpenWeatherAPI, WeatherAPI

OPEN_WEATHER_API_KEY = os.getenv(
    "OPEN_WEATHER_API_KEY", "a22034aed53ca5845e3c8af45d527d3a"
)

PROCESS_INTERVAL_SECONDS = 30


async def process_all_pitches_periodically():
    """
    Asynchronously process all pitches periodically based on current weather conditions and its health status, including rescheduling maintenance if necessary.
    """

    weather_api = OpenWeatherAPI(OPEN_WEATHER_API_KEY)

    while True:
        print(f"[{datetime.utcnow()}] Processing all pitches health conditions")

        pitches = get_all_pitches_from_db()

        tasks = [process_pitch(pitch, weather_api) for pitch in pitches]

        await asyncio.gather(*tasks)

        # Wait until the next processment
        await asyncio.sleep(PROCESS_INTERVAL_SECONDS)


async def process_pitch(pitch: Pitch, weather_api: WeatherAPI):
    """
    Process the pitch based on current weather conditions and its health status, including rescheduling maintenance if necessary.

    Args:
        pitch: The pitch object to process.
        weather_api: An instance of the WeatherAPI to check current weather conditions.

    Raises:
        Exception: If an error occurs while processing the pitch.
    """

    print(f"[{datetime.utcnow()}] Processing pitch {pitch.name}")

    try:
        is_raining_now = weather_api.is_raining_now(
            pitch.location.city, pitch.location.country
        )

        # Check current weather and update control variables
        pitch = update_weather_status(pitch, is_raining_now)

        # If there was a maintenance scheduled, check if we need to postpone it due to more rain
        pitch = reschedule_due_to_rain(pitch, is_raining_now)

        # Apply rain damage to pitch object if a rain cycle is completed
        pitch = apply_rain_damage(pitch)

        # Check if pitch is not perfect and schedule a maintenance
        pitch = schedule_regular_maintenance(pitch)

        # Cancel maintenance if
        pitch = cancel_maintenance_if_needed(pitch)

        pitch.last_checked_at = datetime.utcnow()

        update_pitch_in_db(pitch.uuid, pitch)

    except Exception as e:
        print(f"Error processing pitch {pitch.uuid}: {e}")

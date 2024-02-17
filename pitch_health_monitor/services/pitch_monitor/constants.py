from pitch_health_monitor.models.schemas import TurfType

DRYING_TIME = {TurfType.artificial: 12, TurfType.hybrid: 24, TurfType.natural: 36}

RAIN_TOLERANCE = {TurfType.artificial: 6, TurfType.hybrid: 4, TurfType.natural: 3}

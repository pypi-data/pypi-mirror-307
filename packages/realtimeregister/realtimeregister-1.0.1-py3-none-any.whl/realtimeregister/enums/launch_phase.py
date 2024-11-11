from enum import Enum, unique

@unique
class LaunchPhase(Enum):
    SUNRISE = "sunrise"
    LANDRUSH = "landrush"
    CLAIMS = "claims"
    GENERAL_AVAILABILITY = "general-availability"
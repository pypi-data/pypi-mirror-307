from enum import Enum, unique

@unique
class AbuseStatus(Enum):
    OPEN = "open"
    IN_PROGRESS = "in-progress"
    RESOLVED = "resolved"
    CLOSED = "closed"
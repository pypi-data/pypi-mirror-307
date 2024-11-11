from enum import Enum, unique

@unique
class NotificationType(Enum):
    EMAIL = "email"
    WEBHOOK = "webhook"
    SMS = "sms"
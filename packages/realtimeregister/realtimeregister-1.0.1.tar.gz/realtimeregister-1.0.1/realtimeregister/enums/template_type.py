from enum import Enum, unique

@unique
class TemplateType(Enum):
    EMAIL = "email"
    SMS = "sms"
    DOCUMENT = "document"
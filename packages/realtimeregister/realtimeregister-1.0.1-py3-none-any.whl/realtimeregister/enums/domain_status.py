from enum import Enum, unique

@unique
class DomainStatus(Enum):
    ACTIVE = "active"
    EXPIRED = "expired"
    INACTIVE = "inactive"
    PENDING = "pending"
    PENDING_DELETE = "pending-delete"
    PENDING_TRANSFER = "pending-transfer"
    PENDING_UPDATE = "pending-update"
    REDEMPTION = "redemption"
    TRANSFER_PROHIBITED = "transfer-prohibited"
    UPDATE_PROHIBITED = "update-prohibited"
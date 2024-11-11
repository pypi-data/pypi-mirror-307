from enum import Enum, unique

@unique
class BillingType(Enum):
    PREPAID = "prepaid"
    POSTPAID = "postpaid"
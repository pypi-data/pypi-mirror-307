from enum import Enum, unique

@unique
class TransactionType(Enum):
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    PAYMENT = "payment"
    REFUND = "refund"
    CREDIT = "credit"
    DEBIT = "debit"
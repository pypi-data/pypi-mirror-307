from dataclasses import dataclass
from typing import Dict, Any, Optional
from datetime import datetime

@dataclass
class DomainStatistics:
    total: int
    active: int
    expired: int
    pending: int
    period_distribution: Dict[str, int]
    tld_distribution: Dict[str, int]
    created_date: datetime

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DomainStatistics':
        return cls(
            total=data['total'],
            active=data['active'],
            expired=data['expired'],
            pending=data['pending'],
            period_distribution=data['periodDistribution'],
            tld_distribution=data['tldDistribution'],
            created_date=datetime.fromisoformat(data['createdDate'])
        )

@dataclass
class BillingStatistics:
    total_amount: float
    paid_amount: float
    outstanding_amount: float
    currency: str
    invoice_distribution: Dict[str, int]
    created_date: datetime

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BillingStatistics':
        return cls(
            total_amount=data['totalAmount'],
            paid_amount=data['paidAmount'],
            outstanding_amount=data['outstandingAmount'],
            currency=data['currency'],
            invoice_distribution=data['invoiceDistribution'],
            created_date=datetime.fromisoformat(data['createdDate'])
        )

@dataclass
class CustomerStatistics:
    total: int
    active: int
    suspended: int
    billing_type_distribution: Dict[str, int]
    created_date: datetime

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CustomerStatistics':
        return cls(
            total=data['total'],
            active=data['active'],
            suspended=data['suspended'],
            billing_type_distribution=data['billingTypeDistribution'],
            created_date=datetime.fromisoformat(data['createdDate'])
        )
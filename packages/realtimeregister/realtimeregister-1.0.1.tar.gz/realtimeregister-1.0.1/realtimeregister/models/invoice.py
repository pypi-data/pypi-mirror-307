from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from datetime import datetime

@dataclass
class Invoice:
    id: str
    number: str
    customer_handle: str
    brand_name: str
    status: str
    currency_code: str
    sub_total: float
    vat_amount: float
    total_amount: float
    paid_amount: Optional[float]
    refunded_amount: Optional[float]
    due_date: datetime
    paid_date: Optional[datetime]
    created_date: datetime
    updated_date: Optional[datetime]
    items: List[Dict[str, Any]]
    properties: Optional[Dict[str, Any]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Invoice':
        return cls(
            id=data['id'],
            number=data['number'],
            customer_handle=data['customerHandle'],
            brand_name=data['brandName'],
            status=data['status'],
            currency_code=data['currencyCode'],
            sub_total=data['subTotal'],
            vat_amount=data['vatAmount'],
            total_amount=data['totalAmount'],
            paid_amount=data.get('paidAmount'),
            refunded_amount=data.get('refundedAmount'),
            due_date=datetime.fromisoformat(data['dueDate']),
            paid_date=datetime.fromisoformat(data['paidDate']) if data.get('paidDate') else None,
            created_date=datetime.fromisoformat(data['createdDate']),
            updated_date=datetime.fromisoformat(data['updatedDate']) if data.get('updatedDate') else None,
            items=data['items'],
            properties=data.get('properties')
        )

    def to_dict(self) -> Dict[str, Any]:
        result = {
            'id': self.id,
            'number': self.number,
            'customerHandle': self.customer_handle,
            'brandName': self.brand_name,
            'status': self.status,
            'currencyCode': self.currency_code,
            'subTotal': self.sub_total,
            'vatAmount': self.vat_amount,
            'totalAmount': self.total_amount,
            'items': self.items,
            'dueDate': self.due_date.isoformat(),
            'createdDate': self.created_date.isoformat()
        }

        if self.paid_amount is not None:
            result['paidAmount'] = self.paid_amount
        if self.refunded_amount is not None:
            result['refundedAmount'] = self.refunded_amount
        if self.paid_date:
            result['paidDate'] = self.paid_date.isoformat()
        if self.updated_date:
            result['updatedDate'] = self.updated_date.isoformat()
        if self.properties:
            result['properties'] = self.properties

        return result
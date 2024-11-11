from dataclasses import dataclass
from typing import Optional, Dict, Any
from datetime import datetime

@dataclass
class Transaction:
    id: str
    customer_handle: str
    brand_name: str
    type: str
    status: str
    currency_code: str
    amount: float
    description: str
    created_date: datetime
    updated_date: Optional[datetime]
    properties: Optional[Dict[str, Any]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Transaction':
        return cls(
            id=data['id'],
            customer_handle=data['customerHandle'],
            brand_name=data['brandName'],
            type=data['type'],
            status=data['status'],
            currency_code=data['currencyCode'],
            amount=data['amount'],
            description=data['description'],
            created_date=datetime.fromisoformat(data['createdDate']),
            updated_date=datetime.fromisoformat(data['updatedDate']) if data.get('updatedDate') else None,
            properties=data.get('properties')
        )

    def to_dict(self) -> Dict[str, Any]:
        result = {
            'id': self.id,
            'customerHandle': self.customer_handle,
            'brandName': self.brand_name,
            'type': self.type,
            'status': self.status,
            'currencyCode': self.currency_code,
            'amount': self.amount,
            'description': self.description,
            'createdDate': self.created_date.isoformat()
        }

        if self.updated_date:
            result['updatedDate'] = self.updated_date.isoformat()
        if self.properties:
            result['properties'] = self.properties

        return result
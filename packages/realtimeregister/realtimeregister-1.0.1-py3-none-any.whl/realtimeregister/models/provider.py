from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from datetime import datetime


@dataclass
class Provider:
    name: str
    type: str
    status: str
    tld: str
    currency_code: str
    prices: Dict[str, Any]
    created_date: datetime
    updated_date: Optional[datetime] = None
    properties: Optional[Dict[str, Any]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Provider':
        return cls(
            name=data['name'],
            type=data['type'],
            status=data['status'],
            tld=data['tld'],
            currency_code=data['currencyCode'],
            prices=data['prices'],
            created_date=datetime.fromisoformat(data['createdDate']),
            updated_date=datetime.fromisoformat(data['updatedDate']) if data.get('updatedDate') else None,
            properties=data.get('properties')
        )

    def to_dict(self) -> Dict[str, Any]:
        result = {
            'name': self.name,
            'type': self.type,
            'status': self.status,
            'tld': self.tld,
            'currencyCode': self.currency_code,
            'prices': self.prices,
            'createdDate': self.created_date.isoformat()
        }

        if self.updated_date:
            result['updatedDate'] = self.updated_date.isoformat()
        if self.properties:
            result['properties'] = self.properties

        return result
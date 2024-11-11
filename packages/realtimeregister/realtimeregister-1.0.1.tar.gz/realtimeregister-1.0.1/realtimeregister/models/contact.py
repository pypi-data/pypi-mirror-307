from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from datetime import datetime

@dataclass
class Contact:
    handle: str
    brand_name: str
    company_name: Optional[str]
    name: str
    email: str
    phone: str
    fax: Optional[str]
    address: Dict[str, str]
    created_date: datetime
    updated_date: Optional[datetime]
    properties: Optional[Dict[str, Any]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Contact':
        return cls(
            handle=data['handle'],
            brand_name=data['brandName'],
            company_name=data.get('companyName'),
            name=data['name'],
            email=data['email'],
            phone=data['phone'],
            fax=data.get('fax'),
            address=data['address'],
            created_date=datetime.fromisoformat(data['createdDate']),
            updated_date=datetime.fromisoformat(data['updatedDate']) if data.get('updatedDate') else None,
            properties=data.get('properties')
        )

    def to_dict(self) -> Dict[str, Any]:
        result = {
            'handle': self.handle,
            'brandName': self.brand_name,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'createdDate': self.created_date.isoformat()
        }
        
        if self.company_name:
            result['companyName'] = self.company_name
        if self.fax:
            result['fax'] = self.fax
        if self.updated_date:
            result['updatedDate'] = self.updated_date.isoformat()
        if self.properties:
            result['properties'] = self.properties
            
        return result
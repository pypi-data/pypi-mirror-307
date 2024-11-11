from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from datetime import datetime

@dataclass
class Brand:
    name: str
    organization: str
    vat_number: Optional[str]
    registration_number: Optional[str]
    email: str
    phone: str
    fax: Optional[str]
    address: Dict[str, str]
    billing_address: Optional[Dict[str, str]]
    created_date: datetime
    updated_date: Optional[datetime]
    properties: Optional[Dict[str, Any]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Brand':
        return cls(
            name=data['name'],
            organization=data['organization'],
            vat_number=data.get('vatNumber'),
            registration_number=data.get('registrationNumber'),
            email=data['email'],
            phone=data['phone'],
            fax=data.get('fax'),
            address=data['address'],
            billing_address=data.get('billingAddress'),
            created_date=datetime.fromisoformat(data['createdDate']),
            updated_date=datetime.fromisoformat(data['updatedDate']) if data.get('updatedDate') else None,
            properties=data.get('properties')
        )

    def to_dict(self) -> Dict[str, Any]:
        result = {
            'name': self.name,
            'organization': self.organization,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'createdDate': self.created_date.isoformat()
        }
        
        if self.vat_number:
            result['vatNumber'] = self.vat_number
        if self.registration_number:
            result['registrationNumber'] = self.registration_number
        if self.fax:
            result['fax'] = self.fax
        if self.billing_address:
            result['billingAddress'] = self.billing_address
        if self.updated_date:
            result['updatedDate'] = self.updated_date.isoformat()
        if self.properties:
            result['properties'] = self.properties
            
        return result
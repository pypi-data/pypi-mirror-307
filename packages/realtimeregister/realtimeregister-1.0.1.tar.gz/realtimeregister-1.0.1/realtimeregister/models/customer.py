from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from datetime import datetime

@dataclass
class Customer:
    handle: str
    brand_name: str
    company_name: Optional[str]
    name: str
    email: str
    phone: str
    fax: Optional[str]
    address: Dict[str, str]
    billing_address: Optional[Dict[str, str]]
    vat_number: Optional[str]
    registration_number: Optional[str]
    language_code: str
    currency_code: str
    billing_type: str
    created_date: datetime
    updated_date: Optional[datetime]
    properties: Optional[Dict[str, Any]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Customer':
        return cls(
            handle=data['handle'],
            brand_name=data['brandName'],
            company_name=data.get('companyName'),
            name=data['name'],
            email=data['email'],
            phone=data['phone'],
            fax=data.get('fax'),
            address=data['address'],
            billing_address=data.get('billingAddress'),
            vat_number=data.get('vatNumber'),
            registration_number=data.get('registrationNumber'),
            language_code=data['languageCode'],
            currency_code=data['currencyCode'],
            billing_type=data['billingType'],
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
            'languageCode': self.language_code,
            'currencyCode': self.currency_code,
            'billingType': self.billing_type,
            'createdDate': self.created_date.isoformat()
        }
        
        if self.company_name:
            result['companyName'] = self.company_name
        if self.fax:
            result['fax'] = self.fax
        if self.billing_address:
            result['billingAddress'] = self.billing_address
        if self.vat_number:
            result['vatNumber'] = self.vat_number
        if self.registration_number:
            result['registrationNumber'] = self.registration_number
        if self.updated_date:
            result['updatedDate'] = self.updated_date.isoformat()
        if self.properties:
            result['properties'] = self.properties
            
        return result
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from datetime import datetime
from .nameserver import Nameserver
from .contact import Contact

@dataclass
class Domain:
    name: str
    brand_name: str
    status: List[str]
    auth_code: str
    registrant: Contact
    admin_contact: Optional[Contact]
    tech_contact: Optional[Contact]
    billing_contact: Optional[Contact]
    nameservers: List[Nameserver]
    created_date: datetime
    updated_date: Optional[datetime]
    expiry_date: datetime
    premium: bool
    zone_published: bool
    dnssec_keys: Optional[List[Dict[str, Any]]]
    properties: Optional[Dict[str, Any]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Domain':
        return cls(
            name=data['name'],
            brand_name=data['brandName'],
            status=data['status'],
            auth_code=data['authCode'],
            registrant=Contact.from_dict(data['registrant']),
            admin_contact=Contact.from_dict(data['adminContact']) if data.get('adminContact') else None,
            tech_contact=Contact.from_dict(data['techContact']) if data.get('techContact') else None,
            billing_contact=Contact.from_dict(data['billingContact']) if data.get('billingContact') else None,
            nameservers=[Nameserver.from_dict(ns) for ns in data['nameservers']],
            created_date=datetime.fromisoformat(data['createdDate']),
            updated_date=datetime.fromisoformat(data['updatedDate']) if data.get('updatedDate') else None,
            expiry_date=datetime.fromisoformat(data['expiryDate']),
            premium=data['premium'],
            zone_published=data['zonePublished'],
            dnssec_keys=data.get('dnssecKeys'),
            properties=data.get('properties')
        )

    def to_dict(self) -> Dict[str, Any]:
        result = {
            'name': self.name,
            'brandName': self.brand_name,
            'status': self.status,
            'authCode': self.auth_code,
            'registrant': self.registrant.to_dict(),
            'nameservers': [ns.to_dict() for ns in self.nameservers],
            'createdDate': self.created_date.isoformat(),
            'expiryDate': self.expiry_date.isoformat(),
            'premium': self.premium,
            'zonePublished': self.zone_published
        }

        if self.admin_contact:
            result['adminContact'] = self.admin_contact.to_dict()
        if self.tech_contact:
            result['techContact'] = self.tech_contact.to_dict()
        if self.billing_contact:
            result['billingContact'] = self.billing_contact.to_dict()
        if self.updated_date:
            result['updatedDate'] = self.updated_date.isoformat()
        if self.dnssec_keys:
            result['dnssecKeys'] = self.dnssec_keys
        if self.properties:
            result['properties'] = self.properties

        return result
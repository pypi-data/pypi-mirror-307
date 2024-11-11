from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from datetime import datetime
from .contact import Contact
from .nameserver import Nameserver

@dataclass
class Transfer:
    domain: str
    status: str
    registrar: str
    auth_code: str
    period: Optional[int]
    registrant: Optional[Contact]
    admin_contact: Optional[Contact]
    tech_contact: Optional[Contact]
    billing_contact: Optional[Contact]
    nameservers: Optional[List[Nameserver]]
    created_date: datetime
    updated_date: Optional[datetime]
    expiry_date: Optional[datetime]
    properties: Optional[Dict[str, Any]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Transfer':
        return cls(
            domain=data['domain'],
            status=data['status'],
            registrar=data['registrar'],
            auth_code=data['authCode'],
            period=data.get('period'),
            registrant=Contact.from_dict(data['registrant']) if data.get('registrant') else None,
            admin_contact=Contact.from_dict(data['adminContact']) if data.get('adminContact') else None,
            tech_contact=Contact.from_dict(data['techContact']) if data.get('techContact') else None,
            billing_contact=Contact.from_dict(data['billingContact']) if data.get('billingContact') else None,
            nameservers=[Nameserver.from_dict(ns) for ns in data['nameservers']] if data.get('nameservers') else None,
            created_date=datetime.fromisoformat(data['createdDate']),
            updated_date=datetime.fromisoformat(data['updatedDate']) if data.get('updatedDate') else None,
            expiry_date=datetime.fromisoformat(data['expiryDate']) if data.get('expiryDate') else None,
            properties=data.get('properties')
        )

    def to_dict(self) -> Dict[str, Any]:
        result = {
            'domain': self.domain,
            'status': self.status,
            'registrar': self.registrar,
            'authCode': self.auth_code,
            'createdDate': self.created_date.isoformat()
        }

        if self.period:
            result['period'] = self.period
        if self.registrant:
            result['registrant'] = self.registrant.to_dict()
        if self.admin_contact:
            result['adminContact'] = self.admin_contact.to_dict()
        if self.tech_contact:
            result['techContact'] = self.tech_contact.to_dict()
        if self.billing_contact:
            result['billingContact'] = self.billing_contact.to_dict()
        if self.nameservers:
            result['nameservers'] = [ns.to_dict() for ns in self.nameservers]
        if self.updated_date:
            result['updatedDate'] = self.updated_date.isoformat()
        if self.expiry_date:
            result['expiryDate'] = self.expiry_date.isoformat()
        if self.properties:
            result['properties'] = self.properties

        return result
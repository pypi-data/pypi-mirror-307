from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from datetime import datetime

@dataclass
class Certificate:
    id: str
    domain: str
    type: str
    status: str
    validation_method: str
    validation_status: str
    created_date: datetime
    expiry_date: datetime
    updated_date: Optional[datetime] = None
    properties: Optional[Dict[str, Any]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Certificate':
        return cls(
            id=data['id'],
            domain=data['domain'],
            type=data['type'],
            status=data['status'],
            validation_method=data['validationMethod'],
            validation_status=data['validationStatus'],
            created_date=datetime.fromisoformat(data['createdDate']),
            expiry_date=datetime.fromisoformat(data['expiryDate']),
            updated_date=datetime.fromisoformat(data['updatedDate']) if data.get('updatedDate') else None,
            properties=data.get('properties')
        )

    def to_dict(self) -> Dict[str, Any]:
        result = {
            'id': self.id,
            'domain': self.domain,
            'type': self.type,
            'status': self.status,
            'validationMethod': self.validation_method,
            'validationStatus': self.validation_status,
            'createdDate': self.created_date.isoformat(),
            'expiryDate': self.expiry_date.isoformat()
        }
        
        if self.updated_date:
            result['updatedDate'] = self.updated_date.isoformat()
        if self.properties:
            result['properties'] = self.properties
            
        return result
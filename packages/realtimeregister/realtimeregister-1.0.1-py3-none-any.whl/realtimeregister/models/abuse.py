from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from datetime import datetime

@dataclass
class AbuseReport:
    id: str
    domain: str
    reporter_name: str
    reporter_email: str
    message: str
    status: str
    evidence: Optional[List[Dict[str, Any]]]
    notes: Optional[str]
    created_date: datetime
    updated_date: Optional[datetime]
    properties: Optional[Dict[str, Any]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AbuseReport':
        return cls(
            id=data['id'],
            domain=data['domain'],
            reporter_name=data['reporterName'],
            reporter_email=data['reporterEmail'],
            message=data['message'],
            status=data['status'],
            evidence=data.get('evidence'),
            notes=data.get('notes'),
            created_date=datetime.fromisoformat(data['createdDate']),
            updated_date=datetime.fromisoformat(data['updatedDate']) if data.get('updatedDate') else None,
            properties=data.get('properties')
        )

    def to_dict(self) -> Dict[str, Any]:
        result = {
            'id': self.id,
            'domain': self.domain,
            'reporterName': self.reporter_name,
            'reporterEmail': self.reporter_email,
            'message': self.message,
            'status': self.status,
            'createdDate': self.created_date.isoformat()
        }

        if self.evidence:
            result['evidence'] = self.evidence
        if self.notes:
            result['notes'] = self.notes
        if self.updated_date:
            result['updatedDate'] = self.updated_date.isoformat()
        if self.properties:
            result['properties'] = self.properties

        return result
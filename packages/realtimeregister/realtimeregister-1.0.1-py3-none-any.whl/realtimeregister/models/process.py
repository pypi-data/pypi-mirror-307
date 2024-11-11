from dataclasses import dataclass
from typing import Optional, Dict, Any
from datetime import datetime

@dataclass
class Process:
    id: str
    type: str
    status: str
    entity_type: str
    entity_id: str
    progress: int
    message: Optional[str]
    error: Optional[str]
    created_date: datetime
    updated_date: Optional[datetime]
    completed_date: Optional[datetime]
    properties: Optional[Dict[str, Any]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Process':
        return cls(
            id=data['id'],
            type=data['type'],
            status=data['status'],
            entity_type=data['entityType'],
            entity_id=data['entityId'],
            progress=data['progress'],
            message=data.get('message'),
            error=data.get('error'),
            created_date=datetime.fromisoformat(data['createdDate']),
            updated_date=datetime.fromisoformat(data['updatedDate']) if data.get('updatedDate') else None,
            completed_date=datetime.fromisoformat(data['completedDate']) if data.get('completedDate') else None,
            properties=data.get('properties')
        )

    def to_dict(self) -> Dict[str, Any]:
        result = {
            'id': self.id,
            'type': self.type,
            'status': self.status,
            'entityType': self.entity_type,
            'entityId': self.entity_id,
            'progress': self.progress,
            'createdDate': self.created_date.isoformat()
        }

        if self.message:
            result['message'] = self.message
        if self.error:
            result['error'] = self.error
        if self.updated_date:
            result['updatedDate'] = self.updated_date.isoformat()
        if self.completed_date:
            result['completedDate'] = self.completed_date.isoformat()
        if self.properties:
            result['properties'] = self.properties

        return result
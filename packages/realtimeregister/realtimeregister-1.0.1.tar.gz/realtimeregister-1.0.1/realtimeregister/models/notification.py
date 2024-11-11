from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from datetime import datetime

@dataclass
class Notification:
    id: str
    type: str
    destination: str
    events: List[str]
    enabled: bool
    created_date: datetime
    updated_date: Optional[datetime]
    properties: Optional[Dict[str, Any]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Notification':
        return cls(
            id=data['id'],
            type=data['type'],
            destination=data['destination'],
            events=data['events'],
            enabled=data['enabled'],
            created_date=datetime.fromisoformat(data['createdDate']),
            updated_date=datetime.fromisoformat(data['updatedDate']) if data.get('updatedDate') else None,
            properties=data.get('properties')
        )

    def to_dict(self) -> Dict[str, Any]:
        result = {
            'id': self.id,
            'type': self.type,
            'destination': self.destination,
            'events': self.events,
            'enabled': self.enabled,
            'createdDate': self.created_date.isoformat()
        }

        if self.updated_date:
            result['updatedDate'] = self.updated_date.isoformat()
        if self.properties:
            result['properties'] = self.properties

        return result
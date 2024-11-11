from dataclasses import dataclass
from typing import Optional, Dict, Any
from datetime import datetime

@dataclass
class Template:
    name: str
    type: str
    content: str
    subject: Optional[str]
    description: Optional[str]
    created_date: datetime
    updated_date: Optional[datetime]
    properties: Optional[Dict[str, Any]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Template':
        return cls(
            name=data['name'],
            type=data['type'],
            content=data['content'],
            subject=data.get('subject'),
            description=data.get('description'),
            created_date=datetime.fromisoformat(data['createdDate']),
            updated_date=datetime.fromisoformat(data['updatedDate']) if data.get('updatedDate') else None,
            properties=data.get('properties')
        )

    def to_dict(self) -> Dict[str, Any]:
        result = {
            'name': self.name,
            'type': self.type,
            'content': self.content,
            'createdDate': self.created_date.isoformat()
        }

        if self.subject:
            result['subject'] = self.subject
        if self.description:
            result['description'] = self.description
        if self.updated_date:
            result['updatedDate'] = self.updated_date.isoformat()
        if self.properties:
            result['properties'] = self.properties

        return result
from dataclasses import dataclass
from typing import Optional, Dict, Any, Union
from datetime import datetime

@dataclass
class DNSRecord:
    name: str
    type: str
    ttl: int
    content: Union[str, Dict[str, Any]]
    created_date: datetime
    updated_date: Optional[datetime] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DNSRecord':
        return cls(
            name=data['name'],
            type=data['type'],
            ttl=data['ttl'],
            content=data['content'],
            created_date=datetime.fromisoformat(data['createdDate']),
            updated_date=datetime.fromisoformat(data['updatedDate']) if data.get('updatedDate') else None
        )

    def to_dict(self) -> Dict[str, Any]:
        result = {
            'name': self.name,
            'type': self.type,
            'ttl': self.ttl,
            'content': self.content,
            'createdDate': self.created_date.isoformat()
        }
        
        if self.updated_date:
            result['updatedDate'] = self.updated_date.isoformat()
            
        return result
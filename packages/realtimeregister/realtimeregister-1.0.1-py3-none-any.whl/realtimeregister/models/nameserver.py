from dataclasses import dataclass
from typing import Optional, List, Dict, Any

@dataclass
class Nameserver:
    hostname: str
    ip_addresses: Optional[List[str]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Nameserver':
        return cls(
            hostname=data['hostname'],
            ip_addresses=data.get('ipAddresses')
        )

    def to_dict(self) -> Dict[str, Any]:
        result = {'hostname': self.hostname}
        if self.ip_addresses:
            result['ipAddresses'] = self.ip_addresses
        return result
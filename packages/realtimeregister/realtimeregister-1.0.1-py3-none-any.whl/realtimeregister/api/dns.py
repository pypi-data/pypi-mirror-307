from typing import Dict, Any, List, Optional
from ..models.dns_record import DNSRecord

class DNSApi:
    def __init__(self, client):
        self.client = client

    def list_records(self, domain: str, page: int = 1, limit: int = 25) -> Dict[str, Any]:
        """List DNS records for a domain"""
        return self.client._request('GET', f'domains/{domain}/dns', params={'page': page, 'limit': limit})

    def get_record(self, domain: str, name: str, type: str) -> DNSRecord:
        """Get DNS record details"""
        response = self.client._request('GET', f'domains/{domain}/dns/{name}/{type}')
        return DNSRecord.from_dict(response)

    def create_record(
        self,
        domain: str,
        name: str,
        type: str,
        ttl: int,
        content: Dict[str, Any]
    ) -> DNSRecord:
        """Create a new DNS record"""
        data = {
            'ttl': ttl,
            'content': content
        }

        response = self.client._request('POST', f'domains/{domain}/dns/{name}/{type}', data=data)
        return DNSRecord.from_dict(response)

    def update_record(
        self,
        domain: str,
        name: str,
        type: str,
        ttl: Optional[int] = None,
        content: Optional[Dict[str, Any]] = None
    ) -> DNSRecord:
        """Update DNS record"""
        data = {}
        if ttl is not None:
            data['ttl'] = ttl
        if content is not None:
            data['content'] = content

        response = self.client._request('PUT', f'domains/{domain}/dns/{name}/{type}', data=data)
        return DNSRecord.from_dict(response)

    def delete_record(self, domain: str, name: str, type: str) -> None:
        """Delete DNS record"""
        self.client._request('DELETE', f'domains/{domain}/dns/{name}/{type}')

    def query_records(
        self,
        domain: str,
        query: str,
        type: Optional[str] = None,
        page: int = 1,
        limit: int = 25
    ) -> Dict[str, Any]:
        """Search DNS records"""
        params = {
            'q': query,
            'page': page,
            'limit': limit
        }
        if type:
            params['type'] = type
            
        return self.client._request('GET', f'domains/{domain}/dns/query', params=params)
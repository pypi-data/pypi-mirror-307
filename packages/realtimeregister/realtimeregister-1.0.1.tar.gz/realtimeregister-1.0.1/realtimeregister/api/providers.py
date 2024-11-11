from typing import Dict, Any, List, Optional
from ..models.provider import Provider

class ProvidersApi:
    def __init__(self, client):
        self.client = client

    def list(self, page: int = 1, limit: int = 25) -> Dict[str, Any]:
        """List providers"""
        return self.client._request('GET', 'providers', params={'page': page, 'limit': limit})

    def get(self, name: str) -> Provider:
        """Get provider details"""
        response = self.client._request('GET', f'providers/{name}')
        return Provider.from_dict(response)

    def create(
        self,
        name: str,
        type: str,
        status: str,
        tld: str,
        currency_code: str,
        prices: Dict[str, Any],
        properties: Optional[Dict[str, Any]] = None
    ) -> Provider:
        """Create a new provider"""
        data = {
            'type': type,
            'status': status,
            'tld': tld,
            'currencyCode': currency_code,
            'prices': prices
        }

        if properties:
            data['properties'] = properties

        response = self.client._request('POST', f'providers/{name}', data=data)
        return Provider.from_dict(response)

    def update(
        self,
        name: str,
        type: Optional[str] = None,
        status: Optional[str] = None,
        tld: Optional[str] = None,
        currency_code: Optional[str] = None,
        prices: Optional[Dict[str, Any]] = None,
        properties: Optional[Dict[str, Any]] = None
    ) -> Provider:
        """Update provider details"""
        data = {}
        if type:
            data['type'] = type
        if status:
            data['status'] = status
        if tld:
            data['tld'] = tld
        if currency_code:
            data['currencyCode'] = currency_code
        if prices:
            data['prices'] = prices
        if properties:
            data['properties'] = properties

        response = self.client._request('PUT', f'providers/{name}', data=data)
        return Provider.from_dict(response)

    def delete(self, name: str) -> None:
        """Delete a provider"""
        self.client._request('DELETE', f'providers/{name}')

    def query(
        self,
        query: str,
        type: Optional[str] = None,
        tld: Optional[str] = None,
        page: int = 1,
        limit: int = 25
    ) -> Dict[str, Any]:
        """Search providers"""
        params = {
            'q': query,
            'page': page,
            'limit': limit
        }
        if type:
            params['type'] = type
        if tld:
            params['tld'] = tld
            
        return self.client._request('GET', 'providers/query', params=params)
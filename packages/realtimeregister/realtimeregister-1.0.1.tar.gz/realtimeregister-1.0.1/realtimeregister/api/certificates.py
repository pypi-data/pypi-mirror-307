from typing import Dict, Any, List, Optional
from ..models.certificate import Certificate

class CertificatesApi:
    def __init__(self, client):
        self.client = client

    def list(self, page: int = 1, limit: int = 25) -> Dict[str, Any]:
        """List SSL certificates"""
        return self.client._request('GET', 'certificates', params={'page': page, 'limit': limit})

    def get(self, id: str) -> Certificate:
        """Get certificate details"""
        response = self.client._request('GET', f'certificates/{id}')
        return Certificate.from_dict(response)

    def order(
        self,
        domain: str,
        type: str,
        validation_method: str,
        period: int = 1,
        properties: Optional[Dict[str, Any]] = None
    ) -> Certificate:
        """Order a new SSL certificate"""
        data = {
            'domain': domain,
            'type': type,
            'validationMethod': validation_method,
            'period': period
        }

        if properties:
            data['properties'] = properties

        response = self.client._request('POST', 'certificates', data=data)
        return Certificate.from_dict(response)

    def cancel(self, id: str) -> None:
        """Cancel a certificate order"""
        self.client._request('DELETE', f'certificates/{id}')

    def reissue(
        self,
        id: str,
        validation_method: Optional[str] = None,
        properties: Optional[Dict[str, Any]] = None
    ) -> Certificate:
        """Reissue an existing certificate"""
        data = {}
        if validation_method:
            data['validationMethod'] = validation_method
        if properties:
            data['properties'] = properties

        response = self.client._request('POST', f'certificates/{id}/reissue', data=data)
        return Certificate.from_dict(response)

    def query(
        self,
        query: str,
        type: Optional[str] = None,
        status: Optional[str] = None,
        page: int = 1,
        limit: int = 25
    ) -> Dict[str, Any]:
        """Search certificates"""
        params = {
            'q': query,
            'page': page,
            'limit': limit
        }
        if type:
            params['type'] = type
        if status:
            params['status'] = status
            
        return self.client._request('GET', 'certificates/query', params=params)
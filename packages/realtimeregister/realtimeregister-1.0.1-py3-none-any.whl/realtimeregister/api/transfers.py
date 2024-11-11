from typing import Dict, Any, List, Optional
from ..models.transfer import Transfer

class TransfersApi:
    def __init__(self, client):
        self.client = client

    def list(self, page: int = 1, limit: int = 25) -> Dict[str, Any]:
        """List domain transfers"""
        return self.client._request('GET', 'transfers', params={'page': page, 'limit': limit})

    def get(self, domain: str) -> Transfer:
        """Get transfer details"""
        response = self.client._request('GET', f'transfers/{domain}')
        return Transfer.from_dict(response)

    def request(
        self,
        domain: str,
        auth_code: str,
        period: Optional[int] = None,
        registrant: Optional[Dict[str, Any]] = None,
        admin_contact: Optional[Dict[str, Any]] = None,
        tech_contact: Optional[Dict[str, Any]] = None,
        billing_contact: Optional[Dict[str, Any]] = None,
        nameservers: Optional[List[Dict[str, Any]]] = None,
        properties: Optional[Dict[str, Any]] = None
    ) -> Transfer:
        """Request a domain transfer"""
        data = {'authCode': auth_code}

        if period:
            data['period'] = period
        if registrant:
            data['registrant'] = registrant
        if admin_contact:
            data['adminContact'] = admin_contact
        if tech_contact:
            data['techContact'] = tech_contact
        if billing_contact:
            data['billingContact'] = billing_contact
        if nameservers:
            data['nameservers'] = nameservers
        if properties:
            data['properties'] = properties

        response = self.client._request('POST', f'transfers/{domain}', data=data)
        return Transfer.from_dict(response)

    def cancel(self, domain: str) -> None:
        """Cancel a domain transfer"""
        self.client._request('DELETE', f'transfers/{domain}')

    def approve(self, domain: str) -> Transfer:
        """Approve a domain transfer"""
        response = self.client._request('POST', f'transfers/{domain}/approve')
        return Transfer.from_dict(response)

    def reject(self, domain: str, reason: str) -> Transfer:
        """Reject a domain transfer"""
        response = self.client._request('POST', f'transfers/{domain}/reject', data={'reason': reason})
        return Transfer.from_dict(response)

    def query(
        self,
        query: str,
        status: Optional[str] = None,
        page: int = 1,
        limit: int = 25
    ) -> Dict[str, Any]:
        """Search transfers"""
        params = {
            'q': query,
            'page': page,
            'limit': limit
        }
        if status:
            params['status'] = status
            
        return self.client._request('GET', 'transfers/query', params=params)
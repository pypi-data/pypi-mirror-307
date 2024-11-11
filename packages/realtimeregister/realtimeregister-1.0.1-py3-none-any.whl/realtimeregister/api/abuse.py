from typing import Dict, Any, List, Optional
from ..models.abuse import AbuseReport

class AbuseApi:
    def __init__(self, client):
        self.client = client

    def list(self, page: int = 1, limit: int = 25) -> Dict[str, Any]:
        """List abuse reports"""
        return self.client._request('GET', 'abuse', params={'page': page, 'limit': limit})

    def get(self, id: str) -> AbuseReport:
        """Get abuse report details"""
        response = self.client._request('GET', f'abuse/{id}')
        return AbuseReport.from_dict(response)

    def create(
        self,
        domain: str,
        reporter_name: str,
        reporter_email: str,
        message: str,
        evidence: Optional[List[Dict[str, Any]]] = None,
        properties: Optional[Dict[str, Any]] = None
    ) -> AbuseReport:
        """Create a new abuse report"""
        data = {
            'domain': domain,
            'reporterName': reporter_name,
            'reporterEmail': reporter_email,
            'message': message
        }

        if evidence:
            data['evidence'] = evidence
        if properties:
            data['properties'] = properties

        response = self.client._request('POST', 'abuse', data=data)
        return AbuseReport.from_dict(response)

    def update(
        self,
        id: str,
        status: Optional[str] = None,
        notes: Optional[str] = None,
        properties: Optional[Dict[str, Any]] = None
    ) -> AbuseReport:
        """Update abuse report"""
        data = {}
        if status:
            data['status'] = status
        if notes:
            data['notes'] = notes
        if properties:
            data['properties'] = properties

        response = self.client._request('PUT', f'abuse/{id}', data=data)
        return AbuseReport.from_dict(response)

    def delete(self, id: str) -> None:
        """Delete an abuse report"""
        self.client._request('DELETE', f'abuse/{id}')

    def query(
        self,
        query: str,
        status: Optional[str] = None,
        domain: Optional[str] = None,
        page: int = 1,
        limit: int = 25
    ) -> Dict[str, Any]:
        """Search abuse reports"""
        params = {
            'q': query,
            'page': page,
            'limit': limit
        }
        if status:
            params['status'] = status
        if domain:
            params['domain'] = domain
            
        return self.client._request('GET', 'abuse/query', params=params)
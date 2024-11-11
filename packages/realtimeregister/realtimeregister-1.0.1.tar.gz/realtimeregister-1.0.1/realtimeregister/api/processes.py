from typing import Dict, Any, List, Optional
from ..models.process import Process

class ProcessesApi:
    def __init__(self, client):
        self.client = client

    def list(self, page: int = 1, limit: int = 25) -> Dict[str, Any]:
        """List processes"""
        return self.client._request('GET', 'processes', params={'page': page, 'limit': limit})

    def get(self, id: str) -> Process:
        """Get process details"""
        response = self.client._request('GET', f'processes/{id}')
        return Process.from_dict(response)

    def query(
        self,
        query: str,
        status: Optional[str] = None,
        type: Optional[str] = None,
        page: int = 1,
        limit: int = 25
    ) -> Dict[str, Any]:
        """Search processes"""
        params = {
            'q': query,
            'page': page,
            'limit': limit
        }
        if status:
            params['status'] = status
        if type:
            params['type'] = type
            
        return self.client._request('GET', 'processes/query', params=params)
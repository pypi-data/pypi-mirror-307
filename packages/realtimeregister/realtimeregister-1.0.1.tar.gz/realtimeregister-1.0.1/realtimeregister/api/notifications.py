from typing import Dict, Any, List, Optional
from ..models.notification import Notification

class NotificationsApi:
    def __init__(self, client):
        self.client = client

    def list(self, page: int = 1, limit: int = 25) -> Dict[str, Any]:
        """List notifications"""
        return self.client._request('GET', 'notifications', params={'page': page, 'limit': limit})

    def get(self, id: str) -> Notification:
        """Get notification details"""
        response = self.client._request('GET', f'notifications/{id}')
        return Notification.from_dict(response)

    def create(
        self,
        type: str,
        destination: str,
        events: List[str],
        enabled: bool = True,
        properties: Optional[Dict[str, Any]] = None
    ) -> Notification:
        """Create a new notification"""
        data = {
            'type': type,
            'destination': destination,
            'events': events,
            'enabled': enabled
        }

        if properties:
            data['properties'] = properties

        response = self.client._request('POST', 'notifications', data=data)
        return Notification.from_dict(response)

    def update(
        self,
        id: str,
        type: Optional[str] = None,
        destination: Optional[str] = None,
        events: Optional[List[str]] = None,
        enabled: Optional[bool] = None,
        properties: Optional[Dict[str, Any]] = None
    ) -> Notification:
        """Update notification settings"""
        data = {}
        if type:
            data['type'] = type
        if destination:
            data['destination'] = destination
        if events:
            data['events'] = events
        if enabled is not None:
            data['enabled'] = enabled
        if properties:
            data['properties'] = properties

        response = self.client._request('PUT', f'notifications/{id}', data=data)
        return Notification.from_dict(response)

    def delete(self, id: str) -> None:
        """Delete a notification"""
        self.client._request('DELETE', f'notifications/{id}')

    def test(self, id: str) -> bool:
        """Test a notification configuration"""
        response = self.client._request('POST', f'notifications/{id}/test')
        return response.get('success', False)

    def query(
        self,
        query: str,
        type: Optional[str] = None,
        enabled: Optional[bool] = None,
        page: int = 1,
        limit: int = 25
    ) -> Dict[str, Any]:
        """Search notifications"""
        params = {
            'q': query,
            'page': page,
            'limit': limit
        }
        if type:
            params['type'] = type
        if enabled is not None:
            params['enabled'] = enabled
            
        return self.client._request('GET', 'notifications/query', params=params)
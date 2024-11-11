from typing import Dict, Any, List, Optional
from ..models.template import Template

class TemplatesApi:
    def __init__(self, client):
        self.client = client

    def list(self, page: int = 1, limit: int = 25) -> Dict[str, Any]:
        """List templates"""
        return self.client._request('GET', 'templates', params={'page': page, 'limit': limit})

    def get(self, name: str) -> Template:
        """Get template details"""
        response = self.client._request('GET', f'templates/{name}')
        return Template.from_dict(response)

    def create(
        self,
        name: str,
        type: str,
        content: str,
        subject: Optional[str] = None,
        description: Optional[str] = None,
        properties: Optional[Dict[str, Any]] = None
    ) -> Template:
        """Create a new template"""
        data = {
            'type': type,
            'content': content
        }

        if subject:
            data['subject'] = subject
        if description:
            data['description'] = description
        if properties:
            data['properties'] = properties

        response = self.client._request('POST', f'templates/{name}', data=data)
        return Template.from_dict(response)

    def update(
        self,
        name: str,
        type: Optional[str] = None,
        content: Optional[str] = None,
        subject: Optional[str] = None,
        description: Optional[str] = None,
        properties: Optional[Dict[str, Any]] = None
    ) -> Template:
        """Update template details"""
        data = {}
        if type:
            data['type'] = type
        if content:
            data['content'] = content
        if subject:
            data['subject'] = subject
        if description:
            data['description'] = description
        if properties:
            data['properties'] = properties

        response = self.client._request('PUT', f'templates/{name}', data=data)
        return Template.from_dict(response)

    def delete(self, name: str) -> None:
        """Delete a template"""
        self.client._request('DELETE', f'templates/{name}')

    def query(
        self,
        query: str,
        type: Optional[str] = None,
        page: int = 1,
        limit: int = 25
    ) -> Dict[str, Any]:
        """Search templates"""
        params = {
            'q': query,
            'page': page,
            'limit': limit
        }
        if type:
            params['type'] = type
            
        return self.client._request('GET', 'templates/query', params=params)

    def preview(
        self,
        name: str,
        data: Dict[str, Any]
    ) -> str:
        """Preview a template with sample data"""
        response = self.client._request('POST', f'templates/{name}/preview', data=data)
        return response['content']
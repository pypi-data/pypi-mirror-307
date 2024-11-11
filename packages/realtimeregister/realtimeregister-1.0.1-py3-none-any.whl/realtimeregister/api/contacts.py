from typing import Dict, Any, List, Optional
from ..models.contact import Contact

class ContactsApi:
    def __init__(self, client):
        self.client = client

    def list(self, page: int = 1, limit: int = 25) -> Dict[str, Any]:
        """List contacts"""
        return self.client._request('GET', 'contacts', params={'page': page, 'limit': limit})

    def get(self, handle: str) -> Contact:
        """Get contact details"""
        response = self.client._request('GET', f'contacts/{handle}')
        return Contact.from_dict(response)

    def create(
        self,
        handle: str,
        brand_name: str,
        name: str,
        email: str,
        phone: str,
        address: Dict[str, str],
        company_name: Optional[str] = None,
        fax: Optional[str] = None,
        properties: Optional[Dict[str, Any]] = None
    ) -> Contact:
        """Create a new contact"""
        data = {
            'brandName': brand_name,
            'name': name,
            'email': email,
            'phone': phone,
            'address': address
        }

        if company_name:
            data['companyName'] = company_name
        if fax:
            data['fax'] = fax
        if properties:
            data['properties'] = properties

        response = self.client._request('POST', f'contacts/{handle}', data=data)
        return Contact.from_dict(response)

    def update(
        self,
        handle: str,
        name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        address: Optional[Dict[str, str]] = None,
        company_name: Optional[str] = None,
        fax: Optional[str] = None,
        properties: Optional[Dict[str, Any]] = None
    ) -> Contact:
        """Update contact details"""
        data = {}
        if name:
            data['name'] = name
        if email:
            data['email'] = email
        if phone:
            data['phone'] = phone
        if address:
            data['address'] = address
        if company_name:
            data['companyName'] = company_name
        if fax:
            data['fax'] = fax
        if properties:
            data['properties'] = properties

        response = self.client._request('PUT', f'contacts/{handle}', data=data)
        return Contact.from_dict(response)

    def delete(self, handle: str) -> None:
        """Delete a contact"""
        self.client._request('DELETE', f'contacts/{handle}')

    def query(
        self,
        query: str,
        brand_name: Optional[str] = None,
        page: int = 1,
        limit: int = 25
    ) -> Dict[str, Any]:
        """Search contacts"""
        params = {
            'q': query,
            'page': page,
            'limit': limit
        }
        if brand_name:
            params['brandName'] = brand_name
            
        return self.client._request('GET', 'contacts/query', params=params)
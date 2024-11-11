from typing import Dict, Any, List, Optional
from ..models.brand import Brand

class BrandsApi:
    def __init__(self, client):
        self.client = client

    def list(self, page: int = 1, limit: int = 25) -> Dict[str, Any]:
        """List brands"""
        return self.client._request('GET', 'brands', params={'page': page, 'limit': limit})

    def get(self, name: str) -> Brand:
        """Get brand details"""
        response = self.client._request('GET', f'brands/{name}')
        return Brand.from_dict(response)

    def create(
        self,
        name: str,
        organization: str,
        email: str,
        phone: str,
        address: Dict[str, str],
        vat_number: Optional[str] = None,
        registration_number: Optional[str] = None,
        fax: Optional[str] = None,
        billing_address: Optional[Dict[str, str]] = None,
        properties: Optional[Dict[str, Any]] = None
    ) -> Brand:
        """Create a new brand"""
        data = {
            'organization': organization,
            'email': email,
            'phone': phone,
            'address': address
        }

        if vat_number:
            data['vatNumber'] = vat_number
        if registration_number:
            data['registrationNumber'] = registration_number
        if fax:
            data['fax'] = fax
        if billing_address:
            data['billingAddress'] = billing_address
        if properties:
            data['properties'] = properties

        response = self.client._request('POST', f'brands/{name}', data=data)
        return Brand.from_dict(response)

    def update(
        self,
        name: str,
        organization: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        address: Optional[Dict[str, str]] = None,
        vat_number: Optional[str] = None,
        registration_number: Optional[str] = None,
        fax: Optional[str] = None,
        billing_address: Optional[Dict[str, str]] = None,
        properties: Optional[Dict[str, Any]] = None
    ) -> Brand:
        """Update brand details"""
        data = {}
        if organization:
            data['organization'] = organization
        if email:
            data['email'] = email
        if phone:
            data['phone'] = phone
        if address:
            data['address'] = address
        if vat_number:
            data['vatNumber'] = vat_number
        if registration_number:
            data['registrationNumber'] = registration_number
        if fax:
            data['fax'] = fax
        if billing_address:
            data['billingAddress'] = billing_address
        if properties:
            data['properties'] = properties

        response = self.client._request('PUT', f'brands/{name}', data=data)
        return Brand.from_dict(response)

    def delete(self, name: str) -> None:
        """Delete a brand"""
        self.client._request('DELETE', f'brands/{name}')

    def query(
        self,
        query: str,
        page: int = 1,
        limit: int = 25
    ) -> Dict[str, Any]:
        """Search brands"""
        params = {
            'q': query,
            'page': page,
            'limit': limit
        }
        return self.client._request('GET', 'brands/query', params=params)
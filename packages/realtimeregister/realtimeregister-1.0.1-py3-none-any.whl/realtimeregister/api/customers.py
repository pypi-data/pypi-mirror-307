from typing import Dict, Any, List, Optional
from ..models.customer import Customer
from ..models.price import Pricelist


class CustomersApi:
    def __init__(self, client):
        self.client = client

    def list(self, page: int = 1, limit: int = 25) -> Dict[str, Any]:
        """List customers"""
        return self.client._request('GET', 'customers', params={'page': page, 'limit': limit})

    def get(self, handle: str) -> Customer:
        """Get customer details"""
        response = self.client._request('GET', f'customers/{handle}')
        return Customer.from_dict(response)

    def get_pricelist(self, customer: str) -> Pricelist:
        """
        Get customer pricelist

        Args:
            customer: Customer handle to get pricelist for
        """
        response = self.client._request('GET', f'customers/{customer}/pricelist')
        return Pricelist.from_dict(response)

    def create(
            self,
            handle: str,
            brand_name: str,
            name: str,
            email: str,
            phone: str,
            address: Dict[str, str],
            language_code: str,
            currency_code: str,
            billing_type: str,
            company_name: Optional[str] = None,
            fax: Optional[str] = None,
            billing_address: Optional[Dict[str, str]] = None,
            vat_number: Optional[str] = None,
            registration_number: Optional[str] = None,
            properties: Optional[Dict[str, Any]] = None
    ) -> Customer:
        """Create a new customer"""
        data = {
            'brandName': brand_name,
            'name': name,
            'email': email,
            'phone': phone,
            'address': address,
            'languageCode': language_code,
            'currencyCode': currency_code,
            'billingType': billing_type
        }

        if company_name:
            data['companyName'] = company_name
        if fax:
            data['fax'] = fax
        if billing_address:
            data['billingAddress'] = billing_address
        if vat_number:
            data['vatNumber'] = vat_number
        if registration_number:
            data['registrationNumber'] = registration_number
        if properties:
            data['properties'] = properties

        response = self.client._request('POST', f'customers/{handle}', data=data)
        return Customer.from_dict(response)

    def update(
            self,
            handle: str,
            name: Optional[str] = None,
            email: Optional[str] = None,
            phone: Optional[str] = None,
            address: Optional[Dict[str, str]] = None,
            language_code: Optional[str] = None,
            currency_code: Optional[str] = None,
            billing_type: Optional[str] = None,
            company_name: Optional[str] = None,
            fax: Optional[str] = None,
            billing_address: Optional[Dict[str, str]] = None,
            vat_number: Optional[str] = None,
            registration_number: Optional[str] = None,
            properties: Optional[Dict[str, Any]] = None
    ) -> Customer:
        """Update customer details"""
        data = {}
        if name:
            data['name'] = name
        if email:
            data['email'] = email
        if phone:
            data['phone'] = phone
        if address:
            data['address'] = address
        if language_code:
            data['languageCode'] = language_code
        if currency_code:
            data['currencyCode'] = currency_code
        if billing_type:
            data['billingType'] = billing_type
        if company_name:
            data['companyName'] = company_name
        if fax:
            data['fax'] = fax
        if billing_address:
            data['billingAddress'] = billing_address
        if vat_number:
            data['vatNumber'] = vat_number
        if registration_number:
            data['registrationNumber'] = registration_number
        if properties:
            data['properties'] = properties

        response = self.client._request('PUT', f'customers/{handle}', data=data)
        return Customer.from_dict(response)

    def delete(self, handle: str) -> None:
        """Delete a customer"""
        self.client._request('DELETE', f'customers/{handle}')

    def query(
            self,
            query: str,
            brand_name: Optional[str] = None,
            page: int = 1,
            limit: int = 25
    ) -> Dict[str, Any]:
        """Search customers"""
        params = {
            'q': query,
            'page': page,
            'limit': limit
        }
        if brand_name:
            params['brandName'] = brand_name

        return self.client._request('GET', 'customers/query', params=params)
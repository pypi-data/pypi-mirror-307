from typing import Dict, Any, List, Optional
from ..models.domain import Domain


class DomainsApi:
    def __init__(self, client):
        self.client = client

    def list(
            self,
            limit: int = 50,
            offset: int = 0,
            sort: Optional[str] = None,
            order: Optional[str] = None,
            **filters: Any
    ) -> Dict[str, Any]:
        """
        List domains with optional filtering and sorting

        Args:
            limit: Number of results per page (default: 50)
            offset: Starting position (default: 0)
            sort: Field to sort by
            order: Sort order ('asc' or 'desc')
            **filters: Additional filter parameters
                - domainName: Domain name filter
                - customer: Customer handle
                - status: Domain status
                - registrant: Registrant handle
        """
        params = {
            "limit": limit,
            "offset": offset,
            **filters
        }

        if sort:
            params["sort"] = sort
        if order:
            params["order"] = order

        return self.client._request('GET', 'domains', params=params)

    def get(self, domain: str) -> Domain:
        """Get domain details"""
        response = self.client._request('GET', f'domains/{domain}')
        return Domain.from_dict(response)

    def check(self, domain: str) -> Dict[str, Any]:
        """Check domain availability"""
        return self.client._request('GET', f'domains/{domain}/check')

    def register(
            self,
            domain: str,
            customer: str,
            registrant: str,
            contacts: List[Dict[str, str]],
            nameservers: List[str],
            period: int = 1,
            properties: Optional[Dict[str, Any]] = None
    ) -> Domain:
        """Register a new domain"""
        data = {
            'customer': customer,
            'registrant': registrant,
            'contacts': contacts,
            'ns': nameservers,
            'period': period
        }

        if properties:
            data['properties'] = properties

        response = self.client._request('POST', f'domains/{domain}', data=data)
        return Domain.from_dict(response)

    def update(
            self,
            domain: str,
            contacts: Optional[List[Dict[str, str]]] = None,
            nameservers: Optional[List[str]] = None,
            properties: Optional[Dict[str, Any]] = None
    ) -> Domain:
        """Update domain details"""
        data = {}
        if contacts:
            data['contacts'] = contacts
        if nameservers:
            data['ns'] = nameservers
        if properties:
            data['properties'] = properties

        response = self.client._request('PUT', f'domains/{domain}', data=data)
        return Domain.from_dict(response)

    def delete(self, domain: str) -> None:
        """Delete a domain"""
        self.client._request('DELETE', f'domains/{domain}')
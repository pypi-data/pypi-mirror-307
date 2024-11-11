from typing import Dict, Any, List, Optional
from datetime import datetime

class ResellerApi:
    def __init__(self, client):
        self.client = client

    def get_balance(self) -> Dict[str, Any]:
        """Get reseller balance"""
        return self.client._request('GET', 'reseller/balance')

    def list_transactions(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        page: int = 1,
        limit: int = 25
    ) -> Dict[str, Any]:
        """List reseller transactions"""
        params = {'page': page, 'limit': limit}
        if start_date:
            params['startDate'] = start_date.isoformat()
        if end_date:
            params['endDate'] = end_date.isoformat()
        return self.client._request('GET', 'reseller/transactions', params=params)

    def get_transaction(self, id: str) -> Dict[str, Any]:
        """Get reseller transaction details"""
        return self.client._request('GET', f'reseller/transactions/{id}')

    def query_transactions(
        self,
        query: str,
        type: Optional[str] = None,
        page: int = 1,
        limit: int = 25
    ) -> Dict[str, Any]:
        """Search reseller transactions"""
        params = {
            'q': query,
            'page': page,
            'limit': limit
        }
        if type:
            params['type'] = type
        return self.client._request('GET', 'reseller/transactions/query', params=params)
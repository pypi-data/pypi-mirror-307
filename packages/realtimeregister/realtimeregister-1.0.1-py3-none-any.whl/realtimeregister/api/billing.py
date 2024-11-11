from typing import Dict, Any, List, Optional
from datetime import datetime
from ..models.invoice import Invoice
from ..models.transaction import Transaction

class BillingApi:
    def __init__(self, client):
        self.client = client

    def list_invoices(self, page: int = 1, limit: int = 25) -> Dict[str, Any]:
        """List invoices"""
        return self.client._request('GET', 'billing/invoices', params={'page': page, 'limit': limit})

    def get_invoice(self, id: str) -> Invoice:
        """Get invoice details"""
        response = self.client._request('GET', f'billing/invoices/{id}')
        return Invoice.from_dict(response)

    def download_invoice(self, id: str) -> bytes:
        """Download invoice PDF"""
        response = self.client._request('GET', f'billing/invoices/{id}/download')
        return response

    def list_transactions(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        page: int = 1,
        limit: int = 25
    ) -> Dict[str, Any]:
        """List transactions"""
        params = {'page': page, 'limit': limit}
        if start_date:
            params['startDate'] = start_date.isoformat()
        if end_date:
            params['endDate'] = end_date.isoformat()
        return self.client._request('GET', 'billing/transactions', params=params)

    def get_transaction(self, id: str) -> Transaction:
        """Get transaction details"""
        response = self.client._request('GET', f'billing/transactions/{id}')
        return Transaction.from_dict(response)

    def query_invoices(
        self,
        query: str,
        status: Optional[str] = None,
        page: int = 1,
        limit: int = 25
    ) -> Dict[str, Any]:
        """Search invoices"""
        params = {
            'q': query,
            'page': page,
            'limit': limit
        }
        if status:
            params['status'] = status
        return self.client._request('GET', 'billing/invoices/query', params=params)

    def query_transactions(
        self,
        query: str,
        type: Optional[str] = None,
        page: int = 1,
        limit: int = 25
    ) -> Dict[str, Any]:
        """Search transactions"""
        params = {
            'q': query,
            'page': page,
            'limit': limit
        }
        if type:
            params['type'] = type
        return self.client._request('GET', 'billing/transactions/query', params=params)
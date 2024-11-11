from typing import Dict, Any, Optional
from datetime import datetime

class StatisticsApi:
    def __init__(self, client):
        self.client = client

    def get_domain_statistics(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Get domain statistics"""
        params = {}
        if start_date:
            params['startDate'] = start_date.isoformat()
        if end_date:
            params['endDate'] = end_date.isoformat()
        return self.client._request('GET', 'statistics/domains', params=params)

    def get_billing_statistics(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Get billing statistics"""
        params = {}
        if start_date:
            params['startDate'] = start_date.isoformat()
        if end_date:
            params['endDate'] = end_date.isoformat()
        return self.client._request('GET', 'statistics/billing', params=params)

    def get_customer_statistics(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Get customer statistics"""
        params = {}
        if start_date:
            params['startDate'] = start_date.isoformat()
        if end_date:
            params['endDate'] = end_date.isoformat()
        return self.client._request('GET', 'statistics/customers', params=params)
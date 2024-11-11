import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from realtimeregister import Client
from realtimeregister.models.statistics import (
    DomainStatistics,
    BillingStatistics,
    CustomerStatistics
)

class TestStatisticsApi(unittest.TestCase):
    def setUp(self):
        self.client = Client(
            customer="test_customer",
            api_key="test_api_key",
            test_mode=True
        )
        
    @patch("requests.request")
    def test_get_domain_statistics(self, mock_request):
        stats_data = {
            "total": 100,
            "active": 80,
            "expired": 15,
            "pending": 5,
            "periodDistribution": {"1": 50, "2": 30, "3": 20},
            "tldDistribution": {"com": 60, "net": 40},
            "createdDate": "2023-01-01T00:00:00Z"
        }
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = stats_data
        mock_request.return_value = mock_response
        
        result = self.client.statistics.get_domain_statistics()
        stats = DomainStatistics.from_dict(result)
        self.assertEqual(stats.total, 100)
        self.assertEqual(stats.active, 80)
        
    @patch("requests.request")
    def test_get_billing_statistics(self, mock_request):
        stats_data = {
            "totalAmount": 5000.0,
            "paidAmount": 4500.0,
            "outstandingAmount": 500.0,
            "currency": "EUR",
            "invoiceDistribution": {"paid": 90, "pending": 10},
            "createdDate": "2023-01-01T00:00:00Z"
        }
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = stats_data
        mock_request.return_value = mock_response
        
        result = self.client.statistics.get_billing_statistics()
        stats = BillingStatistics.from_dict(result)
        self.assertEqual(stats.total_amount, 5000.0)
        self.assertEqual(stats.currency, "EUR")

    @patch("requests.request")
    def test_get_customer_statistics(self, mock_request):
        stats_data = {
            "total": 50,
            "active": 45,
            "suspended": 5,
            "billingTypeDistribution": {"prepaid": 30, "postpaid": 20},
            "createdDate": "2023-01-01T00:00:00Z"
        }
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = stats_data
        mock_request.return_value = mock_response
        
        result = self.client.statistics.get_customer_statistics()
        stats = CustomerStatistics.from_dict(result)
        self.assertEqual(stats.total, 50)
        self.assertEqual(stats.active, 45)

if __name__ == "__main__":
    unittest.main()
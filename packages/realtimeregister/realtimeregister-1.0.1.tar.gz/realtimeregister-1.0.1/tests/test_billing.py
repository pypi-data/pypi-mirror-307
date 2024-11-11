import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from realtimeregister import Client
from realtimeregister.models import Invoice, Transaction
from realtimeregister.exceptions import (
    RealtimeRegisterException,
    ValidationException,
    AuthenticationException,
    NotFoundException
)

class TestBillingApi(unittest.TestCase):
    def setUp(self):
        self.client = Client(
            customer="test_customer",
            api_key="test_api_key",
            test_mode=True
        )
        
    @patch("requests.request")
    def test_list_invoices(self, mock_request):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "invoices": [],
            "total": 0,
            "page": 1,
            "limit": 25
        }
        mock_request.return_value = mock_response
        
        result = self.client.billing.list_invoices()
        self.assertEqual(result["total"], 0)
        self.assertEqual(result["page"], 1)
        
    @patch("requests.request")
    def test_get_invoice(self, mock_request):
        invoice_data = {
            "id": "inv123",
            "number": "INV-2023-001",
            "customerHandle": "customer1",
            "brandName": "brand1",
            "status": "paid",
            "currencyCode": "EUR",
            "subTotal": 100.0,
            "vatAmount": 21.0,
            "totalAmount": 121.0,
            "items": [],
            "dueDate": "2023-12-31T00:00:00Z",
            "createdDate": "2023-01-01T00:00:00Z"
        }
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = invoice_data
        mock_request.return_value = mock_response
        
        result = self.client.billing.get_invoice("inv123")
        self.assertIsInstance(result, Invoice)
        self.assertEqual(result.id, "inv123")
        self.assertEqual(result.total_amount, 121.0)

    @patch("requests.request")
    def test_list_transactions(self, mock_request):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "transactions": [],
            "total": 0,
            "page": 1,
            "limit": 25
        }
        mock_request.return_value = mock_response
        
        result = self.client.billing.list_transactions()
        self.assertEqual(result["total"], 0)
        self.assertEqual(result["page"], 1)

if __name__ == "__main__":
    unittest.main()
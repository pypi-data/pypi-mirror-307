import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from realtimeregister import Client
from realtimeregister.exceptions import (
    RealtimeRegisterException,
    ValidationException,
    AuthenticationException,
    NotFoundException
)

class TestResellerApi(unittest.TestCase):
    def setUp(self):
        self.client = Client(
            customer="test_customer",
            api_key="test_api_key",
            test_mode=True
        )
        
    @patch("requests.request")
    def test_get_balance(self, mock_request):
        balance_data = {
            "balance": 1000.0,
            "reserved": 100.0,
            "available": 900.0,
            "currency": "EUR"
        }
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = balance_data
        mock_request.return_value = mock_response
        
        result = self.client.reseller.get_balance()
        self.assertEqual(result["balance"], 1000.0)
        self.assertEqual(result["available"], 900.0)
        self.assertEqual(result["currency"], "EUR")
        
    @patch("requests.request")
    def test_list_transactions(self, mock_request):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "transactions": [
                {
                    "id": "trans123",
                    "type": "deposit",
                    "amount": 500.0,
                    "currency": "EUR",
                    "description": "Bank deposit",
                    "createdDate": "2023-01-01T00:00:00Z"
                }
            ],
            "total": 1,
            "page": 1,
            "limit": 25
        }
        mock_request.return_value = mock_response
        
        result = self.client.reseller.list_transactions()
        self.assertEqual(result["total"], 1)
        self.assertEqual(result["transactions"][0]["amount"], 500.0)

    @patch("requests.request")
    def test_get_transaction(self, mock_request):
        transaction_data = {
            "id": "trans123",
            "type": "deposit",
            "amount": 500.0,
            "currency": "EUR",
            "description": "Bank deposit",
            "createdDate": "2023-01-01T00:00:00Z"
        }
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = transaction_data
        mock_request.return_value = mock_response
        
        result = self.client.reseller.get_transaction("trans123")
        self.assertEqual(result["id"], "trans123")
        self.assertEqual(result["amount"], 500.0)

    @patch("requests.request")
    def test_query_transactions(self, mock_request):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "transactions": [
                {
                    "id": "trans123",
                    "type": "deposit",
                    "amount": 500.0,
                    "currency": "EUR",
                    "description": "Bank deposit",
                    "createdDate": "2023-01-01T00:00:00Z"
                }
            ],
            "total": 1,
            "page": 1,
            "limit": 25
        }
        mock_request.return_value = mock_response
        
        result = self.client.reseller.query_transactions(
            query="deposit",
            type="deposit"
        )
        self.assertEqual(result["total"], 1)
        self.assertEqual(result["transactions"][0]["type"], "deposit")

if __name__ == "__main__":
    unittest.main()
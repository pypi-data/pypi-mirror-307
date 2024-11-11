import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from realtimeregister import Client
from realtimeregister.models import Transfer
from realtimeregister.exceptions import (
    RealtimeRegisterException,
    ValidationException,
    AuthenticationException,
    NotFoundException
)

class TestTransfersApi(unittest.TestCase):
    def setUp(self):
        self.client = Client(
            customer="test_customer",
            api_key="test_api_key",
            test_mode=True
        )
        
    @patch("requests.request")
    def test_list_transfers(self, mock_request):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "transfers": [],
            "total": 0,
            "page": 1,
            "limit": 25
        }
        mock_request.return_value = mock_response
        
        result = self.client.transfers.list()
        self.assertEqual(result["total"], 0)
        self.assertEqual(result["page"], 1)
        
    @patch("requests.request")
    def test_get_transfer(self, mock_request):
        transfer_data = {
            "domain": "example.com",
            "status": "pending",
            "registrar": "Example Registrar",
            "authCode": "ABC123",
            "createdDate": "2023-01-01T00:00:00Z"
        }
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = transfer_data
        mock_request.return_value = mock_response
        
        result = self.client.transfers.get("example.com")
        self.assertIsInstance(result, Transfer)
        self.assertEqual(result.domain, "example.com")
        self.assertEqual(result.status, "pending")
        
    @patch("requests.request")
    def test_request_transfer(self, mock_request):
        transfer_data = {
            "domain": "example.com",
            "status": "pending",
            "registrar": "Example Registrar",
            "authCode": "ABC123",
            "period": 1,
            "createdDate": "2023-01-01T00:00:00Z"
        }
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = transfer_data
        mock_request.return_value = mock_response
        
        result = self.client.transfers.request(
            domain="example.com",
            auth_code="ABC123",
            period=1
        )
        self.assertIsInstance(result, Transfer)
        self.assertEqual(result.domain, "example.com")
        self.assertEqual(result.auth_code, "ABC123")

    @patch("requests.request")
    def test_approve_transfer(self, mock_request):
        transfer_data = {
            "domain": "example.com",
            "status": "completed",
            "registrar": "Example Registrar",
            "authCode": "ABC123",
            "createdDate": "2023-01-01T00:00:00Z",
            "updatedDate": "2023-01-02T00:00:00Z"
        }
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = transfer_data
        mock_request.return_value = mock_response
        
        result = self.client.transfers.approve("example.com")
        self.assertIsInstance(result, Transfer)
        self.assertEqual(result.status, "completed")

    @patch("requests.request")
    def test_reject_transfer(self, mock_request):
        transfer_data = {
            "domain": "example.com",
            "status": "rejected",
            "registrar": "Example Registrar",
            "authCode": "ABC123",
            "createdDate": "2023-01-01T00:00:00Z",
            "updatedDate": "2023-01-02T00:00:00Z"
        }
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = transfer_data
        mock_request.return_value = mock_response
        
        result = self.client.transfers.reject(
            domain="example.com",
            reason="Invalid auth code"
        )
        self.assertIsInstance(result, Transfer)
        self.assertEqual(result.status, "rejected")

if __name__ == "__main__":
    unittest.main()
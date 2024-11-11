import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from realtimeregister import Client
from realtimeregister.models import Certificate
from realtimeregister.exceptions import (
    RealtimeRegisterException,
    ValidationException,
    AuthenticationException,
    NotFoundException
)

class TestCertificatesApi(unittest.TestCase):
    def setUp(self):
        self.client = Client(
            customer="test_customer",
            api_key="test_api_key",
            test_mode=True
        )
        
    @patch("requests.request")
    def test_list_certificates(self, mock_request):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "certificates": [],
            "total": 0,
            "page": 1,
            "limit": 25
        }
        mock_request.return_value = mock_response
        
        result = self.client.certificates.list()
        self.assertEqual(result["total"], 0)
        self.assertEqual(result["page"], 1)
        
    @patch("requests.request")
    def test_get_certificate(self, mock_request):
        cert_data = {
            "id": "cert123",
            "domain": "example.com",
            "type": "DV",
            "status": "active",
            "validationMethod": "dns",
            "validationStatus": "completed",
            "createdDate": "2023-01-01T00:00:00Z",
            "expiryDate": "2024-01-01T00:00:00Z"
        }
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = cert_data
        mock_request.return_value = mock_response
        
        result = self.client.certificates.get("cert123")
        self.assertIsInstance(result, Certificate)
        self.assertEqual(result.id, "cert123")
        self.assertEqual(result.domain, "example.com")
        
    @patch("requests.request")
    def test_order_certificate(self, mock_request):
        cert_data = {
            "id": "cert123",
            "domain": "example.com",
            "type": "DV",
            "status": "pending",
            "validationMethod": "dns",
            "validationStatus": "pending",
            "createdDate": "2023-01-01T00:00:00Z",
            "expiryDate": "2024-01-01T00:00:00Z"
        }
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = cert_data
        mock_request.return_value = mock_response
        
        result = self.client.certificates.order(
            domain="example.com",
            type="DV",
            validation_method="dns"
        )
        self.assertIsInstance(result, Certificate)
        self.assertEqual(result.domain, "example.com")
        self.assertEqual(result.status, "pending")

if __name__ == "__main__":
    unittest.main()
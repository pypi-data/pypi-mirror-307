import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from realtimeregister import Client
from realtimeregister.models import AbuseReport
from realtimeregister.exceptions import (
    RealtimeRegisterException,
    ValidationException,
    AuthenticationException,
    NotFoundException
)

class TestAbuseApi(unittest.TestCase):
    def setUp(self):
        self.client = Client(
            customer="test_customer",
            api_key="test_api_key",
            test_mode=True
        )
        
    @patch("requests.request")
    def test_list_abuse_reports(self, mock_request):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "reports": [],
            "total": 0,
            "page": 1,
            "limit": 25
        }
        mock_request.return_value = mock_response
        
        result = self.client.abuse.list()
        self.assertEqual(result["total"], 0)
        self.assertEqual(result["page"], 1)
        
    @patch("requests.request")
    def test_get_abuse_report(self, mock_request):
        report_data = {
            "id": "abuse123",
            "domain": "example.com",
            "reporterName": "John Doe",
            "reporterEmail": "john@example.com",
            "message": "Spam content",
            "status": "open",
            "createdDate": "2023-01-01T00:00:00Z"
        }
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = report_data
        mock_request.return_value = mock_response
        
        result = self.client.abuse.get("abuse123")
        self.assertIsInstance(result, AbuseReport)
        self.assertEqual(result.id, "abuse123")
        self.assertEqual(result.domain, "example.com")
        
    @patch("requests.request")
    def test_create_abuse_report(self, mock_request):
        report_data = {
            "id": "abuse123",
            "domain": "example.com",
            "reporterName": "John Doe",
            "reporterEmail": "john@example.com",
            "message": "Spam content",
            "status": "open",
            "createdDate": "2023-01-01T00:00:00Z"
        }
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = report_data
        mock_request.return_value = mock_response
        
        result = self.client.abuse.create(
            domain="example.com",
            reporter_name="John Doe",
            reporter_email="john@example.com",
            message="Spam content"
        )
        self.assertIsInstance(result, AbuseReport)
        self.assertEqual(result.domain, "example.com")
        self.assertEqual(result.status, "open")

    @patch("requests.request")
    def test_update_abuse_report(self, mock_request):
        report_data = {
            "id": "abuse123",
            "domain": "example.com",
            "reporterName": "John Doe",
            "reporterEmail": "john@example.com",
            "message": "Spam content",
            "status": "closed",
            "notes": "Issue resolved",
            "createdDate": "2023-01-01T00:00:00Z",
            "updatedDate": "2023-01-02T00:00:00Z"
        }
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = report_data
        mock_request.return_value = mock_response
        
        result = self.client.abuse.update(
            id="abuse123",
            status="closed",
            notes="Issue resolved"
        )
        self.assertIsInstance(result, AbuseReport)
        self.assertEqual(result.status, "closed")
        self.assertEqual(result.notes, "Issue resolved")

if __name__ == "__main__":
    unittest.main()
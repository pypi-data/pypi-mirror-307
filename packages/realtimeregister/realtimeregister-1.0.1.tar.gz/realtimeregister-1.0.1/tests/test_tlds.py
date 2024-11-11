import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from realtimeregister import Client
from realtimeregister.models import TLD
from realtimeregister.exceptions import (
    RealtimeRegisterException,
    ValidationException,
    AuthenticationException,
    NotFoundException
)

class TestTLDsApi(unittest.TestCase):
    def setUp(self):
        self.client = Client(
            customer="test_customer",
            api_key="test_api_key",
            test_mode=True
        )
        
    @patch("requests.request")
    def test_list_tlds(self, mock_request):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "tlds": [],
            "total": 0,
            "page": 1,
            "limit": 25
        }
        mock_request.return_value = mock_response
        
        result = self.client.tlds.list()
        self.assertEqual(result["total"], 0)
        self.assertEqual(result["page"], 1)
        
    @patch("requests.request")
    def test_get_tld(self, mock_request):
        tld_data = {
            "name": "com",
            "status": "active",
            "launchPhase": "general-availability",
            "idnScripts": ["latin"],
            "minPeriod": 1,
            "maxPeriod": 10,
            "gracePeriod": 30,
            "transferPeriod": 5,
            "createdDate": "2023-01-01T00:00:00Z"
        }
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = tld_data
        mock_request.return_value = mock_response
        
        result = self.client.tlds.get("com")
        self.assertIsInstance(result, TLD)
        self.assertEqual(result.name, "com")
        self.assertEqual(result.status, "active")

    @patch("requests.request")
    def test_query_tlds(self, mock_request):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "tlds": [
                {
                    "name": "com",
                    "status": "active",
                    "launchPhase": "general-availability",
                    "idnScripts": ["latin"],
                    "minPeriod": 1,
                    "maxPeriod": 10,
                    "gracePeriod": 30,
                    "transferPeriod": 5,
                    "createdDate": "2023-01-01T00:00:00Z"
                }
            ],
            "total": 1,
            "page": 1,
            "limit": 25
        }
        mock_request.return_value = mock_response
        
        result = self.client.tlds.query(
            query="com",
            status="active"
        )
        self.assertEqual(result["total"], 1)
        self.assertEqual(result["tlds"][0]["name"], "com")

if __name__ == "__main__":
    unittest.main()
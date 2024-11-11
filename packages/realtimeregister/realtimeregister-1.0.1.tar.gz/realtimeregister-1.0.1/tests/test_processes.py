import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from realtimeregister import Client
from realtimeregister.models import Process
from realtimeregister.exceptions import (
    RealtimeRegisterException,
    ValidationException,
    AuthenticationException,
    NotFoundException
)

class TestProcessesApi(unittest.TestCase):
    def setUp(self):
        self.client = Client(
            customer="test_customer",
            api_key="test_api_key",
            test_mode=True
        )
        
    @patch("requests.request")
    def test_list_processes(self, mock_request):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "processes": [],
            "total": 0,
            "page": 1,
            "limit": 25
        }
        mock_request.return_value = mock_response
        
        result = self.client.processes.list()
        self.assertEqual(result["total"], 0)
        self.assertEqual(result["page"], 1)
        
    @patch("requests.request")
    def test_get_process(self, mock_request):
        process_data = {
            "id": "proc123",
            "type": "domain.transfer",
            "status": "running",
            "entityType": "domain",
            "entityId": "example.com",
            "progress": 50,
            "message": "Transfer in progress",
            "createdDate": "2023-01-01T00:00:00Z"
        }
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = process_data
        mock_request.return_value = mock_response
        
        result = self.client.processes.get("proc123")
        self.assertIsInstance(result, Process)
        self.assertEqual(result.id, "proc123")
        self.assertEqual(result.type, "domain.transfer")
        self.assertEqual(result.progress, 50)

    @patch("requests.request")
    def test_query_processes(self, mock_request):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "processes": [
                {
                    "id": "proc123",
                    "type": "domain.transfer",
                    "status": "running",
                    "entityType": "domain",
                    "entityId": "example.com",
                    "progress": 50,
                    "createdDate": "2023-01-01T00:00:00Z"
                }
            ],
            "total": 1,
            "page": 1,
            "limit": 25
        }
        mock_request.return_value = mock_response
        
        result = self.client.processes.query(
            query="example.com",
            status="running",
            type="domain.transfer"
        )
        self.assertEqual(result["total"], 1)
        self.assertEqual(result["processes"][0]["id"], "proc123")

if __name__ == "__main__":
    unittest.main()
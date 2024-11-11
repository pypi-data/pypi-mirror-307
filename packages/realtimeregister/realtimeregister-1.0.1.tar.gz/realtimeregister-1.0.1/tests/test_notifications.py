import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from realtimeregister import Client
from realtimeregister.models import Notification
from realtimeregister.exceptions import (
    RealtimeRegisterException,
    ValidationException,
    AuthenticationException,
    NotFoundException
)

class TestNotificationsApi(unittest.TestCase):
    def setUp(self):
        self.client = Client(
            customer="test_customer",
            api_key="test_api_key",
            test_mode=True
        )
        
    @patch("requests.request")
    def test_list_notifications(self, mock_request):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "notifications": [],
            "total": 0,
            "page": 1,
            "limit": 25
        }
        mock_request.return_value = mock_response
        
        result = self.client.notifications.list()
        self.assertEqual(result["total"], 0)
        self.assertEqual(result["page"], 1)
        
    @patch("requests.request")
    def test_get_notification(self, mock_request):
        notification_data = {
            "id": "notif123",
            "type": "webhook",
            "destination": "https://example.com/webhook",
            "events": ["domain.create", "domain.expire"],
            "enabled": True,
            "createdDate": "2023-01-01T00:00:00Z"
        }
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = notification_data
        mock_request.return_value = mock_response
        
        result = self.client.notifications.get("notif123")
        self.assertIsInstance(result, Notification)
        self.assertEqual(result.id, "notif123")
        self.assertEqual(result.type, "webhook")
        
    @patch("requests.request")
    def test_create_notification(self, mock_request):
        notification_data = {
            "id": "notif123",
            "type": "email",
            "destination": "admin@example.com",
            "events": ["domain.expire"],
            "enabled": True,
            "createdDate": "2023-01-01T00:00:00Z"
        }
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = notification_data
        mock_request.return_value = mock_response
        
        result = self.client.notifications.create(
            type="email",
            destination="admin@example.com",
            events=["domain.expire"]
        )
        self.assertIsInstance(result, Notification)
        self.assertEqual(result.type, "email")
        self.assertEqual(result.destination, "admin@example.com")

    @patch("requests.request")
    def test_test_notification(self, mock_request):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True}
        mock_request.return_value = mock_response
        
        result = self.client.notifications.test("notif123")
        self.assertTrue(result)

if __name__ == "__main__":
    unittest.main()
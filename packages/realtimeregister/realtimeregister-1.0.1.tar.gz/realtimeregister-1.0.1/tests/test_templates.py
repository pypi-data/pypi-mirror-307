import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from realtimeregister import Client
from realtimeregister.models import Template
from realtimeregister.exceptions import (
    RealtimeRegisterException,
    ValidationException,
    AuthenticationException,
    NotFoundException
)

class TestTemplatesApi(unittest.TestCase):
    def setUp(self):
        self.client = Client(
            customer="test_customer",
            api_key="test_api_key",
            test_mode=True
        )
        
    @patch("requests.request")
    def test_list_templates(self, mock_request):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "templates": [],
            "total": 0,
            "page": 1,
            "limit": 25
        }
        mock_request.return_value = mock_response
        
        result = self.client.templates.list()
        self.assertEqual(result["total"], 0)
        self.assertEqual(result["page"], 1)
        
    @patch("requests.request")
    def test_get_template(self, mock_request):
        template_data = {
            "name": "welcome-email",
            "type": "email",
            "content": "Welcome {{name}}!",
            "subject": "Welcome to our service",
            "description": "Welcome email template",
            "createdDate": "2023-01-01T00:00:00Z"
        }
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = template_data
        mock_request.return_value = mock_response
        
        result = self.client.templates.get("welcome-email")
        self.assertIsInstance(result, Template)
        self.assertEqual(result.name, "welcome-email")
        self.assertEqual(result.type, "email")
        
    @patch("requests.request")
    def test_create_template(self, mock_request):
        template_data = {
            "name": "invoice-template",
            "type": "document",
            "content": "<html>{{content}}</html>",
            "description": "Invoice template",
            "createdDate": "2023-01-01T00:00:00Z"
        }
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = template_data
        mock_request.return_value = mock_response
        
        result = self.client.templates.create(
            name="invoice-template",
            type="document",
            content="<html>{{content}}</html>",
            description="Invoice template"
        )
        self.assertIsInstance(result, Template)
        self.assertEqual(result.name, "invoice-template")
        self.assertEqual(result.type, "document")

    @patch("requests.request")
    def test_preview_template(self, mock_request):
        preview_data = {
            "content": "Welcome John Doe!"
        }
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = preview_data
        mock_request.return_value = mock_response
        
        result = self.client.templates.preview(
            name="welcome-email",
            data={"name": "John Doe"}
        )
        self.assertEqual(result, "Welcome John Doe!")

if __name__ == "__main__":
    unittest.main()
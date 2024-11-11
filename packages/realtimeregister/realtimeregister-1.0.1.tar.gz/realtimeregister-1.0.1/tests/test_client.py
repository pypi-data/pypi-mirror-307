import unittest
from unittest.mock import patch, MagicMock
from realtimeregister import Client
from realtimeregister.exceptions import (
    RealtimeRegisterException,
    ValidationException,
    AuthenticationException,
    NotFoundException
)

class TestClient(unittest.TestCase):
    def setUp(self):
        self.client = Client(
            customer="test_customer",
            api_key="test_api_key",
            test_mode=True
        )
        
    @patch("requests.request")
    def test_get_domains(self, mock_request):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"domains": []}
        mock_request.return_value = mock_response
        
        result = self.client.get_domains()
        self.assertEqual(result, {"domains": []})
        
    @patch("requests.request")
    def test_authentication_error(self, mock_request):
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_request.return_value = mock_response
        
        with self.assertRaises(AuthenticationException):
            self.client.get_domains()

if __name__ == "__main__":
    unittest.main()
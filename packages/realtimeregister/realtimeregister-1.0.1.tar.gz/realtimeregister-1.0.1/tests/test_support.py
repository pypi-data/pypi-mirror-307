import unittest
from datetime import datetime
from realtimeregister.support.helpers import (
    format_date,
    parse_date,
    clean_dict,
    validate_required,
    validate_enum,
    validate_type
)
from realtimeregister.support.pagination import PaginatedResponse
from realtimeregister.support.validation import Validator
from realtimeregister.exceptions import ValidationException
from realtimeregister.enums import DomainStatus

class TestHelpers(unittest.TestCase):
    def test_format_date(self):
        date = datetime(2023, 1, 1, 12, 0, 0)
        self.assertEqual(format_date(date), "2023-01-01T12:00:00")
        self.assertIsNone(format_date(None))
        
    def test_parse_date(self):
        date_str = "2023-01-01T12:00:00"
        expected = datetime(2023, 1, 1, 12, 0, 0)
        self.assertEqual(parse_date(date_str), expected)
        self.assertIsNone(parse_date(None))
        
    def test_clean_dict(self):
        data = {"a": 1, "b": None, "c": "test"}
        cleaned = clean_dict(data)
        self.assertEqual(cleaned, {"a": 1, "c": "test"})
        
    def test_validate_required(self):
        data = {"a": 1, "c": "test"}
        with self.assertRaises(ValueError):
            validate_required(data, ["a", "b", "c"])
            
    def test_validate_enum(self):
        with self.assertRaises(ValueError):
            validate_enum("invalid", DomainStatus)
        validate_enum("active", DomainStatus)
        
    def test_validate_type(self):
        with self.assertRaises(TypeError):
            validate_type("123", int, "test_field")
        validate_type(123, int, "test_field")

class TestPagination(unittest.TestCase):
    def test_paginated_response(self):
        class TestItem:
            @classmethod
            def from_dict(cls, data):
                return data
                
        data = {
            "items": [{"id": 1}, {"id": 2}],
            "total": 10,
            "page": 1,
            "limit": 2
        }
        
        response = PaginatedResponse.from_dict(data, "items", TestItem)
        self.assertEqual(len(response.items), 2)
        self.assertTrue(response.has_next_page())
        self.assertFalse(response.has_previous_page())
        self.assertEqual(response.next_page_number(), 2)
        self.assertIsNone(response.previous_page_number())

class TestValidator(unittest.TestCase):
    def test_validate_string(self):
        with self.assertRaises(ValidationException):
            Validator.validate_string(123, "test_field")
        Validator.validate_string("test", "test_field", min_length=2, max_length=10)
        
    def test_validate_integer(self):
        with self.assertRaises(ValidationException):
            Validator.validate_integer("123", "test_field")
        Validator.validate_integer(5, "test_field", min_value=0, max_value=10)
        
    def test_validate_email(self):
        with self.assertRaises(ValidationException):
            Validator.validate_email("invalid-email", "test_field")
        Validator.validate_email("test@example.com", "test_field")
        
    def test_validate_domain(self):
        with self.assertRaises(ValidationException):
            Validator.validate_domain("invalid domain", "test_field")
        Validator.validate_domain("example.com", "test_field")
        
    def test_validate_url(self):
        with self.assertRaises(ValidationException):
            Validator.validate_url("invalid-url", "test_field")
        Validator.validate_url("https://example.com", "test_field")

if __name__ == "__main__":
    unittest.main()
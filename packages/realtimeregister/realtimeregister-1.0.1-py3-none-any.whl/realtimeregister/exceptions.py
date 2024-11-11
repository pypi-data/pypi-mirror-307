class RealtimeRegisterException(Exception):
    """Base exception for Realtime Register API"""
    pass

class ValidationException(RealtimeRegisterException):
    """Raised when request validation fails"""
    pass

class AuthenticationException(RealtimeRegisterException):
    """Raised when authentication fails"""
    pass

class NotFoundException(RealtimeRegisterException):
    """Raised when resource is not found"""
    pass
from enum import Enum, unique

@unique
class CertificateValidationMethod(Enum):
    DNS = "dns"
    EMAIL = "email"
    HTTP = "http"
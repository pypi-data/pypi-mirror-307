import requests
from datetime import datetime
from typing import Dict, Any, Optional
from .exceptions import (
    RealtimeRegisterException,
    ValidationException,
    AuthenticationException,
    NotFoundException
)
from .api import (
    DomainsApi,
    ContactsApi,
    BrandsApi,
    CustomersApi,
    ProvidersApi,
    DNSApi,
    CertificatesApi,
    BillingApi,
    TemplatesApi,
    NotificationsApi,
    AbuseApi,
    ProcessesApi,
    StatisticsApi,
    TLDsApi,
    ResellerApi,
    TransfersApi
)


class Client:
    def __init__(
            self,
            api_key: str,
            customer: Optional[str] = None,
            test_mode: bool = False,
            timeout: int = 30
    ):
        self.api_key = api_key
        self.customer = customer
        self.test_mode = test_mode
        self.timeout = timeout

        # Set up base URL for production/test environment
        self.base_url = "https://api.yoursrs.com/v2"
        if test_mode:
            self.base_url = "https://api.yoursrs-ote.com/v2"

        # Set up session with retry configuration
        self.session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(
            max_retries=3,
            pool_connections=10,
            pool_maxsize=10
        )
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)

        # Initialize API endpoints
        self.domains = DomainsApi(self)
        self.contacts = ContactsApi(self)
        self.brands = BrandsApi(self)
        self.customers = CustomersApi(self)
        self.providers = ProvidersApi(self)
        self.dns = DNSApi(self)
        self.certificates = CertificatesApi(self)
        self.billing = BillingApi(self)
        self.templates = TemplatesApi(self)
        self.notifications = NotificationsApi(self)
        self.abuse = AbuseApi(self)
        self.processes = ProcessesApi(self)
        self.statistics = StatisticsApi(self)
        self.tlds = TLDsApi(self)
        self.reseller = ResellerApi(self)
        self.transfers = TransfersApi(self)

    def _request(
            self,
            method: str,
            endpoint: str,
            params: Optional[Dict] = None,
            data: Optional[Dict] = None
    ) -> Dict[str, Any]:
        headers = {
            "Authorization": f"ApiKey {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        if self.customer:
            headers["X-Customer"] = self.customer

        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        try:
            response = self.session.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                json=data,
                timeout=self.timeout,
                verify=True
            )

            if response.status_code == 404:
                raise NotFoundException(f"Resource not found: {endpoint}")
            elif response.status_code == 401:
                raise AuthenticationException("Invalid authentication credentials")
            elif response.status_code == 400:
                raise ValidationException(response.json().get("message", "Validation error"))
            elif response.status_code >= 500:
                raise RealtimeRegisterException("Server error occurred")

            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            raise RealtimeRegisterException(f"Request failed: {str(e)}")

    def __del__(self):
        """Cleanup session on deletion"""
        if hasattr(self, 'session'):
            self.session.close()
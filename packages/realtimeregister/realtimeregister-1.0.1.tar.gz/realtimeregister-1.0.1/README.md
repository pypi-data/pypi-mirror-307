<img src="https://realtimeregister.com/static/images/logo.svg" width="100" height="100">

# Realtime Register Python SDK

[![Latest Stable Version](https://img.shields.io/pypi/v/realtimeregister)](https://pypi.org/project/realtimeregister/)
[![Total Downloads](https://img.shields.io/pypi/dm/realtimeregister)](https://pypi.org/project/realtimeregister/)
[![License](https://img.shields.io/pypi/l/realtimeregister)](https://pypi.org/project/realtimeregister/)
[![Python Version](https://img.shields.io/pypi/pyversions/realtimeregister)](https://pypi.org/project/realtimeregister/)

The Realtime Register Python SDK provides a convenient way to interact with the [Realtime Register REST API](https://dm.realtimeregister.com/docs/api) from your Python applications.

## Requirements

- Python 3.7 or later
- `requests` library
- `python-dateutil` library

## Installation

You can install the SDK via pip:

```bash
pip install realtimeregister
```

## Usage

```python
from realtimeregister import Client

# Initialize the client
client = Client(
    customer="your_customer_id",
    api_key="your_api_key",
    test_mode=True  # Set to False for production
)

# List domains
domains = client.domains.list()

# Get domain details
domain = client.domains.get("example.com")

# Register a new domain
new_domain = client.domains.register(
    domain="example.com",
    period=1,
    registrant={
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "+1.1234567890",
        "address": {
            "street": "123 Main St",
            "city": "Anytown",
            "state": "ST",
            "zipcode": "12345",
            "country": "US"
        }
    }
)
```

## Available API Endpoints

### Domains

```python
# List domains
client.domains.list()

# Get domain details
client.domains.get("example.com")

# Register domain
client.domains.register("example.com", registrant, period=1)

# Update domain
client.domains.update("example.com", nameservers=[...])

# Delete domain
client.domains.delete("example.com")

# Renew domain
client.domains.renew("example.com", period=1)

# Restore domain
client.domains.restore("example.com")
```

### Contacts

```python
# List contacts
client.contacts.list()

# Get contact details
client.contacts.get("contact123")

# Create contact
client.contacts.create("contact123", contact_data)

# Update contact
client.contacts.update("contact123", contact_data)

# Delete contact
client.contacts.delete("contact123")
```

### DNS

```python
# List DNS records
client.dns.list_records("example.com")

# Get DNS record
client.dns.get_record("example.com", "www", "A")

# Create DNS record
client.dns.create_record("example.com", "www", "A", ttl=3600, content={"ip": "1.2.3.4"})

# Update DNS record
client.dns.update_record("example.com", "www", "A", ttl=7200)

# Delete DNS record
client.dns.delete_record("example.com", "www", "A")
```

### SSL Certificates

```python
# List certificates
client.certificates.list()

# Get certificate details
client.certificates.get("cert123")

# Order certificate
client.certificates.order("example.com", "DV", "dns")

# Reissue certificate
client.certificates.reissue("cert123")
```

### Billing

```python
# List invoices
client.billing.list_invoices()

# Get invoice details
client.billing.get_invoice("inv123")

# Download invoice
client.billing.download_invoice("inv123")

# List transactions
client.billing.list_transactions()
```

### Templates

```python
# List templates
client.templates.list()

# Get template details
client.templates.get("welcome-email")

# Create template
client.templates.create("welcome-email", "email", "Welcome {{name}}!")

# Update template
client.templates.update("welcome-email", content="Updated welcome {{name}}!")

# Preview template
client.templates.preview("welcome-email", {"name": "John"})
```

### Notifications

```python
# List notifications
client.notifications.list()

# Get notification details
client.notifications.get("notif123")

# Create notification
client.notifications.create("webhook", "https://example.com/webhook", ["domain.expire"])

# Update notification
client.notifications.update("notif123", enabled=False)

# Test notification
client.notifications.test("notif123")
```

### Abuse

```python
# List abuse reports
client.abuse.list()

# Get abuse report details
client.abuse.get("abuse123")

# Create abuse report
client.abuse.create("example.com", "John Doe", "john@example.com", "Spam content")

# Update abuse report
client.abuse.update("abuse123", status="resolved")
```

### Processes

```python
# List processes
client.processes.list()

# Get process details
client.processes.get("proc123")
```

### Statistics

```python
# Get domain statistics
client.statistics.get_domain_statistics()

# Get billing statistics
client.statistics.get_billing_statistics()

# Get customer statistics
client.statistics.get_customer_statistics()
```

### TLDs

```python
# List TLDs
client.tlds.list()

# Get TLD details
client.tlds.get("com")
```

### Reseller

```python
# Get balance
client.reseller.get_balance()

# List transactions
client.reseller.list_transactions()

# Get transaction details
client.reseller.get_transaction("trans123")
```

### Transfers

```python
# List transfers
client.transfers.list()

# Get transfer details
client.transfers.get("example.com")

# Request transfer
client.transfers.request("example.com", "auth-code")

# Approve transfer
client.transfers.approve("example.com")

# Reject transfer
client.transfers.reject("example.com", "Invalid auth code")
```

## Error Handling

The SDK provides detailed error handling through specific exception classes:

```python
from realtimeregister.exceptions import (
    RealtimeRegisterException,
    ValidationException,
    AuthenticationException,
    NotFoundException
)

try:
    domain = client.domains.get("nonexistent.com")
except NotFoundException:
    print("Domain not found")
except AuthenticationException:
    print("Invalid credentials")
except ValidationException as e:
    print(f"Validation error: {str(e)}")
except RealtimeRegisterException as e:
    print(f"API error: {str(e)}")
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

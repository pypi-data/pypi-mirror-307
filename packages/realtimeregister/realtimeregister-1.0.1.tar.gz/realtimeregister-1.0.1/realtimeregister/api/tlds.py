from typing import Dict, Any, List, Optional
from ..models.tld import TLD


class TLDsApi:
    def __init__(self, client):
        self.client = client

    def get_info(self, tld: str) -> TLD:
        """
        Get TLD information

        Args:
            tld: The TLD to get information for (e.g. 'com', 'net')
        """
        # Remove leading dot if present
        tld = tld.lstrip('.')
        response = self.client._request('GET', f'tlds/{tld}/info')
        return TLD.from_dict(response)
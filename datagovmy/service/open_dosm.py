from typing import Optional

from datagovmy.core.api import BaseAPIClient
from datagovmy.service.environment import get_base_url


class OpenDOSMClient(BaseAPIClient):
    ENDPOINT = "/opendosm"

    def __init__(self, api_key: Optional[str] = None):
        super().__init__(base_url=get_base_url())
        self.api_key = api_key

    def get_dataset_as_json(self, id: str, **kwargs):
        # kwargs can be used to add additional query parameters for filtering
        # reference: https://developer.data.gov.my/request-query
        endpoint = f"{self.ENDPOINT}?id={id}"
        filters = "&".join(f"{k}={v}" for k, v in kwargs.items())

        if filters:
            endpoint += f"&{filters}"

        return self.get(endpoint).json()

import logging
from typing import Any, Optional, cast

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from datagovmy.exceptions import (
    APIError,
    AuthenticationError,
    NotFoundError,
    RateLimitError,
)

logger = logging.getLogger(__name__)


class BaseAPIClient:
    """Generic API client with configurable retry support.

    Args:
        base_url: Base URL for all requests (e.g. "https://api.example.com").
        headers: Default headers sent with every request.
        retry_strategy: A ``urllib3.util.retry.Retry`` instance that controls
            which status codes trigger retries, how many times, and the backoff.
    """

    def __init__(
        self,
        base_url: str,
        headers: Optional[dict[str, str]] = None,
        retry_strategy: Optional[Retry] = None,
    ):
        self.base_url = base_url
        self.session = requests.Session()
        if headers:
            self.session.headers.update(headers)
        if retry_strategy:
            adapter = HTTPAdapter(max_retries=cast(Any, retry_strategy))
            self.session.mount("http://", adapter)
            self.session.mount("https://", adapter)

    def _build_url(self, path: str) -> str:
        return f"{self.base_url}{path}"

    def _request(self, method: str, path: str, **kwargs: Any) -> requests.Response:
        url = self._build_url(path)
        logger.debug("Requesting %s %s", method, url)
        response = self.session.request(method, url, **kwargs)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as exc:
            status = response.status_code
            if status == 429:
                raise RateLimitError(response=response) from exc
            if status == 404:
                raise NotFoundError(response=response) from exc
            if status in (401, 403):
                raise AuthenticationError(
                    message=f"Authentication failed (HTTP {status})",
                    status_code=status,
                    response=response,
                ) from exc
            raise APIError(f"API error (HTTP {status})", status_code=status, response=response) from exc
        return response

    def get(
        self,
        path: str,
        params: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, str]] = None,
    ) -> requests.Response:
        return self._request("GET", path, params=params, headers=headers)

    def post(
        self,
        path: str,
        json: Optional[Any] = None,
        headers: Optional[dict[str, str]] = None,
    ) -> requests.Response:
        return self._request("POST", path, json=json, headers=headers)

    def put(
        self,
        path: str,
        json: Optional[Any] = None,
        headers: Optional[dict[str, str]] = None,
    ) -> requests.Response:
        return self._request("PUT", path, json=json, headers=headers)

    def delete(
        self,
        path: str,
        params: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, str]] = None,
    ) -> requests.Response:
        return self._request("DELETE", path, params=params, headers=headers)

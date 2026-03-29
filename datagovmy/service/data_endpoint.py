import logging
from typing import Any, Optional

from urllib3.util.retry import Retry

from datagovmy.core.api import BaseAPIClient
from datagovmy.service.environment import get_base_url

logger = logging.getLogger(__name__)

DEFAULT_RETRY = Retry(
    total=3,
    status_forcelist=[429, 500, 502, 503, 504],
    backoff_factor=1,
    allowed_methods=["GET"],
)


class DataEndpointClient(BaseAPIClient):
    """Base client for data.gov.my JSON dataset endpoints.

    Subclasses only need to set ``ENDPOINT`` to the API path
    (e.g. ``/data-catalogue`` or ``/opendosm``).
    """

    ENDPOINT: str

    def __init__(
        self,
        api_key: Optional[str] = None,
        retry_strategy: Optional[Retry] = None,
    ):
        headers = {"Authorization": f"Token {api_key}"} if api_key else None
        super().__init__(
            base_url=get_base_url(),
            headers=headers,
            retry_strategy=retry_strategy or DEFAULT_RETRY,
        )
        self.api_key = api_key

    def get_dataset(
        self,
        dataset_id: str,
        *,
        limit: Optional[int] = None,
        filter: Optional[str] = None,
        ifilter: Optional[str] = None,
        contains: Optional[str] = None,
        icontains: Optional[str] = None,
        range: Optional[str] = None,
        sort: Optional[str] = None,
        include: Optional[str] = None,
        exclude: Optional[str] = None,
        date_start: Optional[str] = None,
        date_end: Optional[str] = None,
        timestamp_start: Optional[str] = None,
        timestamp_end: Optional[str] = None,
        meta: bool = False,
    ) -> list[dict[str, Any]] | dict[str, Any]:
        """Fetch a dataset by ID with optional query filters.

        Args:
            dataset_id: The dataset identifier (e.g. ``"population_malaysia"``).
            limit: Maximum number of records to return.
            filter: Exact case-sensitive match (``"value@column"``).
            ifilter: Exact case-insensitive match (``"value@column"``).
            contains: Partial case-sensitive match (``"value@column"``).
            icontains: Partial case-insensitive match (``"value@column"``).
            range: Numeric range filter (``"column[begin:end]"``).
            sort: Sort order (``"column,-column2"``; dash = descending).
            include: Columns to include (comma-separated).
            exclude: Columns to exclude (comma-separated).
            date_start: Start date filter (``"YYYY-MM-DD"``).
            date_end: End date filter (``"YYYY-MM-DD"``).
            timestamp_start: Start timestamp filter (``"YYYY-MM-DD HH:MM:SS"``).
            timestamp_end: End timestamp filter (``"YYYY-MM-DD HH:MM:SS"``).
            meta: If ``True``, include metadata wrapper in response.

        Returns:
            A list of record dicts, or a dict with ``meta`` and ``data`` keys
            when ``meta=True``.
        """
        params: dict[str, Any] = {"id": dataset_id}

        # Collect all explicitly provided params, skipping None values
        optional: dict[str, Any] = {
            "limit": limit,
            "filter": filter,
            "ifilter": ifilter,
            "contains": contains,
            "icontains": icontains,
            "range": range,
            "sort": sort,
            "include": include,
            "exclude": exclude,
            "date_start": date_start,
            "date_end": date_end,
            "timestamp_start": timestamp_start,
            "timestamp_end": timestamp_end,
        }
        for key, value in optional.items():
            if value is not None:
                params[key] = value

        if meta:
            params["meta"] = "true"

        logger.debug("Fetching dataset %s from %s", dataset_id, self.ENDPOINT)
        return self.get(self.ENDPOINT, params=params).json()

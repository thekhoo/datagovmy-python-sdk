---
name: SDK Patterns and Conventions
description: Established naming, structure, return type, and error handling patterns in the datagovmy SDK as of post-v1.0.1 DX fixes
type: project
---

## Package structure

- Module directory is `datagovmy/` (importable as `datagovmy`), not `mydata/`
- Public entry point: `from datagovmy import DataGovMyClient`
- Sub-clients live in `datagovmy/service/`: `DataCatalogueClient`, `OpenDOSMClient`
- Shared base for JSON dataset endpoints: `DataEndpointClient` in `datagovmy/service/data_endpoint.py`
- HTTP core in `datagovmy/core/api.py`: `BaseAPIClient` (requests-based, sync only)
- Exceptions in `datagovmy/service/exceptions.py`
- Environment helpers in `datagovmy/service/environment.py`

## Naming conventions established

- Top-level client: `DataGovMyClient` (facade, lazy-init sub-clients via properties)
- Sub-clients: `DataCatalogueClient`, `OpenDOSMClient` (accessed via `.data_catalogue`, `.opendosm`)
- Primary data-fetch method: `get_dataset(dataset_id, *, ...)` — keyword-only params after first positional

## Return type conventions

- `get_dataset` returns `list[dict[str, Any]] | dict[str, Any]` (raw parsed JSON, no typed models)
- When `meta=True`, return shape changes to `{"meta": {...}, "data": [...]}` — this is a DX concern (union return type)
- `BaseAPIClient.get/post/put/delete` return raw `requests.Response`

## Error handling

- `BaseAPIClient._request` wraps `requests.exceptions.HTTPError` into SDK exceptions
- Exception hierarchy:
  - `DataGovMyError` (base)
  - `APIError(DataGovMyError)` — carries `status_code` and `response` attributes
  - `RateLimitError(APIError)` — HTTP 429, default message "Rate limit exceeded"
  - `NotFoundError(APIError)` — HTTP 404, default message "Resource not found"
  - `AuthenticationError(APIError)` — HTTP 401/403
- All SDK exceptions are exported from `datagovmy.__init__` for catchability

## Auth pattern

- `api_key` passed to `DataGovMyClient(api_key=...)`, forwarded to sub-clients
- Auth header is now correctly set: `Authorization: Token <key>` via session headers in `DataEndpointClient.__init__`

## HTTP client

- Uses `requests` (sync only); httpx async support not yet implemented
- Default retry strategy (`DEFAULT_RETRY`) is defined in `data_endpoint.py`:
  - `total=3`, `status_forcelist=[429, 500, 502, 503, 504]`, `backoff_factor=1`, `allowed_methods=["GET"]`
- Can be overridden per-client via `retry_strategy` constructor parameter

## Query parameter handling

- All filter params are explicit keyword-only arguments in `get_dataset`
- Params are passed as a `dict` to `requests` (proper URL encoding, no manual string concatenation)
- `meta` is a `bool` param, converted to the string `"true"` only when `True`; omitted entirely when `False`

## Known DX issues flagged in review (post-v1.0.1 fixes)

- `filter` and `range` shadow Python builtins as parameter names
- `dataset_id` positional param name differs from `id` in the API — subtle but reasonable
- Return type `list[dict] | dict` is imprecise; a `meta=True` response has a distinct shape that isn't surfaced in typing
- `retry_strategy` constructor param exposes `urllib3.Retry` directly — a leaky abstraction for most users
- `RateLimitError` can still be raised if retries are exhausted; this is not documented
- `response` attribute on exceptions is untyped (`response=None`, no hint it's a `requests.Response`)
- `DataEndpointClient` is not exported from `__init__` (intentionally internal, but useful for type-checking advanced users)
- `post`, `put`, `delete` methods on `BaseAPIClient` are dead weight for a read-only SDK

**Why to apply:** Use these as the baseline when reviewing new additions for consistency.

---
name: Project Architecture
description: SDK structure, auth pattern, HTTP client stack, and key file locations
type: project
---

**SDK:** datagovmy-python-sdk — read-only GET SDK for Malaysia's data.gov.my Open API.

**HTTP stack:** `requests` + `urllib3` Retry. No async support currently.

**Key files:**
- `datagovmy/core/api.py` — `BaseAPIClient`: session management, error wrapping, retry mounting
- `datagovmy/service/data_endpoint.py` — `DataEndpointClient`: auth header injection, query param construction, DEFAULT_RETRY
- `datagovmy/service/data_catalogue.py` / `open_dosm.py` — thin subclasses, set `ENDPOINT`
- `datagovmy/datagovmy.py` — `DataGovMyClient` facade; lazily instantiates sub-clients
- `datagovmy/service/exceptions.py` — exception hierarchy rooted at `DataGovMyError`
- `datagovmy/service/environment.py` — `get_base_url()` returns hardcoded base URL (no env var currently)

**Auth pattern:** Optional bearer-style token — `Authorization: Token <api_key>`. Token stored on instance as `self.api_key` and in session headers. No token = anonymous (4 req/min), token = 10 req/min.

**Retry:** DEFAULT_RETRY retries 429/5xx up to 3 times with backoff_factor=1. Applies only to GET.

**Dependencies:** `requests` (unpinned), dev deps include `pytest`, `ruff`, `requests-mock`, `pyrefly`.

---
name: Security Patterns and Findings
description: Known security posture, confirmed findings, and conventions observed in this codebase
type: project
---

## Confirmed secure practices
- Auth token injected via `requests.Session` headers dict — never concatenated into URLs or logged
- Query params built via `requests` `params=` dict — URL encoding handled by the library, no string concatenation
- Error messages expose only the HTTP status code integer, not response body content
- Exception hierarchy (`DataGovMyError > APIError > *`) allows callers to catch at appropriate granularity
- `response` object stored on exceptions gives callers raw access without the SDK leaking body text itself
- `get_base_url()` isolates the base URL; base URL is hardcoded HTTPS only — no HTTP downgrade path for production traffic
- Retry strategy restricts retries to GET only (`allowed_methods=["GET"]`) — safe for idempotent calls

## Known issues / areas to watch (from first review, 2026-03-29)

### Medium — api_key stored as plaintext instance attribute
- `DataEndpointClient.__init__` stores `self.api_key = api_key` after placing it in session headers.
- The attribute is redundant (never read after construction) and increases the window where the token lives in memory and is accessible via `repr`/`vars()`.
- Recommendation: remove `self.api_key`; the session already holds the header.

### Medium — `requests` dependency unpinned
- `pyproject.toml` lists `requests` with no version constraint.
- Supply chain risk: a compromised or breaking upstream release is pulled automatically.
- Recommendation: pin to a minimum tested version (e.g. `requests>=2.31,<3`).

### Low — `response` object on exceptions carries full HTTP response body
- `APIError.response` stores the raw `requests.Response`. Callers who log `str(exc)` only see the safe message, but callers who log `exc.response.text` or `repr(exc)` could inadvertently log API error bodies.
- Not a direct SDK vulnerability, but worth documenting in exception class docstrings.

### Low — debug log emits full URL including all query params
- `logger.debug("Requesting %s %s", method, url)` in `BaseAPIClient._request` logs the fully constructed URL.
- Query params (dataset IDs, filter values) appear in debug logs. Not a secret, but worth noting for environments that forward logs externally.

### Low — `get_base_url()` returns a hardcoded string with no env override
- The function exists as the correct indirection point (per CLAUDE.md convention) but currently provides no runtime configurability.
- If a developer ever needs to point at a staging API, they must patch code. Low risk now; technical debt for the future.

### Informational — `BaseAPIClient` exposes POST/PUT/DELETE methods
- The API is read-only (GET only per spec), but `BaseAPIClient` exposes `post`, `put`, `delete`.
- No security issue if callers use `DataEndpointClient`, but the base class surface is broader than needed.

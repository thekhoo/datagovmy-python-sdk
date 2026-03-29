# CLAUDE.md — datagovmy-python-sdk

## Project Overview

Unofficial Python SDK for accessing open data from Malaysia's [data.gov.my](https://data.gov.my) platform via their [Open API](https://developer.data.gov.my/).

**Package name:** `mydata` (importable module in `mydata/`)
**Python:** >=3.13 (managed via `.python-version`)
**Build system:** Standard `pyproject.toml` (no build backend specified yet)

## API Reference (data.gov.my)

Base URL: `https://api.data.gov.my`

## Always do this

- When implementing a feature, always come up with a plan before making any code changes
- If requirements are not clear, always ask for clarity - never assume
- Always use TDD to implement new features
- After implementing features, trigger the sdk-dx-reviewer and security-code-reviewer agents to ensure DX remains good and no vulnaribilities are introduced
- After writing executable code, run the unit tests and linters and ensure all of them pass
- Always commit in small chunks. Unit tests and linters must pass before committing
- Be clear and concise with your code. I fthere are hidden implications, leave comments explaining why
- Make sure logs are written at difference code checkpoints. Do not be too verbose
- Use existing utility functions instead of re-implementing. Helper functions should be reusable in an appropriately named module

## Never do this

- Change main code when there are no unit tests that capture the functionality. add unit tests before making any changes
- Do not hardcode secrets or ARNs within the code. Any secrets should be taken from SSM
- Do not expose any tenanted information within the log messages

## Coding Conventions

### Environment

- All environment variable access should be done using helper functions in mydata/service/environment.py and not os.environ directly in the code.

### Endpoints

| Endpoint                                       | Returns  | Description                                   |
| ---------------------------------------------- | -------- | --------------------------------------------- |
| `GET /data-catalogue?id=<id>`                  | JSON     | National data catalogue datasets              |
| `GET /opendosm?id=<id>`                        | JSON     | Dept of Statistics (DOSM) datasets            |
| `GET /weather/forecast`                        | JSON     | 7-day weather forecast                        |
| `GET /weather/warning`                         | JSON     | Weather warnings                              |
| `GET /weather/warning/earthquake`              | JSON     | Earthquake warnings                           |
| `GET /gtfs-static/<agency>`                    | ZIP      | GTFS static feeds (ktmb, prasarana, mybas-\*) |
| `GET /gtfs-realtime/vehicle-position/<agency>` | Protobuf | Real-time vehicle positions                   |

### Authentication

- **Optional.** API works without a token (4 req/min).
- With token (10 req/min): `Authorization: Token <TOKEN>`

### Query Parameters (JSON endpoints)

| Param                               | Usage                                                      |
| ----------------------------------- | ---------------------------------------------------------- |
| `id`                                | Dataset identifier (required for data-catalogue/opendosm)  |
| `limit`                             | Max records to return                                      |
| `filter` / `ifilter`                | Exact match (case-sensitive / insensitive): `value@column` |
| `contains` / `icontains`            | Partial match: `value@column`                              |
| `range`                             | Numeric range: `column[begin:end]`                         |
| `sort`                              | Sort: `column,-column2` (dash = descending)                |
| `include` / `exclude`               | Select/omit columns                                        |
| `date_start` / `date_end`           | Date filter (`YYYY-MM-DD`)                                 |
| `timestamp_start` / `timestamp_end` | Timestamp filter (`YYYY-MM-DD HH:MM:SS`)                   |
| `meta=true`                         | Include metadata wrapper in response                       |

Multiple filters: comma-separated. Nested fields: double underscores (e.g. `location__location_name`).

### Response Format

- Success: JSON array of records (or `{"meta": {}, "data": []}` with `meta=true`)
- Error: `{"status": <int>, "errors": [...]}`
- Status codes: 200, 400, 404, 429, 500

### Rate Limits

- Without token: **4 requests/minute**
- With token: **10 requests/minute**
- Exceeding returns HTTP 429

## Development Guidelines

- All endpoints are **read-only GET** requests — the SDK only needs HTTP GET support.
- Use `httpx` or `requests` as the HTTP client (add to `pyproject.toml` dependencies).
- The SDK should support both sync and async usage patterns.
- Handle rate limiting gracefully (retry with backoff on 429).
- Dataset IDs can be discovered at https://data.gov.my/data-catalogue or https://open.dosm.gov.my/data-catalogue.

## Commands

```bash
# Run the project
uv run main.py

# Run tests (once added)
uv run pytest

# Install dependencies
uv sync
```

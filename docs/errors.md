# Error Handling

The SDK provides a hierarchy of exceptions so you can handle errors at the right granularity. All exceptions are importable from `datagovmy.exceptions`.

## Exception Hierarchy

```
DataGovMyError
└── APIError
    ├── RateLimitError      (HTTP 429)
    ├── NotFoundError       (HTTP 404)
    └── AuthenticationError (HTTP 401/403)
```

## Usage

### Catching specific errors

```python
from datagovmy import DataGovMyClient
from datagovmy.exceptions import NotFoundError, RateLimitError

client = DataGovMyClient()

try:
    data = client.data_catalogue.get_dataset("invalid_dataset_id")
except NotFoundError:
    print("Dataset not found")
except RateLimitError:
    print("Rate limited — try again later or add an API key")
```

### Catching all API errors

```python
from datagovmy.exceptions import APIError

try:
    data = client.data_catalogue.get_dataset("population_malaysia")
except APIError as e:
    print(f"API error (HTTP {e.status_code}): {e}")
```

### Catching all SDK errors

```python
from datagovmy.exceptions import DataGovMyError

try:
    data = client.data_catalogue.get_dataset("population_malaysia")
except DataGovMyError as e:
    print(f"Something went wrong: {e}")
```

## Exception Attributes

All `APIError` subclasses expose:

| Attribute | Type | Description |
|---|---|---|
| `status_code` | `int` | The HTTP status code from the API |
| `response` | `requests.Response` or `None` | The raw response object for inspection |

## Automatic Retries

The SDK retries on HTTP 429 (rate limit) and 5xx (server error) responses automatically with exponential backoff — up to 3 retries by default. A `RateLimitError` is only raised after all retries are exhausted.

You can customise the retry strategy:

```python
from urllib3.util.retry import Retry
from datagovmy.service.data_catalogue import DataCatalogueClient

custom_retry = Retry(total=5, status_forcelist=[429], backoff_factor=2)
client = DataCatalogueClient(api_key="your-key", retry_strategy=custom_retry)
```

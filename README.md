# Data.gov.my Python SDK

Unofficial SDK for accessing open source data on https://data.gov.my.

## Installation

```bash
pip install datagovmy-python-sdk
```

## Quick Start

```python
from datagovmy import DataGovMyClient

client = DataGovMyClient()

# Fetch a dataset from the national data catalogue
data = client.data_catalogue.get_dataset("population_malaysia")

# Fetch with filters
data = client.data_catalogue.get_dataset(
    "population_malaysia",
    filter="Selangor@location",
    sort="-year",
    limit=10,
)

# Fetch DOSM data
data = client.opendosm.get_dataset("cpi_2d_category")
```

## Documentation

- [Usage Guide](docs/usage.md) — query filters, sorting, pagination, date ranges, column selection, and more
- [Error Handling](docs/errors.md) — SDK exceptions and how to handle them

## API Reference

This SDK wraps the [data.gov.my Open API](https://developer.data.gov.my/). Dataset IDs can be discovered at:

- [data.gov.my Data Catalogue](https://data.gov.my/data-catalogue)
- [OpenDOSM Data Catalogue](https://open.dosm.gov.my/data-catalogue)

## Rate Limits

- Without API key: **4 requests/minute**
- With API key: **10 requests/minute**

The SDK automatically retries on rate limit errors (HTTP 429) with exponential backoff (up to 3 retries).

```python
client = DataGovMyClient(api_key="your-api-key")
```

## License

MIT

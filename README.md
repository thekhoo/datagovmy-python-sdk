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
data = client.data_catalogue.get_dataset_as_json(id="population_malaysia")

# Fetch with filters
data = client.data_catalogue.get_dataset_as_json(
    id="population_malaysia",
    filter="Selangor@location",
    sort="-year",
    limit=10
)

# Fetch DOSM data
data = client.opendosm.get_dataset_as_json(id="cpi_2d_category")
```

## Documentation

For detailed usage examples including all supported query filters (filtering, sorting, pagination, date ranges, column selection, and more), see the [Usage Guide](docs/usage.md).

## API Reference

This SDK wraps the [data.gov.my Open API](https://developer.data.gov.my/). Dataset IDs can be discovered at:

- [data.gov.my Data Catalogue](https://data.gov.my/data-catalogue)
- [OpenDOSM Data Catalogue](https://open.dosm.gov.my/data-catalogue)

## Rate Limits

- Without API key: **4 requests/minute**
- With API key: **10 requests/minute**

```python
client = DataGovMyClient(api_key="your-api-key")
```

## License

MIT

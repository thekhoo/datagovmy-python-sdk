# Usage Guide

This guide covers how to use `DataGovMyClient` to query datasets from [data.gov.my](https://data.gov.my).

## Setup

```python
from datagovmy import DataGovMyClient

client = DataGovMyClient()
```

## Basic Usage (No Filters)

### Fetch a Data Catalogue dataset

```python
# Fetch population data
data = client.data_catalogue.get_dataset("population_malaysia")
print(data)
```

### Fetch an Open DOSM dataset

```python
# Fetch CPI data from DOSM
data = client.opendosm.get_dataset("cpi_2d_category")
print(data)
```

## Using Filters

All query parameters from the [data.gov.my API](https://developer.data.gov.my/request-query) are supported as keyword-only arguments.

### Limit results

```python
# Get only the first 5 records
data = client.data_catalogue.get_dataset("population_malaysia", limit=5)
```

### Exact match filter (`filter`)

Case-sensitive exact match on a column value. Format: `value@column`.

```python
# Filter population data for Malaysia only
data = client.data_catalogue.get_dataset(
    "population_malaysia",
    filter="Malaysia@location",
)
```

### Case-insensitive filter (`ifilter`)

```python
# Case-insensitive exact match
data = client.data_catalogue.get_dataset(
    "population_malaysia",
    ifilter="malaysia@location",
)
```

### Partial match (`contains` / `icontains`)

```python
# Case-sensitive partial match
data = client.data_catalogue.get_dataset(
    "population_malaysia",
    contains="Sela@location",
)

# Case-insensitive partial match
data = client.data_catalogue.get_dataset(
    "population_malaysia",
    icontains="sela@location",
)
```

### Range filter

Filter numeric values within an inclusive range. Format: `column[begin:end]`.

```python
# Filter records where year is between 2010 and 2020
data = client.data_catalogue.get_dataset(
    "population_malaysia",
    range="year[2010:2020]",
)
```

### Sorting

Sort by one or more columns. Prefix with `-` for descending order.

```python
# Sort by year ascending
data = client.data_catalogue.get_dataset("population_malaysia", sort="year")

# Sort by year descending
data = client.data_catalogue.get_dataset("population_malaysia", sort="-year")

# Sort by multiple columns
data = client.data_catalogue.get_dataset("population_malaysia", sort="location,-year")
```

### Date range filtering

```python
# Filter by date range (YYYY-MM-DD)
data = client.data_catalogue.get_dataset(
    "population_malaysia",
    date_start="2020-01-01",
    date_end="2023-12-31",
)
```

### Timestamp range filtering

```python
# Filter by timestamp range (YYYY-MM-DD HH:MM:SS)
data = client.data_catalogue.get_dataset(
    "weather_forecast",
    timestamp_start="2024-01-01 00:00:00",
    timestamp_end="2024-01-07 23:59:59",
)
```

### Column selection (`include` / `exclude`)

```python
# Only include specific columns
data = client.data_catalogue.get_dataset(
    "population_malaysia",
    include="year,population",
)

# Exclude specific columns
data = client.data_catalogue.get_dataset(
    "population_malaysia",
    exclude="population_male,population_female",
)
```

### Include metadata

```python
# Get response with metadata wrapper
data = client.data_catalogue.get_dataset("population_malaysia", meta=True)
# Returns: {"meta": {...}, "data": [...]}
```

## Combining Multiple Filters

You can combine any of the above parameters in a single call:

```python
# Get the 10 most recent records for Selangor
data = client.data_catalogue.get_dataset(
    "population_malaysia",
    filter="Selangor@location",
    sort="-year",
    limit=10,
    include="year,location,population",
)
```

```python
# DOSM data with filters
data = client.opendosm.get_dataset(
    "cpi_2d_category",
    date_start="2023-01-01",
    date_end="2023-12-31",
    sort="-date",
    limit=20,
)
```

## Multiple filter values

Use commas to apply multiple filters of the same type:

```python
# Filter for multiple locations
data = client.data_catalogue.get_dataset(
    "population_malaysia",
    filter="Selangor@location,2020@year",
)
```

## Query Parameter Reference

| Parameter | Format | Description |
|---|---|---|
| `dataset_id` | `str` | Dataset identifier (positional argument) |
| `limit` | `int` | Max records to return |
| `filter` | `value@column` | Exact match (case-sensitive) |
| `ifilter` | `value@column` | Exact match (case-insensitive) |
| `contains` | `value@column` | Partial match (case-sensitive) |
| `icontains` | `value@column` | Partial match (case-insensitive) |
| `range` | `column[begin:end]` | Inclusive numeric range |
| `sort` | `column,-column2` | Sort (prefix `-` for descending) |
| `include` | `col1,col2` | Select columns to return |
| `exclude` | `col1,col2` | Omit columns from response |
| `date_start` | `YYYY-MM-DD` | Start of date range |
| `date_end` | `YYYY-MM-DD` | End of date range |
| `timestamp_start` | `YYYY-MM-DD HH:MM:SS` | Start of timestamp range |
| `timestamp_end` | `YYYY-MM-DD HH:MM:SS` | End of timestamp range |
| `meta` | `bool` | Include metadata in response (`True`/`False`) |

For more details, see the [official API documentation](https://developer.data.gov.my/request-query).

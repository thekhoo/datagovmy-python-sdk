import pytest
import requests_mock
from requests.adapters import HTTPAdapter

from datagovmy.service.data_catalogue import DataCatalogueClient

BASE_URL = "https://api.data.gov.my"


@pytest.fixture
def client():
    return DataCatalogueClient()


@pytest.fixture
def auth_client():
    return DataCatalogueClient(api_key="test-token")


# --- Issue 1: Auth header passthrough ---


def test_auth_header_sent_when_api_key_provided(auth_client):
    with requests_mock.Mocker() as m:
        m.get(f"{BASE_URL}/data-catalogue", json=[])
        auth_client.get_dataset("population_malaysia")
    assert m.last_request.headers["Authorization"] == "Token test-token"


def test_no_auth_header_when_no_api_key(client):
    with requests_mock.Mocker() as m:
        m.get(f"{BASE_URL}/data-catalogue", json=[])
        client.get_dataset("population_malaysia")
    assert "Authorization" not in m.last_request.headers


# --- Issue 2: Query params via params dict (proper URL encoding) ---


def test_id_passed_as_query_param(client):
    with requests_mock.Mocker() as m:
        m.get(f"{BASE_URL}/data-catalogue", json=[])
        client.get_dataset("population_malaysia")
    assert "id=population_malaysia" in m.last_request.url


def test_special_characters_in_filter_are_encoded(client):
    """Values with spaces/special chars should be URL-encoded, not broken."""
    with requests_mock.Mocker() as m:
        m.get(f"{BASE_URL}/data-catalogue", json=[])
        client.get_dataset("population_malaysia", filter="Kuala Lumpur@location")
    # Space should be encoded as + or %20, not left raw
    assert "Kuala" in m.last_request.url
    assert " " not in m.last_request.url.split("?", 1)[1]


# --- Issue 3: Default retry on 429 ---


def test_default_retry_strategy_configured(client):
    adapter = client.session.get_adapter("https://api.data.gov.my")
    assert isinstance(adapter, HTTPAdapter)
    assert adapter.max_retries.total == 3
    assert 429 in adapter.max_retries.status_forcelist


def test_custom_retry_strategy_overrides_default():
    from urllib3.util.retry import Retry

    custom = Retry(total=1, status_forcelist=[500])
    client = DataCatalogueClient(retry_strategy=custom)
    adapter = client.session.get_adapter("https://api.data.gov.my")
    assert isinstance(adapter, HTTPAdapter)
    assert adapter.max_retries.total == 1


# --- Issue 5: Renamed method ---


def test_get_dataset_returns_json(client):
    with requests_mock.Mocker() as m:
        m.get(f"{BASE_URL}/data-catalogue", json=[{"id": 1}])
        result = client.get_dataset("population_malaysia")
    assert result == [{"id": 1}]


def test_get_dataset_as_json_no_longer_exists(client):
    assert not hasattr(client, "get_dataset_as_json")


# --- Issue 6: Explicit query parameters ---


def test_limit_param(client):
    with requests_mock.Mocker() as m:
        m.get(f"{BASE_URL}/data-catalogue", json=[])
        client.get_dataset("population_malaysia", limit=10)
    assert "limit=10" in m.last_request.url


def test_filter_param(client):
    with requests_mock.Mocker() as m:
        m.get(f"{BASE_URL}/data-catalogue", json=[])
        client.get_dataset("population_malaysia", filter="value@col")
    assert "filter=value%40col" in m.last_request.url


def test_sort_param(client):
    with requests_mock.Mocker() as m:
        m.get(f"{BASE_URL}/data-catalogue", json=[])
        client.get_dataset("population_malaysia", sort="date,-value")
    assert "sort=date" in m.last_request.url


def test_date_range_params(client):
    with requests_mock.Mocker() as m:
        m.get(f"{BASE_URL}/data-catalogue", json=[])
        client.get_dataset("population_malaysia", date_start="2020-01-01", date_end="2023-12-31")
    assert "date_start=2020-01-01" in m.last_request.url
    assert "date_end=2023-12-31" in m.last_request.url


def test_meta_bool_converted_to_string(client):
    """meta=True should be sent as meta=true (string) to the API."""
    with requests_mock.Mocker() as m:
        m.get(f"{BASE_URL}/data-catalogue", json={"meta": {}, "data": []})
        client.get_dataset("population_malaysia", meta=True)
    assert "meta=true" in m.last_request.url.lower()


def test_meta_false_not_sent(client):
    """meta=False (default) should not appear in query params."""
    with requests_mock.Mocker() as m:
        m.get(f"{BASE_URL}/data-catalogue", json=[])
        client.get_dataset("population_malaysia")
    assert "meta" not in m.last_request.url


def test_none_params_excluded(client):
    """Parameters left as None should not appear in the URL."""
    with requests_mock.Mocker() as m:
        m.get(f"{BASE_URL}/data-catalogue", json=[])
        client.get_dataset("population_malaysia", limit=5)
    url = m.last_request.url
    assert "filter" not in url
    assert "sort" not in url
    assert "date_start" not in url


def test_include_exclude_params(client):
    with requests_mock.Mocker() as m:
        m.get(f"{BASE_URL}/data-catalogue", json=[])
        client.get_dataset("population_malaysia", include="col1,col2", exclude="col3")
    assert "include=col1" in m.last_request.url
    assert "exclude=col3" in m.last_request.url


def test_timestamp_params(client):
    with requests_mock.Mocker() as m:
        m.get(f"{BASE_URL}/data-catalogue", json=[])
        client.get_dataset("population_malaysia", timestamp_start="2020-01-01 00:00:00")
    # Space should be encoded
    assert "timestamp_start=2020-01-01" in m.last_request.url


def test_contains_and_icontains_params(client):
    with requests_mock.Mocker() as m:
        m.get(f"{BASE_URL}/data-catalogue", json=[])
        client.get_dataset("population_malaysia", contains="val@col", icontains="val2@col2")
    assert "contains=" in m.last_request.url
    assert "icontains=" in m.last_request.url


def test_range_param(client):
    with requests_mock.Mocker() as m:
        m.get(f"{BASE_URL}/data-catalogue", json=[])
        client.get_dataset("population_malaysia", range="col[1:10]")
    assert "range=" in m.last_request.url

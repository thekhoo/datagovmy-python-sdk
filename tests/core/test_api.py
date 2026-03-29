import pytest
import requests_mock
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from datagovmy.core.api import BaseAPIClient
from datagovmy.exceptions import (
    APIError,
    AuthenticationError,
    DataGovMyError,
    NotFoundError,
    RateLimitError,
)

BASE_URL = "https://api.example.com"


@pytest.fixture
def client():
    return BaseAPIClient(base_url=BASE_URL)


@pytest.fixture
def retry_client():
    retry_strategy = Retry(
        total=2,
        status_forcelist=[429, 500],
        backoff_factor=0,  # no delay in tests
    )
    return BaseAPIClient(base_url=BASE_URL, retry_strategy=retry_strategy)


# --- GET ---


def test_get_request(client):
    with requests_mock.Mocker() as m:
        m.get(f"{BASE_URL}/items", json={"data": [1, 2, 3]})
        response = client.get("/items")
    assert response.status_code == 200
    assert response.json() == {"data": [1, 2, 3]}


def test_get_with_params(client):
    with requests_mock.Mocker() as m:
        m.get(f"{BASE_URL}/items", json={"id": "123"})
        response = client.get("/items", params={"id": "123"})
    assert response.status_code == 200
    assert "id=123" in response.request.url


# --- POST ---


def test_post_request(client):
    with requests_mock.Mocker() as m:
        m.post(f"{BASE_URL}/items", json={"created": True}, status_code=201)
        response = client.post("/items", json={"name": "test"})
    assert response.status_code == 201
    assert response.json() == {"created": True}


# --- PUT ---


def test_put_request(client):
    with requests_mock.Mocker() as m:
        m.put(f"{BASE_URL}/items/1", json={"updated": True})
        response = client.put("/items/1", json={"name": "updated"})
    assert response.status_code == 200
    assert response.json() == {"updated": True}


# --- DELETE ---


def test_delete_request(client):
    with requests_mock.Mocker() as m:
        m.delete(f"{BASE_URL}/items/1", status_code=204)
        response = client.delete("/items/1")
    assert response.status_code == 204


# --- Headers ---


def test_custom_headers():
    client = BaseAPIClient(base_url=BASE_URL, headers={"Authorization": "Token abc123"})
    with requests_mock.Mocker() as m:
        m.get(f"{BASE_URL}/items", json=[])
        response = client.get("/items")
    assert response.request.headers["Authorization"] == "Token abc123"


def test_per_request_headers(client):
    with requests_mock.Mocker() as m:
        m.get(f"{BASE_URL}/items", json=[])
        response = client.get("/items", headers={"X-Custom": "value"})
    assert response.request.headers["X-Custom"] == "value"


# --- Retry configuration ---


def test_retry_strategy_mounted_on_session(retry_client):
    """Verify the retry strategy is properly configured on the session adapters."""
    https_adapter = retry_client.session.get_adapter("https://example.com")
    assert isinstance(https_adapter, HTTPAdapter)
    assert https_adapter.max_retries.total == 2
    assert 429 in https_adapter.max_retries.status_forcelist
    assert 500 in https_adapter.max_retries.status_forcelist


def test_no_retry_strategy_by_default(client):
    """Without a retry_strategy, the default adapter has no retries."""
    adapter = client.session.get_adapter("https://example.com")
    assert adapter.max_retries.total == 0


# --- Error handling (SDK exceptions) ---


def test_raises_api_error_on_generic_error(client):
    with requests_mock.Mocker() as m:
        m.get(f"{BASE_URL}/items", status_code=500)
        with pytest.raises(APIError) as exc_info:
            client.get("/items")
    assert exc_info.value.status_code == 500


def test_raises_rate_limit_error_on_429(client):
    with requests_mock.Mocker() as m:
        m.get(f"{BASE_URL}/items", status_code=429)
        with pytest.raises(RateLimitError) as exc_info:
            client.get("/items")
    assert exc_info.value.status_code == 429


def test_raises_not_found_error_on_404(client):
    with requests_mock.Mocker() as m:
        m.get(f"{BASE_URL}/items", status_code=404)
        with pytest.raises(NotFoundError) as exc_info:
            client.get("/items")
    assert exc_info.value.status_code == 404


def test_raises_authentication_error_on_401(client):
    with requests_mock.Mocker() as m:
        m.get(f"{BASE_URL}/items", status_code=401)
        with pytest.raises(AuthenticationError) as exc_info:
            client.get("/items")
    assert exc_info.value.status_code == 401


def test_raises_authentication_error_on_403(client):
    with requests_mock.Mocker() as m:
        m.get(f"{BASE_URL}/items", status_code=403)
        with pytest.raises(AuthenticationError) as exc_info:
            client.get("/items")
    assert exc_info.value.status_code == 403


def test_sdk_errors_are_catchable_as_base_error(client):
    """All SDK errors can be caught via DataGovMyError."""
    with requests_mock.Mocker() as m:
        m.get(f"{BASE_URL}/items", status_code=500)
        with pytest.raises(DataGovMyError):
            client.get("/items")

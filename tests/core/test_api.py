import pytest
import requests
import requests_mock
from urllib3.util.retry import Retry

from mydata.core.api import BaseAPIClient

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
    assert https_adapter.max_retries.total == 2
    assert 429 in https_adapter.max_retries.status_forcelist
    assert 500 in https_adapter.max_retries.status_forcelist


def test_no_retry_strategy_by_default(client):
    """Without a retry_strategy, the default adapter has no retries."""
    adapter = client.session.get_adapter("https://example.com")
    assert adapter.max_retries.total == 0


# --- Error handling ---


def test_raises_on_error_status(client):
    with requests_mock.Mocker() as m:
        m.get(f"{BASE_URL}/items", status_code=403)
        with pytest.raises(requests.exceptions.HTTPError):
            client.get("/items")

import requests_mock

from datagovmy.service.open_dosm import OpenDOSMClient

BASE_URL = "https://api.data.gov.my"


# --- Verify OpenDOSMClient uses the correct endpoint and inherits all fixes ---


def test_opendosm_uses_correct_endpoint():
    client = OpenDOSMClient()
    with requests_mock.Mocker() as m:
        m.get(f"{BASE_URL}/opendosm", json=[])
        client.get_dataset("gdp")
    assert "/opendosm" in m.last_request.url


def test_opendosm_auth_header():
    client = OpenDOSMClient(api_key="dosm-key")
    with requests_mock.Mocker() as m:
        m.get(f"{BASE_URL}/opendosm", json=[])
        client.get_dataset("gdp")
    assert m.last_request.headers["Authorization"] == "Token dosm-key"


def test_opendosm_explicit_params():
    client = OpenDOSMClient()
    with requests_mock.Mocker() as m:
        m.get(f"{BASE_URL}/opendosm", json=[])
        client.get_dataset("gdp", limit=5, sort="date")
    assert "limit=5" in m.last_request.url
    assert "sort=date" in m.last_request.url


def test_opendosm_default_retry():
    client = OpenDOSMClient()
    adapter = client.session.get_adapter("https://api.data.gov.my")
    assert adapter.max_retries.total == 3
    assert 429 in adapter.max_retries.status_forcelist

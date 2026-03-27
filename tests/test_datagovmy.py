from datagovmy import DataGovMyClient
from datagovmy.service.data_catalogue import DataCatalogueClient
from datagovmy.service.open_dosm import OpenDOSMClient


# --- Property access ---


def test_data_catalogue_returns_data_catalogue_client():
    client = DataGovMyClient()
    assert isinstance(client.data_catalogue, DataCatalogueClient)


def test_opendosm_returns_opendosm_client():
    client = DataGovMyClient()
    assert isinstance(client.opendosm, OpenDOSMClient)


# --- Lazy instantiation (same instance returned) ---


def test_data_catalogue_returns_same_instance():
    client = DataGovMyClient()
    assert client.data_catalogue is client.data_catalogue


def test_opendosm_returns_same_instance():
    client = DataGovMyClient()
    assert client.opendosm is client.opendosm


# --- API key passthrough ---


def test_data_catalogue_receives_api_key():
    client = DataGovMyClient(api_key="test-key")
    assert client.data_catalogue.api_key == "test-key"


def test_opendosm_receives_api_key():
    client = DataGovMyClient(api_key="test-key")
    assert client.opendosm.api_key == "test-key"


def test_no_api_key_by_default():
    client = DataGovMyClient()
    assert client.data_catalogue.api_key is None
    assert client.opendosm.api_key is None

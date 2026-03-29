from datagovmy.exceptions import (
    APIError,
    AuthenticationError,
    DataGovMyError,
    NotFoundError,
    RateLimitError,
)

# --- Hierarchy ---


def test_api_error_is_datagovmy_error():
    assert issubclass(APIError, DataGovMyError)


def test_rate_limit_error_is_api_error():
    assert issubclass(RateLimitError, APIError)


def test_not_found_error_is_api_error():
    assert issubclass(NotFoundError, APIError)


def test_authentication_error_is_api_error():
    assert issubclass(AuthenticationError, APIError)


# --- Attributes ---


def test_api_error_stores_status_code_and_response():
    err = APIError("bad", status_code=500, response="fake-resp")
    assert err.status_code == 500
    assert err.response == "fake-resp"
    assert str(err) == "bad"


def test_rate_limit_error_defaults():
    err = RateLimitError("slow down")
    assert err.status_code == 429
    assert err.response is None

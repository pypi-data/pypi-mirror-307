import pytest
import requests
from promptstudio_sdk.base import Base


def test_base_initialization():
    # Test initialization with test environment
    base = Base({"api_key": "test_key", "env": "test"})
    assert base.api_key == "test_key"
    assert base.env == "test"
    assert base.bypass == False  # Default should be False
    assert base.base_url == "https://api.playground.promptstudio.dev/api/v1"

    # Test initialization with prod environment
    base = Base({"api_key": "test_key", "env": "prod"})
    assert base.api_key == "test_key"
    assert base.env == "prod"
    assert base.bypass == False
    assert base.base_url == "https://api.promptstudio.dev/api/v1"

    # Test initialization with bypass
    base = Base({"api_key": "test_key", "env": "test", "bypass": True})
    assert base.bypass == True


def test_request_headers():
    base = Base({"api_key": "test_key", "env": "test"})

    # Mock the requests.request method
    class MockResponse:
        def __init__(self, status_code):
            self.status_code = status_code
            self.ok = status_code == 200

        def raise_for_status(self):
            if not self.ok:
                raise requests.exceptions.HTTPError()

        def json(self):
            return {"data": "test"}

    def mock_request(method, url, headers, **kwargs):
        # Test that headers are correctly set
        assert headers["Content-Type"] == "application/json"
        assert headers["x-api-key"] == "test_key"
        return MockResponse(200)

    # Replace requests.request with our mock
    requests.request = mock_request

    # Make a test request
    response = base._request("/test")
    assert response == {"data": "test"}


def test_request_error_handling():
    base = Base({"api_key": "test_key", "env": "test"})

    # Mock the requests.request method to simulate an error
    def mock_error_request(method, url, headers, **kwargs):
        raise requests.exceptions.HTTPError("404 Client Error")

    # Replace requests.request with our mock
    requests.request = mock_error_request

    # Test that the error is properly raised
    with pytest.raises(requests.exceptions.HTTPError):
        base._request("/test")

import pytest
from pytest_httpx import HTTPXMock
from utils import create_mock
from src.server_utils import fetch_openapi_spec


@pytest.mark.asyncio
async def test_fetch_openapi_spec_valid(httpx_mock: HTTPXMock):
    """Test that the OpenAPI spec can be fetched and parsed correctly."""

    create_mock(httpx_mock, "insights")

    spec = await fetch_openapi_spec("https://dev.bandwidth.com/spec/insights.yml")

    assert isinstance(spec, dict), "Fetched spec should be a dictionary"
    assert "openapi" in spec, "Spec should contain 'openapi' key"
    assert "info" in spec, "Spec should contain 'info' key"
    assert "paths" in spec, "Spec should contain 'paths' key"


@pytest.mark.asyncio
async def test_fetch_openapi_spec_empty_yaml(httpx_mock: HTTPXMock):
    """Test that fetching an empty spec raises an error."""
    create_mock(httpx_mock, "empty")
    with pytest.raises(ValueError):
        await fetch_openapi_spec("https://dev.bandwidth.com/spec/empty.yml")


@pytest.mark.asyncio
async def test_fetch_openapi_spec_http_error():
    """Test that fetching an invalid URL raises an HTTP error."""
    with pytest.raises(RuntimeError):
        await fetch_openapi_spec("https://dev.bandwidth.com/spec/nonexistent.yml")


@pytest.mark.asyncio
async def test_fetch_openapi_spec_invalid_yaml():
    """Test that fetching an invalid YAML file raises a YAMLError."""
    with pytest.raises(RuntimeError):
        await fetch_openapi_spec("https://not-real-564987132489746sadfg.com")

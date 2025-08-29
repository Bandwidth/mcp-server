from pytest_httpx import HTTPXMock


def create_mock(httpx_mock: HTTPXMock, spec_name: str):
    """Helper function to create a mock response for HTTPX."""
    with open(f"test/fixtures/{spec_name}.yml", "r", encoding="utf-8") as f:
        response_text = f.read()
    httpx_mock.add_response(
        url=f"https://dev.bandwidth.com/spec/{spec_name}.yml", text=response_text
    )

from fastmcp import FastMCP
from httpx import AsyncClient
from typing import Dict, List, Optional, Callable, Any

from server_utils import (
    add_resources,
    create_route_map_fn,
    create_auth_header,
    fetch_openapi_spec,
    print_server_info,
)

api_server_info: Dict[str, Dict[str, Any]] = {
    "messaging": {"url": "https://dev.bandwidth.com/spec/messaging.yml"},
    "multi-factor-auth": {
        "url": "https://dev.bandwidth.com/spec/multi-factor-auth.yml"
    },
    "phone-number-lookup": {
        "url": "https://dev.bandwidth.com/spec/phone-number-lookup.yml"
    },
    "insights": {"url": "https://dev.bandwidth.com/spec/insights.yml"},
    "end-user-management": {
        "url": "https://dev.bandwidth.com/spec/end-user-management.yml"
    },
}


async def _create_server(
    url: str, route_map_fn: Optional[Callable] = None, config: Dict[str, Any] = {}
) -> FastMCP:
    """Create an MCP server from the provided spec URL and credentials."""
    # Fetch and clean the OpenAPI spec
    spec_object = await fetch_openapi_spec(url)

    # Validate spec structure
    if "servers" not in spec_object or not spec_object["servers"]:
        raise ValueError(f"OpenAPI spec from {url} has no servers defined")

    base_url = spec_object["servers"][0]["url"]
    auth_b64 = create_auth_header(config["BW_USERNAME"], config["BW_PASSWORD"])

    client = AsyncClient(
        base_url=base_url,
        headers={
            "Authorization": f"Basic {auth_b64}",
            "User-Agent": "Bandwidth MCP Server",
        },
    )

    mcp = FastMCP.from_openapi(
        openapi_spec=spec_object,
        client=client,
        name="Bandwidth",
        route_map_fn=route_map_fn,
    )

    return mcp


async def create_bandwidth_mcp(
    mcp: FastMCP,
    enabled_tools: Optional[List[str]],
    excluded_tools: Optional[List[str]],
    config: Dict[str, Any] = {},
) -> FastMCP:
    """Create the Bandwidth MCP server from all supplied APIs, taking into account enabled and excluded APIs.

    Args:
        mcp: The FastMCP instance to import servers into
        enabled_tools: List of tools to enable. If None, all tools are enabled.
        excluded_tools: List of tools to exclude. Takes priority over enabled_tools.
        config: Configuration dictionary containing API credentials and other variables.

    Returns:
        The FastMCP instance with all API servers imported and resources added.

    Raises:
        RuntimeError: If any API server fails to create or import
    """
    route_map_fn = create_route_map_fn(enabled_tools, excluded_tools)

    for api_name, api_info in api_server_info.items():
        try:
            server = await _create_server(
                api_info["url"], route_map_fn=route_map_fn, config=config
            )
            await mcp.import_server(server)
        except Exception as e:
            print(f"Warning: Failed to create server for {api_name}: {e}")

    add_resources(mcp, config)
    await print_server_info(mcp)

    return mcp

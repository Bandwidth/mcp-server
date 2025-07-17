from fastmcp import FastMCP
from httpx import AsyncClient
from resources import get_bandwidth_resources
from typing import Dict, List, Optional, Callable, Any
from utils import (
    get_config,
    create_route_map_fn,
    create_auth_header,
    fetch_openapi_spec
)

api_server_info: Dict[str, Dict[str, Any]] = {
    "messaging": {
        "url": "https://dev.bandwidth.com/spec/messaging.yml"
    },
    "multi-factor-auth": {
        "url": "https://dev.bandwidth.com/spec/multi-factor-auth.yml"
    },
    "phone-number-lookup": {
        "url": "https://dev.bandwidth.com/spec/phone-number-lookup.yml"
    },
    "insights": {
        "url": "https://dev.bandwidth.com/spec/insights.yml"
    }
}


async def _create_server(
    url: str,
    route_map_fn: Optional[Callable] = None
) -> FastMCP:
    """Create an MCP server from the provided spec URL and credentials."""
    # Fetch and clean the OpenAPI spec
    spec_object = await fetch_openapi_spec(url)
    
    # Validate spec structure
    if "servers" not in spec_object or not spec_object["servers"]:
        raise ValueError(f"OpenAPI spec from {url} has no servers defined")
    
    config = get_config()
    base_url = spec_object["servers"][0]["url"]
    auth_b64 = create_auth_header(config["username"], config["password"])

    client = AsyncClient(
        base_url=base_url,
        headers={
            "Authorization": f"Basic {auth_b64}",
        }
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
    excluded_tools: Optional[List[str]]
) -> FastMCP:
    """Create the Bandwidth MCP server from all supplied APIs, taking into account enabled and excluded APIs.
    
    Args:
        mcp: The FastMCP instance to import servers into
        enabled_tools: List of tools to enable. If None, all tools are enabled.
        excluded_tools: List of tools to exclude. Takes priority over enabled_tools.
        
    Returns:
        The FastMCP instance with all API servers imported
        
    Raises:
        RuntimeError: If any API server fails to create or import
    """
    route_map_fn = create_route_map_fn(enabled_tools, excluded_tools)
    
    for api_name, api_info in api_server_info.items():
        try:
            server = await _create_server(
                api_info["url"],
                route_map_fn=route_map_fn
            )
            await mcp.import_server(server)
        except Exception as e:
            print(f"Warning: Failed to create server for {api_name}: {e}")

    for resource in get_bandwidth_resources():
        try:
            mcp.add_resource(resource)
        except Exception as e:
            print(f"Warning: Failed to import resource {resource.name}: {e}")
    
    return mcp

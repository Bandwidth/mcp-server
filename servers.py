import yaml
import httpx
import base64
import requests
from fastmcp import FastMCP
from utils import username, password, clean_openapi_spec, filter_apis
from resources import number_order_guide_resource

api_server_info = {
    "messaging": {
        "url": "https://dev.bandwidth.com/spec/messaging.yml",
        "resources": [number_order_guide_resource]
    },
    "multi-factor-auth": {
        "url": "https://dev.bandwidth.com/spec/multi-factor-auth.yml",
        "resources": None
    },
    "phone-number-lookup": {
        "url": "https://dev.bandwidth.com/spec/phone-number-lookup.yml",
        "resources": None
    },
    "insights": {
        "url": "https://dev.bandwidth.com/spec/insights.yml",
        "resources": None
    }
}

def create_server(
    url: str,
    username: str = username,
    password: str = password,
    route_maps: list = None,
    resources: list = None
):
    """Create an MCP server from the provided spec URL and credentials."""
    spec = requests.get(url).text
    spec_object = clean_openapi_spec(yaml.safe_load(spec))

    auth_bytes = f"{username}:{password}".encode('utf-8')
    auth_b64 = base64.b64encode(auth_bytes).decode('utf-8')

    client = httpx.AsyncClient(
        base_url=spec_object["servers"][0]["url"],
        headers={
            "Authorization": f"Basic {auth_b64}",
        }
    )

    mcp = FastMCP.from_openapi(
        openapi_spec=spec_object,
        client=client,
        name="Bandwidth",
        route_maps=route_maps,
    )

    if resources:
        for resource in resources:
            mcp.add_resource(resource)

    return mcp


async def create_bandwidth_mcp(mcp: FastMCP, enabled_apis: list | None, excluded_apis: list | None):
    """Create the Bandwidth MCP server from all supplied APIs, taking into account enabled and excluded APIs."""
    all_apis = list(api_server_info.keys())
    filtered_apis = filter_apis(all_apis, enabled_apis, excluded_apis)

    for api in filtered_apis:
        api_info = api_server_info[api]
        server = create_server(api_info["url"], resources=api_info["resources"])
        await mcp.import_server(server)

    return mcp

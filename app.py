import asyncio

from fastmcp import FastMCP

from utils import get_enabled_apis, get_excluded_apis
from resources import config_resource
from servers import create_bandwidth_mcp

mcp = FastMCP(name="Bandwidth MCP")

# Initialize the Bandwidth API client
async def setup(mcp: FastMCP = mcp):
    enabled_apis = get_enabled_apis()
    excluded_apis = get_excluded_apis()

    await create_bandwidth_mcp(
        mcp,
        enabled_apis,
        excluded_apis
    )

mcp.add_resource(config_resource)

if __name__ == "__main__":
    asyncio.run(setup())
    mcp.run()

import asyncio

from fastmcp import FastMCP
from servers import create_bandwidth_mcp
from utils import get_enabled_tools, get_excluded_tools, print_server_info

mcp = FastMCP(name="Bandwidth MCP")

# Initialize the Bandwidth API client
async def setup(mcp: FastMCP = mcp):
    enabled_tools = get_enabled_tools()
    excluded_tools = get_excluded_tools()

    await create_bandwidth_mcp(mcp, enabled_tools, excluded_tools)
    await print_server_info(mcp)


if __name__ == "__main__":
    asyncio.run(setup())
    mcp.run()

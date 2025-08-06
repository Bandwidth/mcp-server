import asyncio

from fastmcp import FastMCP
from servers import create_bandwidth_mcp
from utils import get_enabled_tools, get_excluded_tools, print_server_info

mcp = FastMCP(name="Bandwidth MCP")

# Initialize the Bandwidth API client
async def setup(mcp: FastMCP = mcp):
    enabled_tools = get_enabled_tools()
    excluded_tools = get_excluded_tools()

    print("Setting up Bandwidth MCP server...")
    await create_bandwidth_mcp(mcp, enabled_tools, excluded_tools)
    await print_server_info(mcp)

def main():
    """Main function to run the Bandwidth MCP server."""
    asyncio.run(setup())
    mcp.run()

if __name__ == "__main__":
    main()

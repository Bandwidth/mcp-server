import asyncio
from fastmcp import FastMCP
from servers import create_bandwidth_mcp
from config import load_config, get_enabled_tools, get_excluded_tools

mcp = FastMCP(name="Bandwidth MCP")


async def setup(mcp: FastMCP = mcp):
    """Setup the Bandwidth MCP server with tools and resources."""
    enabled_tools = get_enabled_tools()
    excluded_tools = get_excluded_tools()
    config = load_config()

    print("Setting up Bandwidth MCP server...")
    await create_bandwidth_mcp(mcp, enabled_tools, excluded_tools, config)


def main():
    """Main function to run the Bandwidth MCP server."""
    asyncio.run(setup())
    mcp.run()


if __name__ == "__main__":
    main()

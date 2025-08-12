import pytest
from fastmcp import FastMCP
from src.servers import create_bandwidth_mcp, _create_server

async def create_mcp_server(name=None, tools=None, excluded_tools=None):
    """Fixture to create and return a FastMCP instance."""
    mcp = FastMCP(name=name or "Test MCP")
    config = {"BW_USERNAME": "test_user", "BW_PASSWORD": "test_pass"}
    enabled_tools = tools if tools is not None else []
    excluded_tools = excluded_tools if excluded_tools is not None else []
    
    await create_bandwidth_mcp(mcp, enabled_tools, excluded_tools, config)
    
    return mcp


def calculate_expected_tools(tools, excluded_tools, total_tools=19):
    if tools and not excluded_tools:
        return len(tools)
    elif excluded_tools:
        return total_tools - len(excluded_tools)
    else:
        return total_tools


server_configuration_list = [
    ([], []),
    ([], ["getReports", "createReport"]),
    (["createMessage"], []),
    (["generateMessagingCode", "generateVoiceCode"], []),
    (["createLookup", "getLookupStatus", "createMessage"], ["listCalls"]),
    (["listMedia"], ["uploadMedia", "deleteMedia", "getMedia"]),
]

@pytest.mark.skip
@pytest.mark.asyncio
@pytest.mark.parametrize("tools, excluded_tools", server_configuration_list)
async def test_full_mcp_server_creation(tools, excluded_tools):
    """Test that the MCP server is created correctly with included and excluded tools."""

    expected_tools = calculate_expected_tools(tools, excluded_tools)
    name = f"Test MCP with {expected_tools} Tools"
    
    mcp = await create_mcp_server(name, tools, excluded_tools)
    mcp_tools = await mcp.get_tools()
    mcp_tool_names = list(mcp_tools.keys())
    mcp_resources = await mcp.get_resources()

    assert isinstance(mcp, FastMCP)
    assert mcp.name == name, f"Expected MCP name '{name}', got '{mcp.name}'"
    assert len(mcp_tools) == expected_tools, f"Expected {expected_tools} tools, got {len(mcp_tools)}"
    assert len(mcp_resources) == 2, f"Expected 2 resources, got {len(mcp_resources)}"

    if excluded_tools:
        for tool in excluded_tools:
            assert tool not in mcp_tool_names, f"Excluded tool {tool} should not be present"

    if tools and not excluded_tools:
        for tool in tools:
            assert tool in mcp_tool_names, f"Enabled tool {tool} should be present"


spec_list = [
    (
        "https://dev.bandwidth.com/spec/multi-factor-auth.yml",
        {"BW_USERNAME": "test_user_mfa", "BW_PASSWORD": "test_pass_mfa"},
        "https://mfa.bandwidth.com/api/v1/",
        {"generateMessagingCode", "generateVoiceCode", "verifyCode"},
        "Basic dGVzdF91c2VyX21mYTp0ZXN0X3Bhc3NfbWZh"
    ),
    (
        "https://dev.bandwidth.com/spec/phone-number-lookup.yml",
        {"BW_USERNAME": "test_user_tnlookup", "BW_PASSWORD": "test_pass_tnlookup"},
        "https://numbers.bandwidth.com/api/v1/",
        {"createLookup", "getLookupStatus"},
        "Basic dGVzdF91c2VyX3RubG9va3VwOnRlc3RfcGFzc190bmxvb2t1cA=="
    )
]


@pytest.mark.asyncio
@pytest.mark.parametrize("url, config, expected_base_url, expected_tools, expected_auth_header", spec_list)
async def test_individual_mcp_server_creation(
    url,
    config,
    expected_base_url,
    expected_tools,
    expected_auth_header
):
    """Test that individual MCP servers are created correctly."""
    
    server = await _create_server(url, None, config)
    server_client = server._client
    
    server_tools = await server.get_tools()
    server_tool_names = set(server_tools.keys())

    assert isinstance(server, FastMCP)
    assert server.name == "Bandwidth", f"Expected server name to be 'Bandwidth', got '{server.name}'"
    assert server_tool_names == expected_tools, f"Expected tools {expected_tools}, got {server_tool_names}"
    assert server_client.headers["User-Agent"] == "Bandwidth MCP Server", \
        f"Expected User-Agent 'Bandwidth MCP Server', got '{server_client.headers['User-Agent']}'"
    assert server_client.base_url == expected_base_url, \
        f"Expected base URL '{expected_base_url}', got '{server_client.base_url}'"
    assert server_client.headers["Authorization"] == expected_auth_header, \
        f"Expected auth header '{expected_auth_header}', got '{server_client.headers['Authorization']}'"

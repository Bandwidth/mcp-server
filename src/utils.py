import os
import copy
import yaml
import httpx
import base64

from fastmcp import FastMCP
from dotenv import load_dotenv
from argparse import ArgumentParser, Namespace
from fastmcp.server.openapi import MCPType, HTTPRoute
from typing import Dict, List, Optional, Any, Callable

# ===== Config and Server Info =====
load_dotenv()

bandwidth_account_id = os.environ.get("BW_ACCOUNT_ID", None)
bandwidth_number = os.environ.get("BW_NUMBER", None)
bandwidth_messaging_application_id = os.environ.get("BW_MESSAGING_APPLICATION_ID", None)
bandwidth_voice_application_id = os.environ.get("BW_VOICE_APPLICATION_ID", None)
username = os.environ["BW_USERNAME"]
password = os.environ["BW_PASSWORD"].replace("\\", "")


def get_config() -> Dict[str, Any]:
    """Get the Bandwidth configuration"""
    return {
        "bandwidth_account_id": bandwidth_account_id,
        "bandwidth_number": bandwidth_number,
        "bandwidth_messaging_application_id": bandwidth_messaging_application_id,
        "bandwidth_voice_application_id": bandwidth_voice_application_id,
        "username": username,
        "password": password
    }


async def print_server_info(mcp: FastMCP) -> None:
    """Print concise server information."""
    try:
        all_tools = await mcp.get_tools()
        all_resources = await mcp.get_resources()
        
        tool_names = list(all_tools.keys())
        resource_names = [resource.name for resource in all_resources.values()]

        print("Bandwidth MCP Server Started")
        print(f"Tools ({len(tool_names)}): {', '.join(sorted(tool_names)) if tool_names else 'None'}")
        print(f"Resources ({len(resource_names)}): {', '.join(sorted(resource_names)) if resource_names else 'None'}")
        
    except Exception as e:
        print(f"Error retrieving server info: {e}")
        print("Server may still be functional")


# ===== Server Flags =====
def _parse_cli_args(args: Optional[List[str]] = None) -> Namespace:
    """Parse command line arguments with proper type hints."""
    parser = ArgumentParser(description="Bandwidth MCP Server")

    # Tools
    parser.add_argument(
        "--tools",
        help="Comma-separated list of tool names to enable. If not specified, all tools are enabled.",
        type=str,
    )
    parser.add_argument(
        "--exclude-tools",
        help="Comma-separated list of tool names to disable.",
        type=str,
    )

    return parser.parse_known_args(args)[0]


def _parse_arg_list(arg_string: str) -> List[str]:
    """Parse a comma-separated argument string into a list."""
    return [item.strip() for item in arg_string.split(",") if item.strip()]


def _parse_flags(cli_arg: Optional[str], env_var: str) -> Optional[List[str]]:
    """Get flag values from CLI argument or environment variable."""
    # Try CLI argument first
    if cli_arg:
        return _parse_arg_list(cli_arg)
    
    # Fall back to environment variable
    env_value = os.getenv(env_var)
    if env_value:
        return _parse_arg_list(env_value)
    
    return None


# ===== Tool Management =====
def get_enabled_tools() -> Optional[List[str]]:
    """Get the list of enabled tools from CLI args or environment variable."""
    args = _parse_cli_args()
    return _parse_flags(args.tools, "BW_MCP_TOOLS")


def get_excluded_tools() -> Optional[List[str]]:
    """Get the list of excluded tools from CLI args or environment variable."""
    args = _parse_cli_args()
    return _parse_flags(args.exclude_tools, "BW_MCP_EXCLUDE_TOOLS")


def create_route_map_fn(enabled_tools: Optional[List[str]], excluded_tools: Optional[List[str]]) -> Callable[[HTTPRoute, MCPType], MCPType]:
    """Create a route map function based on enabled and excluded tools.
    
    Args:
        enabled_tools: List of tools to enable. If None, all tools are enabled.
        excluded_tools: List of tools to exclude. Takes priority over enabled_tools.
        
    Returns:
        A function that maps routes to MCP types based on the tool configuration.
    """
    def route_map_fn(route: HTTPRoute, mcp_type: MCPType) -> MCPType:
        # Excluded tools have priority - if provided, ignore enabled tools
        if excluded_tools:
            return mcp_type if route.operation_id not in excluded_tools else MCPType.EXCLUDE
        if enabled_tools:
            return mcp_type if route.operation_id in enabled_tools else MCPType.EXCLUDE
            
        return mcp_type

    return route_map_fn


# ===== OpenAPI Spec Operations =====
def _clean_openapi_spec(spec: Dict[str, Any]) -> Dict[str, Any]:
    """Recursively clean OpenAPI spec:
    - Remove all callbacks
    - Remove all 4xx/5xx responses
    - Remove any field starting with 'x-'
    - Remove all path resources that start with 'x-'
    """
    cleaned_spec = copy.deepcopy(spec)
    
    def _clean(obj: Any) -> Any:
        if isinstance(obj, dict):
            # Remove 'callbacks' and 'x-' fields
            keys_to_remove = [k for k in obj if k == "callbacks" or k.startswith("x-")]
            for k in keys_to_remove:
                del obj[k]
            # Remove 4xx/5xx responses
            if "responses" in obj:
                codes_to_remove = [code for code in obj["responses"] 
                                 if str(code).startswith(("4", "5"))]
                for code in codes_to_remove:
                    del obj["responses"][code]
            # Special handling for paths
            if "paths" in obj:
                paths_to_remove = [p for p in obj["paths"] if p.startswith("x-")]
                for p in paths_to_remove:
                    del obj["paths"][p]
            # Recurse into all values
            for v in obj.values():
                _clean(v)
        elif isinstance(obj, list):
            for item in obj:
                _clean(item)
        return obj

    return _clean(cleaned_spec)


async def fetch_openapi_spec(url: str) -> Dict[str, Any]:
    """Fetch and parse OpenAPI spec from URL."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            spec_text = response.text
            
        spec_object = yaml.safe_load(spec_text)
        if not spec_object:
            raise ValueError(f"Empty or invalid YAML spec from {url}")
            
        return _clean_openapi_spec(spec_object)
    except httpx.HTTPError as e:
        raise RuntimeError(f"Failed to fetch OpenAPI spec from {url}: {e}") from e
    except yaml.YAMLError as e:
        raise RuntimeError(f"Failed to parse YAML spec from {url}: {e}") from e


def create_auth_header(username: str, password: str) -> str:
    """Create a basic authentication header."""
    auth_bytes = f"{username}:{password}".encode('utf-8')
    return base64.b64encode(auth_bytes).decode('utf-8')

import os
from typing import Dict, List, Optional
from argparse import ArgumentParser, Namespace


def load_config() -> Dict[str, str]:
    """Load Bandwidth configuration from environment variables."""
    config = {}
    required_vars = ["BW_USERNAME", "BW_PASSWORD"]
    optional_vars = [
        "BW_ACCOUNT_ID",
        "BW_NUMBER",
        "BW_MESSAGING_APPLICATION_ID",
        "BW_VOICE_APPLICATION_ID",
    ]

    # Add all variables that exist
    for var in required_vars + optional_vars:
        value = os.getenv(var)
        if value:
            config[var] = value

    # Required variables
    for var in required_vars:
        if var not in config.keys():
            raise ValueError(f"Missing required environment variable: {var}")
        
    return config


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


def get_enabled_tools() -> Optional[List[str]]:
    """Get the list of enabled tools from CLI args or environment variable."""
    args = _parse_cli_args()
    return _parse_flags(args.tools, "BW_MCP_TOOLS")


def get_excluded_tools() -> Optional[List[str]]:
    """Get the list of excluded tools from CLI args or environment variable."""
    args = _parse_cli_args()
    return _parse_flags(args.exclude_tools, "BW_MCP_EXCLUDE_TOOLS")

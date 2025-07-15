import os
import argparse
from dotenv import load_dotenv

load_dotenv()

bandwidth_account_id = os.environ["BW_ACCOUNT_ID"]
bandwidth_number = os.environ["BW_NUMBER"]
bandwidth_messaging_application_id = os.environ["BW_MESSAGING_APPLICATION_ID"]
username = os.environ["BW_USERNAME"]
password = os.environ["BW_PASSWORD"].replace("\\", "")



def get_config():
    """Get the Bandwidth configuration"""
    return {
        "bandwidth_account_id": bandwidth_account_id,
        "bandwidth_number": bandwidth_number,
        "bandwidth_messaging_application_id": bandwidth_messaging_application_id,
        "username": username,
        "password": password
    }


def clean_openapi_spec(spec: dict):
    """Recursively clean OpenAPI spec:
    - Remove all callbacks
    - Remove all 4xx/5xx responses
    - Remove any field starting with 'x-'
    - Remove all path resources that start with 'x-'
    """
    def _clean(obj):
        if isinstance(obj, dict):
            # Remove 'callbacks' and 'x-' fields
            keys_to_remove = [k for k in obj if k == "callbacks" or k.startswith("x-")]
            for k in keys_to_remove:
                del obj[k]
            # Remove 4xx/5xx responses
            if "responses" in obj:
                codes_to_remove = [code for code in obj["responses"] if code.startswith("4") or code.startswith("5")]
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

    return _clean(spec)


def parse_cli_args(args=None):
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Bandwidth MCP Server")

    # APIs
    parser.add_argument(
        "--apis",
        help="Comma-separated list of API names to enable. If not specified, all tools are enabled.",
        type=str,
    )
    parser.add_argument(
        "--exclude-apis",
        help="Comma-separated list of API names to disable.",
        type=str,
    )
    # parser.add_argument(
    #     "--list-tools",
    #     help="List all available tools and exit.",
    #     action="store_true",
    # )

    return parser.parse_known_args(args)[0]


def get_enabled_apis():
    """Get the list of enabled APIs from CLI args or environment variable."""
    try:
        args = parse_cli_args()

        if args.apis:
            return [api.strip() for api in args.apis.split(",")]
    except:
        pass

    # Check for environment variable
    env_apis = os.getenv("BW_MCP_APIS")
    if env_apis:
        return [api.strip() for api in env_apis.split(",")]

    return None


def get_excluded_apis():
    """Get the list of excluded APIs from CLI args or environment variable."""
    try:
        args = parse_cli_args()

        if args.exclude_apis:
            return [api.strip() for api in args.exclude_apis.split(",")]
    except:
        pass

    env_exclude_apis = os.getenv("BW_MCP_EXCLUDE_APIS")
    if env_exclude_apis:
        return [api.strip() for api in env_exclude_apis.split(",")]

    return []


def filter_apis(all_apis: list, enabled_apis: list | None, excluded_apis: list | None) -> list:
    """Return the list of APIs after applying enabled and excluded filters."""
    filtered = all_apis
    if enabled_apis:
        filtered = [api for api in all_apis if api in enabled_apis]
        if not filtered:
            raise ValueError("No valid APIs enabled. Please specify at least one valid API to enable.")
    if excluded_apis:
        filtered = [api for api in all_apis if api not in excluded_apis]
        if not filtered:
            raise ValueError("All valid APIs excluded. Please specify at least one valid API to include.")
    return filtered

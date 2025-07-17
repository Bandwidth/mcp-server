from typing import List
from utils import get_config
from fastmcp.resources import FunctionResource, HttpResource, Resource

config_resource = FunctionResource(
    name="Bandwidth API Configuration",
    description="Configuration Object for Bandwidth API",
    tags={"bandwidth", "config"},
    uri="data://config",
    mime_type="application/json",
    fn=get_config,
)

number_order_guide_resource = HttpResource(
    name="Bandwidth Number Order Guide",
    description="Bandwidth Number Order Guide",
    tags={"bandwidth", "number", "order", "guide"},
    uri="data://number_order_guide",
    mime_type="text/markdown",
    url="https://dev.bandwidth.com/docs/numbers/guides/searchingForNumbers.md",
)

def get_bandwidth_resources() -> List[Resource]:
    """Get all Bandwidth resources."""
    return [config_resource, number_order_guide_resource]

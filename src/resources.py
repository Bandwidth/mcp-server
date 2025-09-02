from typing import List
from fastmcp.resources import HttpResource, Resource


number_order_guide_resource = HttpResource(
    name="Bandwidth Number Order Guide",
    description="Bandwidth Number Order Guide",
    tags={"bandwidth", "number", "order", "guide"},
    uri="resource://number_order_guide",
    mime_type="text/markdown",
    url="https://dev.bandwidth.com/docs/numbers/guides/searchingForNumbers.md",
)


def get_bandwidth_resources() -> List[Resource]:
    """Get all Bandwidth resources."""
    return [number_order_guide_resource]

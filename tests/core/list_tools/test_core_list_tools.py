import pytest
from paylink_sdk import PayLinkClient

@pytest.mark.asyncio
async def test_list_tools_returns_tools():
    client = PayLinkClient("http://localhost:8050/mcp")
    tools = await client.list_tools()
    assert isinstance(tools, list)
    assert len(tools) > 0
    assert all(hasattr(tool, "name") for tool in tools)

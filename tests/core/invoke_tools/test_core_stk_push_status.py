import pytest
from paylink_sdk import PayLinkClient

@pytest.mark.asyncio
async def test_stk_push_status_successfully_checks():
    client = PayLinkClient("http://localhost:8050/mcp")

    # Replace this dynamically if you have a way to get the latest one
    tool_args = {
        "checkout_request_id": "ws_CO_12052025033128264797357665"
    }

    result = await client.call_tool("stk_push_status", tool_args)

    assert result is not None
    assert hasattr(result, "content")
    assert not result.isError

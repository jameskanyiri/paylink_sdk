from typing import Dict, List, Any

from paylink_sdk import PayLinkClient as BasePayLinkClient


class PayLinkClient:
    """Langchain-compatible client for PayLink tools."""

    def __init__(self, server_url: str = None):
        self.base_client = (
            BasePayLinkClient(server_url) if server_url else BasePayLinkClient()
        )
        self._tools_cache = None

    async def _load_tools(self):
        """Load available tools from the PayLink server."""
        if self._tools_cache is None:
            self._tools_cache = await self.base_client.list_tools()
        return self._tools_cache

    async def list_tools(self) -> List[Dict]:
        """Get all available tools as Langchain tools format."""
        server_tools = await self._load_tools()

        langchain_tools = []
        for tool in server_tools:
            # Convert tool definition to Langchain format
            tool_name = tool.name
            tool_description = tool.description

            properties = tool.inputSchema.get("properties", {})

            langchain_properties = {}
            required_fields = []

            for key, value in properties.items():
                field_type = value.get("type", "string")
                field_desc = value.get("description", value.get("title", ""))

                langchain_properties[key] = {
                    "type": field_type,
                    "description": field_desc,
                }

                required_fields.append(key)

            openai_tool = {
                "type": "function",
                "function": {
                    "name": tool_name,
                    "description": tool_description,
                    "parameters": {
                        "type": "object",
                        "properties": langchain_properties,
                        "required": required_fields,
                        "additionalProperties": False,
                    },
                },
            }

            langchain_tools.append(openai_tool)

        return langchain_tools

    async def call_tool(self, name: str, arguments: Dict) -> Any:
        """Execute a specific tool with given arguments."""
        return await self.base_client.call_tool(name, arguments)

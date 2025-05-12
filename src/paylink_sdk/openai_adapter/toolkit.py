from typing import Dict, List, Any

from paylink_sdk import PayLinkClient as BasePayLinkClient


class PayLinkClient:
    """OpenAI-compatible client for PayLink tools."""

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
        """Get all available tools as OpenAI tools format."""
        server_tools = await self._load_tools()

        openai_tools = []
        for tool in server_tools:
            # Convert tool definition to OpenAI format
            tool_name = tool.name
            tool_description = tool.description
            
            properties = tool.inputSchema.get("properties", {})
            
            open_ai_properties = {}
            required_fields = []
            
            for key, value in properties.items():
                field_type = value.get("type", "string")
                field_desc = value.get("description", value.get("title",""))
                
                open_ai_properties[key] = {
                    "type": field_type,
                    "description": field_desc
                }
                
                required_fields.append(key)
            
            
            openai_tool = {
                "type": "function",
                "name": tool_name,
                "description": tool_description,
                "parameters": {
                    "type": "object",
                    "properties": open_ai_properties,
                    "required": required_fields,
                    "additionalProperties": False
                }
            }
            
            openai_tools.append(openai_tool)

        return openai_tools


    async def call_tool(self, name: str, arguments: Dict) -> Any:
        """Execute a specific tool with given arguments."""
        return await self.base_client.call_tool(name, arguments)
from contextlib import asynccontextmanager
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client



class PayLinkClient:
    """
    Client for interacting with the PayLink MCP server over streamable HTTP.
    """

    def __init__(
        self, server_url: str = "http://0.0.0.0:8050/mcp"
    ):
        self.server_url = server_url

    @asynccontextmanager
    async def connect(self):
        """
        Async context manager to connect to the MCP server using streamable HTTP.
        """
        async with streamablehttp_client(self.server_url) as (read_stream, write_stream, _):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                yield session
                

    async def list_tools(self):
        """
        List all available tools from the server.
        Returns:
            list: A list of ToolDescription objects.
        """
        async with self.connect() as session:
            tools_result = await session.list_tools()
            return tools_result.tools
        

    async def call_tool(self, tool_name: str, tool_args: dict):
        """Call a tool by name with arguments and return the results

        Args:
            tool_name (str): Name of the tool to invoke
            tool_args (dict): Input arguments for the tool

        Returns:
            Dict: result from the tool execution
        """

        async with self.connect() as session:
            # Step 1: List available tools to confirm it exists
            tools_result = await session.list_tools()
            tool = next((t for t in tools_result.tools if t.name == tool_name), None)

            if not tool:
                raise ValueError(f"Tool '{tool_name}' not found in server's tool list.")

            result = await session.call_tool(tool_name, tool_args)

            return result

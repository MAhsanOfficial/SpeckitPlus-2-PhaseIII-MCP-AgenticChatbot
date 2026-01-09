"""
Property Test: Tool Availability

Feature: phase-iii-chatbot, Property 11: Tool Availability
Validates: Requirements 1.3

For any AI agent invocation, all registered MCP tools (habit_list, habit_create,
habit_log_completion, habit_streak, habit_summary) SHALL be available for the
agent to call.
"""
import os
import pytest
from hypothesis import given, settings, strategies as st
from unittest.mock import patch, MagicMock

# Set a dummy API key for testing
os.environ.setdefault("GEMINI_API_KEY", "test-api-key")


class TestToolAvailability:
    """Property tests for tool availability in the AI agent."""
    
    REQUIRED_TOOLS = [
        "habit_list",
        "habit_get", 
        "habit_create",
        "habit_log_completion",
        "habit_streak",
        "habit_summary"
    ]
    
    def test_all_required_tools_are_registered(self):
        """
        Property: All required MCP tools are available in the agent.
        
        For any agent instance, all required tools must be present.
        """
        from src.mcp.tools.habits import get_habit_tools
        
        tools = get_habit_tools()
        tool_names = [tool.name for tool in tools]
        
        for required_tool in self.REQUIRED_TOOLS:
            assert required_tool in tool_names, f"Required tool '{required_tool}' not found"
    
    def test_tools_have_valid_schemas(self):
        """
        Property: All tools have valid input schemas.
        
        For any tool, the input_schema must be a valid JSON schema object.
        """
        from src.mcp.tools.habits import get_habit_tools
        
        tools = get_habit_tools()
        
        for tool in tools:
            schema = tool.input_schema
            assert isinstance(schema, dict), f"Tool {tool.name} schema is not a dict"
            assert "type" in schema, f"Tool {tool.name} schema missing 'type'"
            assert schema["type"] == "object", f"Tool {tool.name} schema type is not 'object'"
            assert "properties" in schema, f"Tool {tool.name} schema missing 'properties'"
    
    def test_tools_have_descriptions(self):
        """
        Property: All tools have non-empty descriptions.
        
        For any tool, the description must be a non-empty string.
        """
        from src.mcp.tools.habits import get_habit_tools
        
        tools = get_habit_tools()
        
        for tool in tools:
            assert tool.description, f"Tool {tool.name} has empty description"
            assert len(tool.description) > 10, f"Tool {tool.name} description too short"
    
    def test_tools_are_async_executable(self):
        """
        Property: All tools have async execute methods.
        
        For any tool, the execute method must be a coroutine function.
        """
        import asyncio
        from src.mcp.tools.habits import get_habit_tools
        
        tools = get_habit_tools()
        
        for tool in tools:
            assert asyncio.iscoroutinefunction(tool.execute), \
                f"Tool {tool.name} execute is not async"
    
    @given(st.sampled_from(REQUIRED_TOOLS))
    @settings(max_examples=len(REQUIRED_TOOLS))
    def test_each_required_tool_exists(self, tool_name: str):
        """
        Property: Each required tool exists in the registry.
        
        For any required tool name, it must exist in the tool registry.
        """
        from src.mcp.tools.habits import get_habit_tools
        
        tools = get_habit_tools()
        tool_names = [tool.name for tool in tools]
        
        assert tool_name in tool_names, f"Tool '{tool_name}' not found in registry"
    
    def test_tools_can_be_converted_to_mcp_format(self):
        """
        Property: All tools can be converted to MCP tool format.
        
        For any tool, to_mcp_tool() must return a valid MCP tool spec.
        """
        from src.mcp.tools.habits import get_habit_tools
        
        tools = get_habit_tools()
        
        for tool in tools:
            mcp_spec = tool.to_mcp_tool()
            assert "name" in mcp_spec, f"Tool {tool.name} MCP spec missing 'name'"
            assert "description" in mcp_spec, f"Tool {tool.name} MCP spec missing 'description'"
            assert "inputSchema" in mcp_spec, f"Tool {tool.name} MCP spec missing 'inputSchema'"
            assert mcp_spec["name"] == tool.name


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

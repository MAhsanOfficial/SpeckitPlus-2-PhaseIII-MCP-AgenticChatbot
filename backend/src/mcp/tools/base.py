"""
Base MCP tool class for Phase III chatbot.

All MCP tools must inherit from this base class to ensure
stateless and deterministic behavior as required by the constitution.
"""
from typing import Any, Dict, Optional
from abc import ABC, abstractmethod


class BaseMCPTool(ABC):
    """
    Base class for all MCP tools.

    Principles enforced:
    - Stateless: No instance-level state between calls
    - Deterministic: Same input always produces same output
    - Phase II delegation: All tools delegate to existing APIs
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique name for the tool."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Description of what the tool does."""
        pass

    @property
    @abstractmethod
    def input_schema(self) -> Dict[str, Any]:
        """JSON Schema for tool input."""
        pass

    @abstractmethod
    async def execute(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Execute the tool with given parameters.

        All tools must:
        - Be async for consistency
        - Accept parameters matching input_schema
        - Return JSON-serializable dict
        - Never modify global state
        - Delegate to Phase II APIs via HTTP client
        """
        pass

    def to_mcp_tool(self) -> Dict[str, Any]:
        """Convert to MCP tool specification format."""
        return {
            "name": self.name,
            "description": self.description,
            "inputSchema": self.input_schema
        }

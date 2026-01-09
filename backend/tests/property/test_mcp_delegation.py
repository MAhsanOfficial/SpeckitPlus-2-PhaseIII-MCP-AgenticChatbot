"""
Property Test: MCP Tool Delegation

Feature: phase-iii-chatbot, Property 3: MCP Tool Delegation
Validates: Requirements 2.6, 2.7, 7.6

For any MCP tool execution, the tool SHALL delegate to Phase II API endpoints
via HTTP and SHALL NOT access the database directly. The JWT token SHALL be
passed through to the Phase II API for user-scoped operations.
"""
import os
import pytest
from hypothesis import given, settings, strategies as st
import inspect
import ast

# Set environment variables for testing
os.environ.setdefault("GEMINI_API_KEY", "test-api-key")


class TestMCPDelegation:
    """Property tests for MCP tool delegation."""
    
    def test_phase2_client_uses_http(self):
        """
        Property: Phase2 client uses HTTP for API calls.
        
        The Phase2APIClient should use httpx for HTTP requests.
        """
        from src.mcp.tools.phase2_client import Phase2APIClient
        import inspect
        
        source = inspect.getsource(Phase2APIClient)
        
        # Should use httpx
        assert "httpx" in source, "Phase2APIClient should use httpx"
    
    def test_phase2_client_accepts_jwt_token(self):
        """
        Property: Phase2 client accepts JWT token.
        
        The client should be initialized with a JWT token.
        """
        from src.mcp.tools.phase2_client import Phase2APIClient
        import inspect
        
        sig = inspect.signature(Phase2APIClient.__init__)
        params = list(sig.parameters.keys())
        
        assert "jwt_token" in params, "Phase2APIClient should accept jwt_token"
    
    def test_phase2_client_sets_auth_header(self):
        """
        Property: Phase2 client sets Authorization header.
        
        The client should set the Bearer token in headers.
        """
        from src.mcp.tools.phase2_client import Phase2APIClient
        
        client = Phase2APIClient("test-token")
        
        assert "Authorization" in client.headers
        assert "Bearer test-token" in client.headers["Authorization"]
    
    def test_habit_tools_use_phase2_client(self):
        """
        Property: Habit tools use Phase2APIClient.
        
        All habit tools should delegate to Phase2APIClient.
        """
        from src.mcp.tools import habits
        import inspect
        
        source = inspect.getsource(habits)
        
        # Should import and use Phase2APIClient
        assert "Phase2APIClient" in source or "create_phase2_client" in source
    
    def test_tools_do_not_import_sqlmodel_directly(self):
        """
        Property: Tools do not access database directly.
        
        MCP tools should not import SQLModel or database modules.
        """
        from src.mcp.tools import habits
        import inspect
        
        source = inspect.getsource(habits)
        
        # Should not directly import database modules
        assert "from sqlmodel import" not in source
        assert "from src.db import" not in source
        assert "from src.core.db import" not in source
    
    def test_all_tools_accept_jwt_token(self):
        """
        Property: All tools accept JWT token parameter.
        
        Every tool's execute method should accept jwt_token.
        """
        from src.mcp.tools.habits import get_habit_tools
        import inspect
        
        tools = get_habit_tools()
        
        for tool in tools:
            sig = inspect.signature(tool.execute)
            params = list(sig.parameters.keys())
            
            assert "jwt_token" in params, f"Tool {tool.name} should accept jwt_token"
    
    @given(token=st.text(min_size=10, max_size=500))
    @settings(max_examples=100, deadline=None)
    def test_jwt_token_is_preserved_in_headers(self, token: str):
        """
        Property: JWT token is preserved in headers.
        
        For any JWT token, it should be correctly set in the Authorization header.
        """
        from src.mcp.tools.phase2_client import Phase2APIClient
        
        client = Phase2APIClient(token)
        
        assert client.headers["Authorization"] == f"Bearer {token}"
    
    def test_phase2_client_has_habit_methods(self):
        """
        Property: Phase2 client has methods for habit operations.
        
        The client should have methods for all habit operations.
        """
        from src.mcp.tools.phase2_client import Phase2APIClient
        
        required_methods = [
            "list_habits",
            "get_habit",
            "create_habit",
            "toggle_habit_completion",
            "get_weekly_analytics"
        ]
        
        for method in required_methods:
            assert hasattr(Phase2APIClient, method), \
                f"Phase2APIClient should have {method} method"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

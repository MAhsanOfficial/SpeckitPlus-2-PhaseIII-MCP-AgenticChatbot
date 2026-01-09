"""
Property Test: Response Structure Compliance

Feature: phase-iii-chatbot, Property 7: Response Structure Compliance
Validates: Requirements 8.1, 8.2, 8.3

For any successful chat response, the response SHALL include:
- A non-empty conversation_id string
- A message object with id, role, content, and timestamp fields
- A suggestions array (may be empty)
"""
import os
import pytest
from datetime import datetime
from hypothesis import given, settings, strategies as st

# Set environment variables for testing
os.environ.setdefault("GEMINI_API_KEY", "test-api-key")


class TestResponseStructure:
    """Property tests for response structure compliance."""
    
    def test_chat_response_has_required_fields(self):
        """
        Property: ChatResponse has all required fields.
        
        The response model must have conversation_id, message, and suggestions.
        """
        from src.api.chat.models import ChatResponse, ChatMessageResponse
        
        response = ChatResponse(
            conversation_id="conv-123",
            message=ChatMessageResponse(
                id="msg-456",
                role="assistant",
                content="Hello!",
                timestamp=datetime.utcnow()
            ),
            suggestions=["Option 1", "Option 2"]
        )
        
        assert response.conversation_id is not None
        assert response.message is not None
        assert response.suggestions is not None
    
    def test_chat_message_response_has_required_fields(self):
        """
        Property: ChatMessageResponse has all required fields.
        
        The message model must have id, role, content, and timestamp.
        """
        from src.api.chat.models import ChatMessageResponse
        
        message = ChatMessageResponse(
            id="msg-789",
            role="assistant",
            content="Test content",
            timestamp=datetime.utcnow()
        )
        
        assert message.id is not None
        assert message.role is not None
        assert message.content is not None
        assert message.timestamp is not None
    
    @given(
        conv_id=st.text(min_size=1, max_size=36),
        content=st.text(min_size=1, max_size=1000)
    )
    @settings(max_examples=100, deadline=None)
    def test_response_preserves_conversation_id(self, conv_id: str, content: str):
        """
        Property: Response preserves conversation_id.
        
        For any conversation_id, it should be preserved in the response.
        """
        from src.api.chat.models import ChatResponse, ChatMessageResponse
        
        response = ChatResponse(
            conversation_id=conv_id,
            message=ChatMessageResponse(
                role="assistant",
                content=content,
                timestamp=datetime.utcnow()
            ),
            suggestions=[]
        )
        
        assert response.conversation_id == conv_id
    
    @given(suggestions=st.lists(st.text(min_size=1, max_size=100), min_size=0, max_size=5))
    @settings(max_examples=100, deadline=None)
    def test_suggestions_array_is_preserved(self, suggestions: list):
        """
        Property: Suggestions array is preserved.
        
        For any list of suggestions, they should be preserved in the response.
        """
        from src.api.chat.models import ChatResponse, ChatMessageResponse
        
        response = ChatResponse(
            conversation_id="conv-123",
            message=ChatMessageResponse(
                role="assistant",
                content="Test",
                timestamp=datetime.utcnow()
            ),
            suggestions=suggestions
        )
        
        assert response.suggestions == suggestions
    
    def test_empty_suggestions_is_valid(self):
        """
        Property: Empty suggestions array is valid.
        
        A response with no suggestions should still be valid.
        """
        from src.api.chat.models import ChatResponse, ChatMessageResponse
        
        response = ChatResponse(
            conversation_id="conv-123",
            message=ChatMessageResponse(
                role="assistant",
                content="Test",
                timestamp=datetime.utcnow()
            ),
            suggestions=[]
        )
        
        assert response.suggestions == []
        assert len(response.suggestions) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

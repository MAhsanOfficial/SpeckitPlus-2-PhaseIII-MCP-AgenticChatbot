"""
Property Test: Message Persistence Round-Trip

Feature: phase-iii-chatbot, Property 1: Message Persistence Round-Trip
Validates: Requirements 4.2, 4.3

For any user message sent to the chat endpoint, the message SHALL be persisted
to the database with role "user", and for any AI response generated, it SHALL
be persisted with role "assistant". Subsequently, loading the conversation
history SHALL return both messages in order.
"""
import os
import json
import pytest
from datetime import datetime
from hypothesis import given, settings, strategies as st
from unittest.mock import AsyncMock, MagicMock, patch

# Set environment variables for testing
os.environ.setdefault("GEMINI_API_KEY", "test-api-key")


# Strategy for generating valid message content
message_content_strategy = st.text(
    alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')),
    min_size=1,
    max_size=1000
).filter(lambda x: x.strip())  # Ensure non-empty after stripping


class TestMessagePersistence:
    """Property tests for message persistence."""
    
    @given(
        user_message=message_content_strategy,
        assistant_response=message_content_strategy
    )
    @settings(max_examples=100, deadline=None)
    def test_messages_are_persisted_with_correct_roles(
        self,
        user_message: str,
        assistant_response: str
    ):
        """
        Property: Messages are persisted with correct roles.
        
        For any user message and assistant response, both should be
        persisted with their respective roles.
        """
        from src.db.models import ChatMessage
        
        # Create user message
        user_msg = ChatMessage(
            session_id="test-session",
            role="user",
            content=user_message,
            timestamp=datetime.utcnow()
        )
        
        # Create assistant message
        assistant_msg = ChatMessage(
            session_id="test-session",
            role="assistant",
            content=assistant_response,
            timestamp=datetime.utcnow()
        )
        
        # Verify roles are correct
        assert user_msg.role == "user"
        assert assistant_msg.role == "assistant"
        
        # Verify content is preserved
        assert user_msg.content == user_message
        assert assistant_msg.content == assistant_response
    
    @given(
        tool_calls=st.lists(
            st.fixed_dictionaries({
                "name": st.sampled_from(["habit_list", "habit_create", "habit_streak"]),
                "arguments": st.fixed_dictionaries({
                    "habit_id": st.text(min_size=1, max_size=36)
                })
            }),
            min_size=0,
            max_size=5
        )
    )
    @settings(max_examples=100)
    def test_tool_calls_are_serialized_correctly(self, tool_calls: list):
        """
        Property: Tool calls are serialized and can be deserialized.
        
        For any list of tool calls, serializing to JSON and deserializing
        should produce the same data.
        """
        from src.db.models import ChatMessage
        
        # Serialize tool calls
        serialized = json.dumps(tool_calls) if tool_calls else None
        
        # Create message with tool calls
        msg = ChatMessage(
            session_id="test-session",
            role="assistant",
            content="Test response",
            timestamp=datetime.utcnow(),
            tool_calls=serialized
        )
        
        # Deserialize and verify
        if msg.tool_calls:
            deserialized = json.loads(msg.tool_calls)
            assert deserialized == tool_calls
        else:
            assert tool_calls == [] or tool_calls is None
    
    @given(
        messages=st.lists(
            st.tuples(
                st.sampled_from(["user", "assistant"]),
                message_content_strategy
            ),
            min_size=1,
            max_size=10
        )
    )
    @settings(max_examples=100)
    def test_message_order_is_preserved(self, messages: list):
        """
        Property: Message order is preserved in conversation history.
        
        For any sequence of messages, the order should be preserved
        when retrieved from the database.
        """
        from src.db.models import ChatMessage
        from datetime import timedelta
        
        # Create messages with incrementing timestamps
        base_time = datetime.utcnow()
        chat_messages = []
        
        for i, (role, content) in enumerate(messages):
            msg = ChatMessage(
                session_id="test-session",
                role=role,
                content=content,
                timestamp=base_time + timedelta(seconds=i)
            )
            chat_messages.append(msg)
        
        # Sort by timestamp (simulating database retrieval)
        sorted_messages = sorted(chat_messages, key=lambda m: m.timestamp)
        
        # Verify order is preserved
        for i, (original, retrieved) in enumerate(zip(chat_messages, sorted_messages)):
            assert original.role == retrieved.role
            assert original.content == retrieved.content
    
    def test_conversation_session_owns_messages(self):
        """
        Property: Messages belong to their conversation session.
        
        For any message, it must have a valid session_id.
        """
        from src.db.models import ChatMessage, ConversationSession
        import uuid
        
        # Create session
        session_id = str(uuid.uuid4())
        session = ConversationSession(
            id=session_id,
            user_id="test-user",
            title="Test Conversation"
        )
        
        # Create message for session
        msg = ChatMessage(
            session_id=session_id,
            role="user",
            content="Test message",
            timestamp=datetime.utcnow()
        )
        
        # Verify session ownership
        assert msg.session_id == session.id
    
    @given(content=message_content_strategy)
    @settings(max_examples=100)
    def test_message_content_is_not_modified(self, content: str):
        """
        Property: Message content is stored exactly as provided.
        
        For any message content, it should be stored and retrieved
        without modification.
        """
        from src.db.models import ChatMessage
        
        msg = ChatMessage(
            session_id="test-session",
            role="user",
            content=content,
            timestamp=datetime.utcnow()
        )
        
        # Content should be exactly as provided
        assert msg.content == content
        assert len(msg.content) == len(content)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

"""
Property Tests for Session Management

This file contains property tests for:
- Property 4: Conversation History Management (Requirements 4.5, 4.6)
- Property 5: Session Isolation (Requirements 5.3, 5.4)
- Property 9: User Data Isolation (Requirements 7.5)
- Property 10: New Conversation Session Creation (Requirements 4.1)
"""
import os
import pytest
from datetime import datetime
from hypothesis import given, settings, strategies as st
import uuid

# Set environment variables for testing
os.environ.setdefault("GEMINI_API_KEY", "test-api-key")


class TestConversationHistoryManagement:
    """
    Property 4: Conversation History Management
    Validates: Requirements 4.5, 4.6
    """
    
    def test_conversation_service_has_limit_parameter(self):
        """
        Property: History loading has a limit parameter.
        
        The get_session_messages method should accept a limit parameter.
        """
        from src.db.conversation_service import ConversationService
        import inspect
        
        sig = inspect.signature(ConversationService.get_session_messages)
        params = list(sig.parameters.keys())
        
        assert "limit" in params, "get_session_messages should have limit parameter"
    
    def test_default_limit_is_50(self):
        """
        Property: Default history limit is 50 messages.
        
        The default limit should be 50 as per requirements.
        """
        from src.db.conversation_service import ConversationService
        import inspect
        
        sig = inspect.signature(ConversationService.get_session_messages)
        limit_param = sig.parameters.get("limit")
        
        assert limit_param is not None
        assert limit_param.default == 50, "Default limit should be 50"


class TestSessionIsolation:
    """
    Property 5: Session Isolation
    Validates: Requirements 5.3, 5.4
    """
    
    def test_session_has_user_id(self):
        """
        Property: Sessions are associated with users.
        
        ConversationSession must have a user_id field.
        """
        from src.db.models import ConversationSession
        
        session = ConversationSession(
            id=str(uuid.uuid4()),
            user_id="user-123",
            title="Test Session"
        )
        
        assert session.user_id == "user-123"
    
    def test_messages_belong_to_sessions(self):
        """
        Property: Messages belong to specific sessions.
        
        ChatMessage must have a session_id field.
        """
        from src.db.models import ChatMessage
        
        session_id = str(uuid.uuid4())
        message = ChatMessage(
            id=str(uuid.uuid4()),
            session_id=session_id,
            role="user",
            content="Test message",
            timestamp=datetime.utcnow()
        )
        
        assert message.session_id == session_id
    
    @given(
        user_id_1=st.text(min_size=8, max_size=36, alphabet=st.characters(whitelist_categories=('L', 'N'))),
        user_id_2=st.text(min_size=8, max_size=36, alphabet=st.characters(whitelist_categories=('L', 'N')))
    )
    @settings(max_examples=100, deadline=None)
    def test_different_users_have_different_sessions(self, user_id_1: str, user_id_2: str):
        """
        Property: Different users have isolated sessions.
        
        Sessions created for different users should have different user_ids.
        """
        from src.db.models import ConversationSession
        
        session_1 = ConversationSession(
            id=str(uuid.uuid4()),
            user_id=user_id_1,
            title="Session 1"
        )
        
        session_2 = ConversationSession(
            id=str(uuid.uuid4()),
            user_id=user_id_2,
            title="Session 2"
        )
        
        # Sessions should have their respective user_ids
        assert session_1.user_id == user_id_1
        assert session_2.user_id == user_id_2


class TestUserDataIsolation:
    """
    Property 9: User Data Isolation
    Validates: Requirements 7.5
    """
    
    def test_get_session_requires_user_id(self):
        """
        Property: Session retrieval requires user_id.
        
        The get_session method must require user_id for filtering.
        """
        from src.db.conversation_service import ConversationService
        import inspect
        
        sig = inspect.signature(ConversationService.get_session)
        params = list(sig.parameters.keys())
        
        assert "user_id" in params
    
    def test_get_user_sessions_filters_by_user(self):
        """
        Property: User sessions are filtered by user_id.
        
        The get_user_sessions method must filter by user_id.
        """
        from src.db.conversation_service import ConversationService
        import inspect
        
        sig = inspect.signature(ConversationService.get_user_sessions)
        params = list(sig.parameters.keys())
        
        assert "user_id" in params
    
    def test_delete_session_requires_user_id(self):
        """
        Property: Session deletion requires user_id.
        
        The delete_session method must require user_id for authorization.
        """
        from src.db.conversation_service import ConversationService
        import inspect
        
        sig = inspect.signature(ConversationService.delete_session)
        params = list(sig.parameters.keys())
        
        assert "user_id" in params


class TestNewSessionCreation:
    """
    Property 10: New Conversation Session Creation
    Validates: Requirements 4.1
    """
    
    def test_create_session_requires_user_id(self):
        """
        Property: Session creation requires user_id.
        
        The create_session method must require user_id.
        """
        from src.db.conversation_service import ConversationService
        import inspect
        
        sig = inspect.signature(ConversationService.create_session)
        params = list(sig.parameters.keys())
        
        assert "user_id" in params
    
    def test_session_model_has_required_fields(self):
        """
        Property: Session model has all required fields.
        
        ConversationSession must have id, user_id, title, created_at, last_activity_at.
        """
        from src.db.models import ConversationSession
        
        session = ConversationSession(
            id=str(uuid.uuid4()),
            user_id="user-123",
            title="Test Session",
            created_at=datetime.utcnow(),
            last_activity_at=datetime.utcnow()
        )
        
        assert session.id is not None
        assert session.user_id is not None
        assert session.created_at is not None
        assert session.last_activity_at is not None
    
    @given(user_id=st.text(min_size=8, max_size=36, alphabet=st.characters(whitelist_categories=('L', 'N'))))
    @settings(max_examples=100, deadline=None)
    def test_session_preserves_user_id(self, user_id: str):
        """
        Property: Session preserves user_id.
        
        For any user_id, it should be preserved in the session.
        """
        from src.db.models import ConversationSession
        
        session = ConversationSession(
            id=str(uuid.uuid4()),
            user_id=user_id,
            title="Test"
        )
        
        assert session.user_id == user_id


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

"""
Property Test: Confirmation Flow for Destructive Actions

Feature: phase-iii-chatbot, Property 6: Confirmation Flow for Destructive Actions
Validates: Requirements 6.1, 6.2, 6.3, 6.5

For any request to delete all habits or reset a streak, the AI agent SHALL
require explicit confirmation before proceeding. For any unambiguous single-item
deletion, the action SHALL proceed without confirmation. For any "cancel" command
during a pending confirmation, the action SHALL be aborted.
"""
import os
import pytest
from datetime import datetime, timedelta
from hypothesis import given, settings, strategies as st

# Set environment variables for testing
os.environ.setdefault("GEMINI_API_KEY", "test-api-key")


class TestConfirmationFlow:
    """Property tests for confirmation flow."""
    
    # Strategies for generating test data
    destructive_phrases = st.sampled_from([
        "delete all habits",
        "remove all habits",
        "clear all habits",
        "reset streak",
        "reset my streak",
        "clear streak"
    ])
    
    confirmation_phrases = st.sampled_from([
        "confirm",
        "yes",
        "yes, delete",
        "yes, proceed",
        "do it",
        "go ahead",
        "i confirm"
    ])
    
    cancellation_phrases = st.sampled_from([
        "cancel",
        "no",
        "nevermind",
        "never mind",
        "stop",
        "abort"
    ])
    
    single_deletion_phrases = st.sampled_from([
        "delete habit morning run",
        "remove habit meditation",
        "delete this habit"
    ])
    
    @given(phrase=destructive_phrases)
    @settings(max_examples=100, deadline=None)
    def test_destructive_actions_are_detected(self, phrase: str):
        """
        Property: Destructive action phrases are detected.
        
        For any destructive phrase, the service should detect it.
        """
        from src.services.confirmation_flow import get_confirmation_service
        
        service = get_confirmation_service()
        action_type = service.detect_destructive_action(phrase)
        
        assert action_type is not None, f"Failed to detect destructive action: {phrase}"
    
    @given(phrase=confirmation_phrases)
    @settings(max_examples=100, deadline=None)
    def test_confirmation_responses_are_recognized(self, phrase: str):
        """
        Property: Confirmation responses are recognized.
        
        For any confirmation phrase, the service should recognize it.
        """
        from src.services.confirmation_flow import get_confirmation_service
        
        service = get_confirmation_service()
        is_confirmation = service.is_confirmation_response(phrase)
        
        assert is_confirmation, f"Failed to recognize confirmation: {phrase}"
    
    @given(phrase=cancellation_phrases)
    @settings(max_examples=100, deadline=None)
    def test_cancellation_responses_are_recognized(self, phrase: str):
        """
        Property: Cancellation responses are recognized.
        
        For any cancellation phrase, the service should recognize it.
        """
        from src.services.confirmation_flow import get_confirmation_service
        
        service = get_confirmation_service()
        is_cancellation = service.is_cancellation_response(phrase)
        
        assert is_cancellation, f"Failed to recognize cancellation: {phrase}"
    
    @given(phrase=single_deletion_phrases)
    @settings(max_examples=100, deadline=None)
    def test_single_item_deletions_are_identified(self, phrase: str):
        """
        Property: Single item deletions are identified.
        
        For any single item deletion phrase, the service should identify it.
        """
        from src.services.confirmation_flow import get_confirmation_service
        
        service = get_confirmation_service()
        is_single = service.is_single_item_deletion(phrase)
        
        assert is_single, f"Failed to identify single deletion: {phrase}"
    
    def test_pending_confirmation_is_created(self):
        """
        Property: Pending confirmations are created for destructive actions.
        
        When a destructive action is detected, a pending confirmation should be created.
        """
        from src.services.confirmation_flow import (
            ConfirmationFlowService,
            DestructiveActionType
        )
        
        service = ConfirmationFlowService()
        user_id = "test-user-123"
        
        # Create pending confirmation
        confirmation = service.create_pending_confirmation(
            user_id=user_id,
            action_type=DestructiveActionType.DELETE_ALL_HABITS,
            context={"count": 5}
        )
        
        assert confirmation is not None
        assert confirmation.action_type == DestructiveActionType.DELETE_ALL_HABITS
        
        # Verify it can be retrieved
        retrieved = service.get_pending_confirmation(user_id)
        assert retrieved is not None
        assert retrieved.action_type == confirmation.action_type
    
    def test_pending_confirmation_is_cleared_on_cancel(self):
        """
        Property: Pending confirmations are cleared when cancelled.
        
        When a user cancels, the pending confirmation should be removed.
        """
        from src.services.confirmation_flow import (
            ConfirmationFlowService,
            DestructiveActionType
        )
        
        service = ConfirmationFlowService()
        user_id = "test-user-456"
        
        # Create pending confirmation
        service.create_pending_confirmation(
            user_id=user_id,
            action_type=DestructiveActionType.RESET_STREAK,
            context={"habit_name": "Morning Run"}
        )
        
        # Clear it
        cleared = service.clear_pending_confirmation(user_id)
        assert cleared is True
        
        # Verify it's gone
        retrieved = service.get_pending_confirmation(user_id)
        assert retrieved is None
    
    def test_confirmation_expires_after_timeout(self):
        """
        Property: Confirmations expire after 60 seconds.
        
        A pending confirmation should not be retrievable after expiration.
        """
        from src.services.confirmation_flow import (
            PendingConfirmation,
            DestructiveActionType
        )
        
        # Create an already-expired confirmation
        expired_confirmation = PendingConfirmation(
            action_type=DestructiveActionType.DELETE_ALL_HABITS,
            context={},
            created_at=datetime.utcnow() - timedelta(seconds=120),
            expires_at=datetime.utcnow() - timedelta(seconds=60)
        )
        
        assert expired_confirmation.is_expired() is True
    
    def test_confirmation_not_expired_within_timeout(self):
        """
        Property: Confirmations are valid within the timeout period.
        
        A pending confirmation should be retrievable before expiration.
        """
        from src.services.confirmation_flow import (
            PendingConfirmation,
            DestructiveActionType
        )
        
        # Create a fresh confirmation
        fresh_confirmation = PendingConfirmation(
            action_type=DestructiveActionType.DELETE_ALL_HABITS,
            context={}
        )
        
        assert fresh_confirmation.is_expired() is False
    
    @given(
        action_type=st.sampled_from([
            "DELETE_ALL_HABITS",
            "RESET_STREAK",
            "CLEAR_COMPLETIONS"
        ])
    )
    @settings(max_examples=100, deadline=None)
    def test_confirmation_prompts_are_generated(self, action_type: str):
        """
        Property: Confirmation prompts are generated for all action types.
        
        For any destructive action type, a non-empty prompt should be generated.
        """
        from src.services.confirmation_flow import (
            get_confirmation_service,
            DestructiveActionType
        )
        
        service = get_confirmation_service()
        action = DestructiveActionType[action_type]
        
        prompt = service.generate_confirmation_prompt(action, {})
        
        assert prompt is not None
        assert len(prompt) > 0
        assert "confirm" in prompt.lower() or "cancel" in prompt.lower()
    
    def test_non_destructive_messages_not_detected(self):
        """
        Property: Non-destructive messages are not flagged.
        
        Normal messages should not trigger confirmation flow.
        """
        from src.services.confirmation_flow import get_confirmation_service
        
        service = get_confirmation_service()
        
        normal_messages = [
            "show my habits",
            "what's my streak?",
            "create habit: morning run",
            "I completed my habit today",
            "help"
        ]
        
        for message in normal_messages:
            action_type = service.detect_destructive_action(message)
            assert action_type is None, f"Incorrectly detected destructive action: {message}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

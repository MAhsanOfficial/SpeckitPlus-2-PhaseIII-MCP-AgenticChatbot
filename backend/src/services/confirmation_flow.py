"""
Confirmation Flow Service for Destructive Actions.

This service manages confirmation state for destructive actions like:
- Delete all habits
- Reset streak
- Bulk deletions

Following the constitution principle of requiring explicit confirmation
for destructive actions to prevent accidental data loss.
"""
import json
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)


class DestructiveActionType(str, Enum):
    """Types of destructive actions requiring confirmation."""
    DELETE_ALL_HABITS = "delete_all_habits"
    DELETE_HABIT = "delete_habit"
    RESET_STREAK = "reset_streak"
    CLEAR_COMPLETIONS = "clear_completions"


@dataclass
class PendingConfirmation:
    """Represents a pending confirmation for a destructive action."""
    action_type: DestructiveActionType
    context: Dict[str, Any]
    created_at: datetime = field(default_factory=datetime.utcnow)
    expires_at: datetime = field(default_factory=lambda: datetime.utcnow() + timedelta(seconds=60))
    
    def is_expired(self) -> bool:
        """Check if this confirmation has expired."""
        return datetime.utcnow() > self.expires_at
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "action_type": self.action_type.value,
            "context": self.context,
            "created_at": self.created_at.isoformat(),
            "expires_at": self.expires_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PendingConfirmation":
        """Create from dictionary."""
        return cls(
            action_type=DestructiveActionType(data["action_type"]),
            context=data["context"],
            created_at=datetime.fromisoformat(data["created_at"]),
            expires_at=datetime.fromisoformat(data["expires_at"])
        )


# Patterns that indicate destructive actions
DESTRUCTIVE_PATTERNS = {
    DestructiveActionType.DELETE_ALL_HABITS: [
        "delete all habits",
        "remove all habits",
        "clear all habits",
        "delete everything",
        "remove everything"
    ],
    DestructiveActionType.RESET_STREAK: [
        "reset streak",
        "reset my streak",
        "clear streak",
        "start over"
    ],
    DestructiveActionType.CLEAR_COMPLETIONS: [
        "clear completions",
        "delete completions",
        "remove all completions"
    ]
}


class ConfirmationFlowService:
    """
    Service for managing confirmation flows for destructive actions.
    
    This service:
    - Detects destructive action requests
    - Creates pending confirmations with 60-second expiration
    - Validates confirmation responses
    - Handles cancellation
    """
    
    def __init__(self):
        # In-memory store for pending confirmations (keyed by user_id)
        # In production, this should be stored in Redis or database
        self._pending: Dict[str, PendingConfirmation] = {}
    
    def detect_destructive_action(self, message: str) -> Optional[DestructiveActionType]:
        """
        Detect if a message requests a destructive action.
        
        Args:
            message: The user's message
            
        Returns:
            The type of destructive action, or None if not destructive
        """
        message_lower = message.lower().strip()
        
        for action_type, patterns in DESTRUCTIVE_PATTERNS.items():
            for pattern in patterns:
                if pattern in message_lower:
                    return action_type
        
        return None
    
    def is_single_item_deletion(self, message: str) -> bool:
        """
        Check if the message is requesting deletion of a single item.
        
        Single item deletions don't require confirmation per the spec.
        """
        message_lower = message.lower()
        
        # Patterns for single item deletion
        single_patterns = [
            "delete habit",
            "remove habit",
            "delete this habit",
            "remove this habit"
        ]
        
        # Check if it's a single item deletion (not "all")
        for pattern in single_patterns:
            if pattern in message_lower and "all" not in message_lower:
                return True
        
        return False
    
    def create_pending_confirmation(
        self,
        user_id: str,
        action_type: DestructiveActionType,
        context: Dict[str, Any]
    ) -> PendingConfirmation:
        """
        Create a pending confirmation for a destructive action.
        
        Args:
            user_id: The user requesting the action
            action_type: Type of destructive action
            context: Additional context (e.g., habit IDs, counts)
            
        Returns:
            The created PendingConfirmation
        """
        confirmation = PendingConfirmation(
            action_type=action_type,
            context=context
        )
        self._pending[user_id] = confirmation
        logger.info(f"Created pending confirmation for user {user_id}: {action_type.value}")
        return confirmation
    
    def get_pending_confirmation(self, user_id: str) -> Optional[PendingConfirmation]:
        """
        Get the pending confirmation for a user.
        
        Returns None if no pending confirmation or if it has expired.
        """
        confirmation = self._pending.get(user_id)
        
        if confirmation is None:
            return None
        
        if confirmation.is_expired():
            self.clear_pending_confirmation(user_id)
            return None
        
        return confirmation
    
    def clear_pending_confirmation(self, user_id: str) -> bool:
        """
        Clear the pending confirmation for a user.
        
        Returns True if a confirmation was cleared, False otherwise.
        """
        if user_id in self._pending:
            del self._pending[user_id]
            logger.info(f"Cleared pending confirmation for user {user_id}")
            return True
        return False
    
    def is_confirmation_response(self, message: str) -> bool:
        """Check if the message is a confirmation response."""
        message_lower = message.lower().strip()
        confirmation_phrases = [
            "confirm",
            "yes",
            "yes, delete",
            "yes, proceed",
            "do it",
            "go ahead",
            "i confirm"
        ]
        return any(phrase in message_lower for phrase in confirmation_phrases)
    
    def is_cancellation_response(self, message: str) -> bool:
        """Check if the message is a cancellation response."""
        message_lower = message.lower().strip()
        cancellation_phrases = [
            "cancel",
            "no",
            "nevermind",
            "never mind",
            "stop",
            "abort",
            "don't",
            "do not"
        ]
        return any(phrase in message_lower for phrase in cancellation_phrases)
    
    def generate_confirmation_prompt(
        self,
        action_type: DestructiveActionType,
        context: Dict[str, Any]
    ) -> str:
        """
        Generate a confirmation prompt for the user.
        
        Args:
            action_type: Type of destructive action
            context: Additional context
            
        Returns:
            A user-friendly confirmation prompt
        """
        prompts = {
            DestructiveActionType.DELETE_ALL_HABITS: (
                f"⚠️ **This will delete all {context.get('count', 'your')} habits.** "
                "This action cannot be undone.\n\n"
                "Type **'confirm'** to proceed or **'cancel'** to abort."
            ),
            DestructiveActionType.RESET_STREAK: (
                f"⚠️ **This will reset your streak for '{context.get('habit_name', 'this habit')}'.** "
                "Your current streak will be lost.\n\n"
                "Type **'confirm'** to proceed or **'cancel'** to abort."
            ),
            DestructiveActionType.CLEAR_COMPLETIONS: (
                "⚠️ **This will clear all your completion history.** "
                "This action cannot be undone.\n\n"
                "Type **'confirm'** to proceed or **'cancel'** to abort."
            ),
            DestructiveActionType.DELETE_HABIT: (
                f"⚠️ **This will delete the habit '{context.get('habit_name', 'this habit')}'.** "
                "All associated data will be lost.\n\n"
                "Type **'confirm'** to proceed or **'cancel'** to abort."
            )
        }
        
        return prompts.get(
            action_type,
            "⚠️ **This is a destructive action.** Type **'confirm'** to proceed or **'cancel'** to abort."
        )
    
    def generate_cancellation_message(self) -> str:
        """Generate a message for when the user cancels."""
        return "✅ Action cancelled. No changes were made."
    
    def generate_expiration_message(self) -> str:
        """Generate a message for when the confirmation expires."""
        return "⏰ The confirmation has expired. Please try again if you still want to proceed."


# Singleton instance
_confirmation_service: Optional[ConfirmationFlowService] = None


def get_confirmation_service() -> ConfirmationFlowService:
    """Get the singleton confirmation service instance."""
    global _confirmation_service
    if _confirmation_service is None:
        _confirmation_service = ConfirmationFlowService()
    return _confirmation_service

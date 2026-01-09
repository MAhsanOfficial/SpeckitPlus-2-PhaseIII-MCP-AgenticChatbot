"""
Conversation database models for Phase III chatbot.

These models are purely additive - no modifications to Phase II schemas.
"""
from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
import uuid


class ConversationSession(SQLModel, table=True):
    """
    Represents a logical conversation thread belonging to a user.
    All conversation state is persisted to the database for stateless server operation.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(index=True, nullable=False)
    title: Optional[str] = Field(default=None, max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    last_activity_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationship to messages
    messages: List["ChatMessage"] = Relationship(back_populates="session")


class ChatMessage(SQLModel, table=True):
    """
    Represents an individual message within a conversation.
    Contains role (user/assistant/system), content, timestamp, and optional tool call metadata.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    session_id: str = Field(foreign_key="conversationsession.id", index=True, nullable=False)
    role: str = Field(nullable=False)  # "user", "assistant", "system"
    content: str = Field(nullable=False)
    timestamp: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    tool_calls: Optional[str] = Field(default=None)  # JSON string of tool calls if any
    tool_results: Optional[str] = Field(default=None)  # JSON string of tool results if any

    # Relationship to session
    session: ConversationSession = Relationship(back_populates="messages")

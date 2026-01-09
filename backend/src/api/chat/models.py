"""
Pydantic models for Phase III chat API.

These models define the request/response structure for the stateless chat endpoint.
Compatible with ChatKit frontend libraries.
"""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
import uuid


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""

    message: str = Field(
        ...,
        min_length=1,
        max_length=10000,
        description="The user's message to the chatbot"
    )
    conversation_id: Optional[str] = Field(
        default=None,
        description="Existing conversation ID to continue, or null for new conversation"
    )


class ChatMessageResponse(BaseModel):
    """Response message model."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    role: str = Field(..., description="Message role: 'user' or 'assistant'")
    content: str = Field(..., description="Message content")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ChatResponse(BaseModel):
    """Response model for chat endpoint. Compatible with ChatKit."""

    conversation_id: str = Field(
        ...,
        description="ID of the conversation session"
    )
    message: ChatMessageResponse = Field(
        ...,
        description="The assistant's response message"
    )
    suggestions: List[str] = Field(
        default_factory=list,
        description="Optional follow-up suggestion strings"
    )


class ConversationListItem(BaseModel):
    """Model for conversation list item."""

    id: str
    title: Optional[str]
    created_at: datetime
    last_activity_at: datetime
    message_count: int = 0


class ConversationListResponse(BaseModel):
    """Response for listing user's conversations."""

    conversations: List[ConversationListItem]
    total: int


class ErrorResponse(BaseModel):
    """Error response model."""

    error: str = Field(..., description="Error type")
    detail: str = Field(..., description="Error details")
    code: str = Field(..., description="Error code for categorization")


# Confirmation flow models
class ConfirmationState(BaseModel):
    """State for destructive action confirmation flow."""

    pending_action: str = Field(..., description="Type of action waiting confirmation")
    context: dict = Field(default_factory=dict, description="Action context")
    expires_at: datetime = Field(..., description="When this confirmation expires")

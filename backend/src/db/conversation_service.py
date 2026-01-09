"""
Conversation persistence service for Phase III chatbot.

Handles all database operations for conversation sessions and messages.
This is purely additive - no modifications to Phase II database operations.
"""
import json
from datetime import datetime
from typing import List, Optional
from sqlmodel import select, desc
from sqlmodel.ext.asyncio.session import AsyncSession
from uuid import UUID

from .models import ConversationSession, ChatMessage


class ConversationService:
    """Service for managing conversation persistence."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_session(self, user_id: str, title: Optional[str] = None) -> ConversationSession:
        """Create a new conversation session."""
        session = ConversationSession(
            user_id=user_id,
            title=title,
            created_at=datetime.utcnow(),
            last_activity_at=datetime.utcnow()
        )
        self.session.add(session)
        await self.session.commit()
        await self.session.refresh(session)
        return session

    async def get_session(self, session_id: str, user_id: str) -> Optional[ConversationSession]:
        """Get a conversation session by ID, ensuring user ownership."""
        result = await self.session.execute(
            select(ConversationSession)
            .where(ConversationSession.id == session_id)
            .where(ConversationSession.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_user_sessions(
        self, user_id: str, limit: int = 20, offset: int = 0
    ) -> List[ConversationSession]:
        """Get all conversation sessions for a user."""
        result = await self.session.execute(
            select(ConversationSession)
            .where(ConversationSession.user_id == user_id)
            .order_by(desc(ConversationSession.last_activity_at))
            .offset(offset)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def update_session_activity(self, session_id: str) -> None:
        """Update the last activity timestamp for a session."""
        result = await self.session.execute(
            select(ConversationSession).where(ConversationSession.id == session_id)
        )
        session = result.scalar_one_or_none()
        if session:
            session.last_activity_at = datetime.utcnow()
            await self.session.commit()

    async def add_message(
        self,
        session_id: str,
        role: str,
        content: str,
        tool_calls: Optional[List[dict]] = None,
        tool_results: Optional[List[dict]] = None
    ) -> ChatMessage:
        """Add a message to a conversation session."""
        message = ChatMessage(
            session_id=session_id,
            role=role,
            content=content,
            timestamp=datetime.utcnow(),
            tool_calls=json.dumps(tool_calls) if tool_calls else None,
            tool_results=json.dumps(tool_results) if tool_results else None
        )
        self.session.add(message)
        await self.session.commit()
        await self.session.refresh(message)

        # Update session activity
        await self.update_session_activity(session_id)

        return message

    async def get_session_messages(
        self,
        session_id: str,
        user_id: str,
        limit: int = 50
    ) -> List[ChatMessage]:
        """Get messages for a session, ensuring user ownership."""
        # First verify session belongs to user
        session = await self.get_session(session_id, user_id)
        if not session:
            return []

        result = await self.session.execute(
            select(ChatMessage)
            .where(ChatMessage.session_id == session_id)
            .order_by(ChatMessage.timestamp)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def delete_session(self, session_id: str, user_id: str) -> bool:
        """Delete a conversation session and all its messages."""
        session = await self.get_session(session_id, user_id)
        if not session:
            return False

        await self.session.delete(session)
        await self.session.commit()
        return True

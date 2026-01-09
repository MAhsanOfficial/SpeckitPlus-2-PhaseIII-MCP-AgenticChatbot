from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from datetime import date as date_type
from typing import List

from src.models.habit import Habit, Completion, CompletionBase
from src.core.db import get_session
from src.core.deps import get_current_user_id

# Phase II router
router = APIRouter(prefix="/habits", tags=["completions"])

# Phase III router (with user_id in path)
router_v3 = APIRouter(prefix="/{user_id}/habits", tags=["completions-v3"])

# Completions list endpoint
completions_router = APIRouter(prefix="/{user_id}/completions", tags=["completions-list"])


def verify_user_isolation(path_user_id: str, token_user_id: str) -> None:
    """Verify the user_id in URL matches the authenticated user."""
    if path_user_id != token_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot access another user's data"
        )

@router.post("/{habit_id}/toggle", response_model=Completion)
async def toggle_completion(
    habit_id: UUID,
    completion_in: CompletionBase,
    session: AsyncSession = Depends(get_session),
    user_id: str = Depends(get_current_user_id)
):
    # Verify ownership
    habit_stmt = select(Habit).where(Habit.id == habit_id, Habit.user_id == user_id)
    habit_res = await session.execute(habit_stmt)
    habit = habit_res.scalar_one_or_none()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")

    # Check for existing completion on this date
    stmt = select(Completion).where(
        Completion.habit_id == habit_id,
        Completion.date == completion_in.date
    )
    res = await session.execute(stmt)
    completion = res.scalar_one_or_none()

    if completion:
        # Toggle existing
        completion.status = not completion.status
        session.add(completion)
    else:
        # Create new
        completion = Completion(
            habit_id=habit_id,
            date=completion_in.date,
            status=completion_in.status
        )
        session.add(completion)

    await session.commit()
    await session.refresh(completion)
    return completion


# ============================================================================
# Phase III Endpoints (with user_id in path for frontend compatibility)
# ============================================================================

@router_v3.post("/{habit_id}/toggle", response_model=Completion)
async def toggle_completion_v3(
    user_id: str,
    habit_id: UUID,
    completion_in: CompletionBase,
    session: AsyncSession = Depends(get_session),
    token_user_id: str = Depends(get_current_user_id)
):
    """Toggle completion with user_id in path (Phase III compatible)."""
    verify_user_isolation(user_id, token_user_id)
    
    # Verify ownership
    habit_stmt = select(Habit).where(Habit.id == habit_id, Habit.user_id == user_id)
    habit_res = await session.execute(habit_stmt)
    habit = habit_res.scalar_one_or_none()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")

    # Check for existing completion on this date
    stmt = select(Completion).where(
        Completion.habit_id == habit_id,
        Completion.date == completion_in.date
    )
    res = await session.execute(stmt)
    completion = res.scalar_one_or_none()

    if completion:
        # Toggle existing
        completion.status = not completion.status
        session.add(completion)
    else:
        # Create new
        completion = Completion(
            habit_id=habit_id,
            date=completion_in.date,
            status=completion_in.status
        )
        session.add(completion)

    await session.commit()
    await session.refresh(completion)
    return completion


# ============================================================================
# Completions List Endpoint
# ============================================================================

@completions_router.get("/", response_model=List[Completion])
async def list_completions(
    user_id: str,
    date: str | None = None,
    session: AsyncSession = Depends(get_session),
    token_user_id: str = Depends(get_current_user_id)
):
    """List all completions for a user, optionally filtered by date."""
    verify_user_isolation(user_id, token_user_id)
    
    # Get all habits for this user
    habits_stmt = select(Habit).where(Habit.user_id == user_id)
    habits_res = await session.execute(habits_stmt)
    habits = habits_res.scalars().all()
    habit_ids = [h.id for h in habits]
    
    if not habit_ids:
        return []
    
    # Build completions query
    stmt = select(Completion).where(Completion.habit_id.in_(habit_ids))
    
    if date:
        # Convert string date to date object
        from datetime import datetime
        try:
            date_obj = datetime.strptime(date, "%Y-%m-%d").date()
            stmt = stmt.where(Completion.date == date_obj)
        except ValueError:
            pass  # Invalid date format, skip filter
    
    results = await session.execute(stmt)
    completions = results.scalars().all()
    return completions

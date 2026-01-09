from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select, SQLModel
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from src.models.habit import Habit, HabitBase
from src.core.db import get_session
from src.core.deps import get_current_user_id
from src.services.gemini_service import get_habit_feedback

# Phase II router (original endpoints)
router = APIRouter(prefix="/habits", tags=["habits"])

# Phase III router (with user_id in path for frontend compatibility)
router_v3 = APIRouter(prefix="/{user_id}/habits", tags=["habits-v3"])

@router.post("/", response_model=Habit)
async def create_habit(
    habit_in: HabitBase,
    session: AsyncSession = Depends(get_session),
    user_id: str = Depends(get_current_user_id)
):
    # Fetch AI Analysis from Gemini Protocol
    pros, cons = get_habit_feedback(habit_in.name, habit_in.description or "")

    habit = Habit(
        name=habit_in.name,
        description=habit_in.description,
        user_id=user_id,
        pros=pros,
        cons=cons
    )
    session.add(habit)
    await session.commit()
    await session.refresh(habit)
    return habit

@router.get("/", response_model=List[Habit])
async def list_habits(
    session: AsyncSession = Depends(get_session),
    user_id: str = Depends(get_current_user_id)
):
    statement = select(Habit).where(Habit.user_id == user_id)
    results = await session.execute(statement)
    habits = results.scalars().all()
    return habits

@router.get("/{habit_id}", response_model=Habit)
async def get_habit(
    habit_id: UUID,
    session: AsyncSession = Depends(get_session),
    user_id: str = Depends(get_current_user_id)
):
    statement = select(Habit).where(Habit.id == habit_id, Habit.user_id == user_id)
    results = await session.execute(statement)
    habit = results.scalar_one_or_none()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    return habit

class HabitUpdate(SQLModel):
    name: str | None = None
    description: str | None = None

@router.put("/{habit_id}", response_model=Habit)
async def update_habit(
    habit_id: UUID,
    habit_update: HabitUpdate,
    session: AsyncSession = Depends(get_session),
    user_id: str = Depends(get_current_user_id)
):
    statement = select(Habit).where(Habit.id == habit_id, Habit.user_id == user_id)
    results = await session.execute(statement)
    habit = results.scalar_one_or_none()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    
    # Update only provided fields
    if habit_update.name is not None:
        habit.name = habit_update.name
    if habit_update.description is not None:
        habit.description = habit_update.description
    
    # Regenerate AI feedback if name or description changed
    if habit_update.name or habit_update.description:
        pros, cons = get_habit_feedback(habit.name, habit.description or "")
        habit.pros = pros
        habit.cons = cons
    
    session.add(habit)
    await session.commit()
    await session.refresh(habit)
    return habit

@router.delete("/{habit_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_habit(
    habit_id: UUID,
    session: AsyncSession = Depends(get_session),
    user_id: str = Depends(get_current_user_id)
):
    statement = select(Habit).where(Habit.id == habit_id, Habit.user_id == user_id)
    results = await session.execute(statement)
    habit = results.scalar_one_or_none()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    await session.delete(habit)
    await session.commit()
    return None


# ============================================================================
# Phase III Endpoints (with user_id in path for frontend compatibility)
# ============================================================================

def verify_user_isolation(path_user_id: str, token_user_id: str) -> None:
    """Verify the user_id in URL matches the authenticated user."""
    if path_user_id != token_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot access another user's data"
        )


@router_v3.get("/", response_model=List[Habit])
async def list_habits_v3(
    user_id: str,
    session: AsyncSession = Depends(get_session),
    token_user_id: str = Depends(get_current_user_id)
):
    """List habits with user_id in path (Phase III compatible)."""
    verify_user_isolation(user_id, token_user_id)
    
    statement = select(Habit).where(Habit.user_id == user_id)
    results = await session.execute(statement)
    habits = results.scalars().all()
    return habits


@router_v3.post("/", response_model=Habit)
async def create_habit_v3(
    user_id: str,
    habit_in: HabitBase,
    session: AsyncSession = Depends(get_session),
    token_user_id: str = Depends(get_current_user_id)
):
    """Create habit with user_id in path (Phase III compatible)."""
    print(f"[HABIT API] create_habit_v3 called - user_id: {user_id}, token_user_id: {token_user_id}")
    print(f"[HABIT API] habit_in: {habit_in}")
    
    verify_user_isolation(user_id, token_user_id)
    
    print(f"[HABIT API] Getting AI feedback for: {habit_in.name}")
    # Fetch AI Analysis from Gemini Protocol
    pros, cons = get_habit_feedback(habit_in.name, habit_in.description or "")
    print(f"[HABIT API] AI feedback received")

    habit = Habit(
        name=habit_in.name,
        description=habit_in.description,
        user_id=user_id,
        pros=pros,
        cons=cons
    )
    session.add(habit)
    await session.commit()
    await session.refresh(habit)
    print(f"[HABIT API] Habit created: {habit.id}")
    return habit


@router_v3.get("/{habit_id}", response_model=Habit)
async def get_habit_v3(
    user_id: str,
    habit_id: UUID,
    session: AsyncSession = Depends(get_session),
    token_user_id: str = Depends(get_current_user_id)
):
    """Get habit with user_id in path (Phase III compatible)."""
    verify_user_isolation(user_id, token_user_id)
    
    statement = select(Habit).where(Habit.id == habit_id, Habit.user_id == user_id)
    results = await session.execute(statement)
    habit = results.scalar_one_or_none()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    return habit


@router_v3.put("/{habit_id}", response_model=Habit)
async def update_habit_v3(
    user_id: str,
    habit_id: UUID,
    habit_update: HabitUpdate,
    session: AsyncSession = Depends(get_session),
    token_user_id: str = Depends(get_current_user_id)
):
    """Update habit with user_id in path (Phase III compatible)."""
    verify_user_isolation(user_id, token_user_id)
    
    statement = select(Habit).where(Habit.id == habit_id, Habit.user_id == user_id)
    results = await session.execute(statement)
    habit = results.scalar_one_or_none()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    
    # Update only provided fields
    if habit_update.name is not None:
        habit.name = habit_update.name
    if habit_update.description is not None:
        habit.description = habit_update.description
    
    # Regenerate AI feedback if name or description changed
    if habit_update.name or habit_update.description:
        pros, cons = get_habit_feedback(habit.name, habit.description or "")
        habit.pros = pros
        habit.cons = cons
    
    session.add(habit)
    await session.commit()
    await session.refresh(habit)
    return habit


@router_v3.delete("/{habit_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_habit_v3(
    user_id: str,
    habit_id: UUID,
    session: AsyncSession = Depends(get_session),
    token_user_id: str = Depends(get_current_user_id)
):
    """Delete habit with user_id in path (Phase III compatible)."""
    verify_user_isolation(user_id, token_user_id)
    
    statement = select(Habit).where(Habit.id == habit_id, Habit.user_id == user_id)
    results = await session.execute(statement)
    habit = results.scalar_one_or_none()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    await session.delete(habit)
    await session.commit()
    return None

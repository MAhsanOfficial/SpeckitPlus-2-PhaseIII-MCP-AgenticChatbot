from fastapi import APIRouter, Depends
from sqlmodel import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date, timedelta
from typing import Dict, Any, List

from src.models.habit import Habit, Completion
from src.core.db import get_session
from src.core.deps import get_current_user_id

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/weekly")
async def get_weekly_analytics(
    session: AsyncSession = Depends(get_session),
    user_id: str = Depends(get_current_user_id)
):
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())  # Monday

    # Get all habits for user
    habit_stmt = select(Habit).where(Habit.user_id == user_id)
    habit_res = await session.execute(habit_stmt)
    habits = habit_res.scalars().all()
    habit_ids = [h.id for h in habits]

    if not habit_ids:
        return {"data": []}

    # Get completions for these habits this week
    comp_stmt = select(Completion).where(
        Completion.habit_id.in_(habit_ids),
        Completion.date >= start_of_week,
        Completion.status == True
    )
    comp_res = await session.execute(comp_stmt)
    completions = comp_res.scalars().all()

    # Aggregate by day
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    daily_counts = {start_of_week + timedelta(days=i): 0 for i in range(7)}

    for c in completions:
        if c.date in daily_counts:
            daily_counts[c.date] += 1

    chart_data = [
        {"day": days[i], "count": daily_counts[start_of_week + timedelta(days=i)]}
        for i in range(7)
    ]

    return {"data": chart_data}

@router.get("/summary")
async def get_summary(
    session: AsyncSession = Depends(get_session),
    user_id: str = Depends(get_current_user_id)
):
    # Total habits
    habit_stmt = select(Habit).where(Habit.user_id == user_id)
    habit_res = await session.execute(habit_stmt)
    habits = habit_res.scalars().all()

    total_habits = len(habits)
    total_completions = 0

    # This is a bit heavy, in production we'd use better SQL aggregations
    # but for Phase II / MVP this works.
    for habit in habits:
        comp_stmt = select(Completion).where(
            Completion.habit_id == habit.id,
            Completion.status == True
        )
        comp_res = await session.execute(comp_stmt)
        total_completions += len(comp_res.scalars().all())

    return {
        "total_habits": total_habits,
        "total_completions": total_completions,
    }

"""
Direct database service for habit operations.
Used by chatbot to perform CRUD operations without going through Phase II APIs.
"""
from typing import List, Optional, Dict, Any
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from datetime import datetime, date

from src.models.habit import Habit, HabitBase, Completion


class HabitService:
    """Service for direct database access to habits."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def list_habits(self, user_id: str) -> List[Dict[str, Any]]:
        """List all habits for a user."""
        statement = select(Habit).where(Habit.user_id == user_id)
        results = await self.session.execute(statement)
        habits = results.scalars().all()
        
        # Convert to dict and add streak info
        habit_list = []
        for habit in habits:
            habit_dict = {
                "id": str(habit.id),
                "name": habit.name,
                "description": habit.description,
                "user_id": habit.user_id,
                "created_at": habit.created_at.isoformat() if habit.created_at else None,
                "pros": habit.pros,
                "cons": habit.cons,
            }
            
            # Calculate streak
            streak = await self._calculate_streak(habit.id, user_id)
            habit_dict["streak"] = streak
            
            habit_list.append(habit_dict)
        
        return habit_list
    
    async def get_habit(self, habit_id: UUID, user_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific habit."""
        statement = select(Habit).where(Habit.id == habit_id, Habit.user_id == user_id)
        result = await self.session.execute(statement)
        habit = result.scalar_one_or_none()
        
        if not habit:
            return None
        
        return {
            "id": str(habit.id),
            "name": habit.name,
            "description": habit.description,
            "user_id": habit.user_id,
            "created_at": habit.created_at.isoformat() if habit.created_at else None,
            "pros": habit.pros,
            "cons": habit.cons,
        }
    
    async def create_habit(
        self, 
        user_id: str, 
        name: str, 
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a new habit."""
        from src.services.gemini_service import get_habit_feedback
        
        # Get AI feedback
        pros, cons = get_habit_feedback(name, description or "")
        
        habit = Habit(
            name=name,
            description=description,
            user_id=user_id,
            pros=pros,
            cons=cons
        )
        
        self.session.add(habit)
        await self.session.commit()
        await self.session.refresh(habit)
        
        return {
            "id": str(habit.id),
            "name": habit.name,
            "description": habit.description,
            "user_id": habit.user_id,
            "created_at": habit.created_at.isoformat() if habit.created_at else None,
            "pros": habit.pros,
            "cons": habit.cons,
        }
    
    async def update_habit(
        self,
        habit_id: UUID,
        user_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Update a habit."""
        statement = select(Habit).where(Habit.id == habit_id, Habit.user_id == user_id)
        result = await self.session.execute(statement)
        habit = result.scalar_one_or_none()
        
        if not habit:
            return None
        
        if name is not None:
            habit.name = name
        if description is not None:
            habit.description = description
        
        await self.session.commit()
        await self.session.refresh(habit)
        
        return {
            "id": str(habit.id),
            "name": habit.name,
            "description": habit.description,
            "user_id": habit.user_id,
            "created_at": habit.created_at.isoformat() if habit.created_at else None,
            "pros": habit.pros,
            "cons": habit.cons,
        }
    
    async def delete_habit(self, habit_id: UUID, user_id: str) -> bool:
        """Delete a habit."""
        statement = select(Habit).where(Habit.id == habit_id, Habit.user_id == user_id)
        result = await self.session.execute(statement)
        habit = result.scalar_one_or_none()
        
        if not habit:
            return False
        
        await self.session.delete(habit)
        await self.session.commit()
        return True
    
    async def log_completion(
        self,
        habit_id: UUID,
        user_id: str,
        completion_date: Optional[date] = None,
        status: bool = True,
        note: Optional[str] = None
    ) -> Dict[str, Any]:
        """Log or toggle a habit completion."""
        # Verify habit belongs to user
        habit_statement = select(Habit).where(Habit.id == habit_id, Habit.user_id == user_id)
        habit_result = await self.session.execute(habit_statement)
        habit = habit_result.scalar_one_or_none()
        
        if not habit:
            raise ValueError("Habit not found")
        
        # Use today if no date provided
        if completion_date is None:
            completion_date = date.today()
        
        # Check if completion already exists
        completion_statement = select(Completion).where(
            Completion.habit_id == habit_id,
            Completion.date == completion_date
        )
        completion_result = await self.session.execute(completion_statement)
        existing_completion = completion_result.scalar_one_or_none()
        
        if existing_completion:
            # Toggle existing completion
            existing_completion.status = status
            if note:
                existing_completion.note = note
            await self.session.commit()
            await self.session.refresh(existing_completion)
            
            return {
                "id": str(existing_completion.id),
                "habit_id": str(existing_completion.habit_id),
                "date": existing_completion.date.isoformat(),
                "status": existing_completion.status,
                "note": existing_completion.note,
                "toggled": True
            }
        else:
            # Create new completion
            completion = Completion(
                habit_id=habit_id,
                date=completion_date,
                status=status,
                note=note
            )
            self.session.add(completion)
            await self.session.commit()
            await self.session.refresh(completion)
            
            return {
                "id": str(completion.id),
                "habit_id": str(completion.habit_id),
                "date": completion.date.isoformat(),
                "status": completion.status,
                "note": completion.note,
                "created": True
            }
    
    async def _calculate_streak(self, habit_id: UUID, user_id: str) -> int:
        """Calculate current streak for a habit."""
        # Get completions for the last 30 days
        from datetime import timedelta
        
        today = date.today()
        thirty_days_ago = today - timedelta(days=30)
        
        statement = select(Completion).where(
            Completion.habit_id == habit_id,
            Completion.date >= thirty_days_ago,
            Completion.date <= today,
            Completion.status == True
        ).order_by(Completion.date.desc())
        
        result = await self.session.execute(statement)
        completions = result.scalars().all()
        
        if not completions:
            return 0
        
        # Calculate consecutive days from today backwards
        streak = 0
        current_date = today
        
        completion_dates = {c.date for c in completions}
        
        while current_date in completion_dates:
            streak += 1
            current_date -= timedelta(days=1)
        
        return streak

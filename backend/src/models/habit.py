from datetime import datetime, date as date_type
from uuid import UUID, uuid4
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class HabitBase(SQLModel):
    name: str = Field(index=True, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    pros: Optional[str] = Field(default=None) # AI Generated
    cons: Optional[str] = Field(default=None) # AI Generated

class Habit(HabitBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: str = Field(index=True)  # From Better Auth
    created_at: datetime = Field(default_factory=datetime.utcnow)

    completions: List["Completion"] = Relationship(back_populates="habit", cascade_delete=True)

class CompletionBase(SQLModel):
    date: date_type = Field(index=True)
    status: bool = Field(default=True)
    note: Optional[str] = Field(default=None, max_length=200)

class Completion(CompletionBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    habit_id: UUID = Field(foreign_key="habit.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    habit: Habit = Relationship(back_populates="completions")

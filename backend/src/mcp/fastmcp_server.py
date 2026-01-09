"""
FastMCP Server for Habit Tracking Operations.

This server provides MCP tools for the chatbot to perform CRUD operations
on habits through a standardized MCP protocol.
"""
from fastmcp import FastMCP
from typing import Optional
from datetime import date
from uuid import UUID

from src.services.habit_service import HabitService
from src.core.db import get_session

# Create FastMCP server
mcp = FastMCP("Habit Tracker MCP Server")

# Store session for database access
_db_session = None


async def get_habit_service():
    """Get HabitService instance with database session."""
    global _db_session
    if _db_session is None:
        async for session in get_session():
            _db_session = session
            break
    return HabitService(_db_session)


@mcp.tool()
async def list_habits(user_id: str) -> dict:
    """
    List all habits for a user.
    
    Args:
        user_id: The user's unique identifier
        
    Returns:
        Dictionary with habits list and count
    """
    service = await get_habit_service()
    habits = await service.list_habits(user_id)
    
    return {
        "success": True,
        "habits": habits,
        "count": len(habits)
    }


@mcp.tool()
async def create_habit(user_id: str, name: str, description: Optional[str] = None) -> dict:
    """
    Create a new habit for a user.
    
    Args:
        user_id: The user's unique identifier
        name: Name of the habit
        description: Optional description of the habit
        
    Returns:
        Dictionary with created habit details
    """
    service = await get_habit_service()
    habit = await service.create_habit(user_id, name, description)
    
    return {
        "success": True,
        "habit": habit,
        "message": f"Created habit: {name}"
    }


@mcp.tool()
async def log_completion(
    user_id: str,
    habit_id: str,
    completion_date: Optional[str] = None,
    status: bool = True,
    note: Optional[str] = None
) -> dict:
    """
    Log or toggle a habit completion.
    
    Args:
        user_id: The user's unique identifier
        habit_id: The habit's unique identifier
        completion_date: Date in YYYY-MM-DD format (defaults to today)
        status: Completion status (default True)
        note: Optional note about the completion
        
    Returns:
        Dictionary with completion details
    """
    service = await get_habit_service()
    habit_uuid = UUID(habit_id)
    
    result = await service.log_completion(
        habit_uuid,
        user_id,
        date.fromisoformat(completion_date) if completion_date else None,
        status,
        note
    )
    
    return {
        "success": True,
        "result": result,
        "message": f"Habit {'completed' if status else 'uncompleted'}"
    }


@mcp.tool()
async def get_habit_streak(user_id: str, habit_id: Optional[str] = None) -> dict:
    """
    Get streak information for habits.
    
    Args:
        user_id: The user's unique identifier
        habit_id: Optional specific habit ID, or get all
        
    Returns:
        Dictionary with streak information
    """
    service = await get_habit_service()
    
    if habit_id:
        # Get specific habit with streak
        habit_uuid = UUID(habit_id)
        habit = await service.get_habit(habit_uuid, user_id)
        if not habit:
            return {"success": False, "error": "Habit not found"}
        
        # Calculate streak
        streak = await service._calculate_streak(habit_uuid, user_id)
        
        return {
            "success": True,
            "habit": habit,
            "current_streak": streak
        }
    else:
        # Get all habits with streaks
        habits = await service.list_habits(user_id)
        
        return {
            "success": True,
            "habits": habits,
            "summary": {
                "total_habits": len(habits),
                "total_streak_days": sum(h.get("streak", 0) for h in habits)
            }
        }


@mcp.tool()
async def update_habit(
    user_id: str,
    habit_id: str,
    name: Optional[str] = None,
    description: Optional[str] = None
) -> dict:
    """
    Update a habit's details.
    
    Args:
        user_id: The user's unique identifier
        habit_id: The habit's unique identifier
        name: New name for the habit
        description: New description for the habit
        
    Returns:
        Dictionary with updated habit details
    """
    service = await get_habit_service()
    habit_uuid = UUID(habit_id)
    
    habit = await service.update_habit(habit_uuid, user_id, name, description)
    
    if not habit:
        return {"success": False, "error": "Habit not found"}
    
    return {
        "success": True,
        "habit": habit,
        "message": "Habit updated successfully"
    }


@mcp.tool()
async def delete_habit(user_id: str, habit_id: str) -> dict:
    """
    Delete a habit.
    
    Args:
        user_id: The user's unique identifier
        habit_id: The habit's unique identifier
        
    Returns:
        Dictionary with deletion status
    """
    service = await get_habit_service()
    habit_uuid = UUID(habit_id)
    
    success = await service.delete_habit(habit_uuid, user_id)
    
    if not success:
        return {"success": False, "error": "Habit not found"}
    
    return {
        "success": True,
        "message": "Habit deleted successfully"
    }


# Export the MCP server
__all__ = ["mcp"]

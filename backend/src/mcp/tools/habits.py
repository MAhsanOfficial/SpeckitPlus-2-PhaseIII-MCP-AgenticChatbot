"""
MCP tools for habit tracking operations.

These tools delegate to Phase II APIs following constitution principles:
- MCP-first tool interface (IX)
- Stateless and deterministic (VIII)
- Phase II sacred codebase (VI)
"""
from typing import Any, Dict, List, Optional
from datetime import date as date_type, datetime
import json

from .base import BaseMCPTool
from .phase2_client import Phase2APIClient, create_phase2_client


class HabitListTool(BaseMCPTool):
    """MCP tool for listing user habits."""

    @property
    def name(self) -> str:
        return "habit_list"

    @property
    def description(self) -> str:
        return "List all habits for the authenticated user with their current streak information."

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "User ID for the request"
                }
            },
            "required": []
        }

    async def execute(self, jwt_token: str, user_id: Optional[str] = None) -> Dict[str, Any]:
        """Execute the habit list tool."""
        client = await create_phase2_client(jwt_token, user_id)
        habits = await client.list_habits()

        # Add computed streak data for each habit
        for habit in habits:
            habit["streak"] = await self._calculate_streak(habit["id"], jwt_token, user_id)

        return {
            "success": True,
            "habits": habits,
            "count": len(habits)
        }

    async def _calculate_streak(self, habit_id: str, jwt_token: str, user_id: Optional[str] = None) -> int:
        """Calculate current streak for a habit."""
        client = await create_phase2_client(jwt_token, user_id)
        analytics = await client.get_weekly_analytics()

        # Count completed days in the chart data
        data = analytics.get("data", [])
        streak = sum(item.get("count", 0) for item in data if item.get("count", 0) > 0)
        return streak


class HabitGetTool(BaseMCPTool):
    """MCP tool for getting a specific habit."""

    @property
    def name(self) -> str:
        return "habit_get"

    @property
    def description(self) -> str:
        return "Get detailed information about a specific habit by its ID."

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "habit_id": {
                    "type": "string",
                    "description": "The unique identifier of the habit"
                }
            },
            "required": ["habit_id"]
        }

    async def execute(self, habit_id: str, jwt_token: str) -> Dict[str, Any]:
        """Execute the habit get tool."""
        client = await create_phase2_client(jwt_token)
        habit = await client.get_habit(habit_id)
        return {
            "success": True,
            "habit": habit
        }


class HabitCreateTool(BaseMCPTool):
    """MCP tool for creating a new habit."""

    @property
    def name(self) -> str:
        return "habit_create"

    @property
    def description(self) -> str:
        return "Create a new habit with the given name and optional description."

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Name of the habit (max 100 characters)"
                },
                "description": {
                    "type": "string",
                    "description": "Optional description of the habit"
                }
            },
            "required": ["name"]
        }

    async def execute(
        self,
        name: str,
        description: Optional[str] = None,
        jwt_token: str = ""
    ) -> Dict[str, Any]:
        """Execute the habit create tool."""
        client = await create_phase2_client(jwt_token)
        habit = await client.create_habit(name=name, description=description)
        return {
            "success": True,
            "habit": habit,
            "message": f"Created habit: {name}"
        }


class HabitLogCompletionTool(BaseMCPTool):
    """MCP tool for logging habit completion."""

    @property
    def name(self) -> str:
        return "habit_log_completion"

    @property
    def description(self) -> str:
        return "Log or toggle habit completion for a specific date. If already completed, this will un-complete it."

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "habit_id": {
                    "type": "string",
                    "description": "The unique identifier of the habit"
                },
                "date": {
                    "type": "string",
                    "description": "Date in YYYY-MM-DD format (defaults to today)"
                },
                "status": {
                    "type": "boolean",
                    "description": "Completion status (default true)"
                },
                "note": {
                    "type": "string",
                    "description": "Optional note about the completion"
                }
            },
            "required": ["habit_id"]
        }

    async def execute(
        self,
        habit_id: str,
        date: Optional[str] = None,
        status: bool = True,
        note: Optional[str] = None,
        jwt_token: str = ""
    ) -> Dict[str, Any]:
        """Execute the habit log completion tool."""
        client = await create_phase2_client(jwt_token)

        # Default to today if no date provided
        completion_date = date or datetime.now().strftime("%Y-%m-%d")

        result = await client.toggle_habit_completion(
            habit_id=habit_id,
            completion_date=completion_date,
            status=status,
            note=note
        )

        action = "completed" if status else "uncompleted"
        return {
            "success": True,
            "result": result,
            "message": f"Habit {action} for {completion_date}"
        }


class HabitStreakTool(BaseMCPTool):
    """MCP tool for getting habit streak information."""

    @property
    def name(self) -> str:
        return "habit_streak"

    @property
    def description(self) -> str:
        return "Get streak information for all habits or a specific habit."

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "habit_id": {
                    "type": "string",
                    "description": "Optional: specific habit ID, or get all"
                }
            },
            "required": []
        }

    async def execute(
        self,
        habit_id: Optional[str] = None,
        jwt_token: str = ""
    ) -> Dict[str, Any]:
        """Execute the habit streak tool."""
        client = await create_phase2_client(jwt_token)

        if habit_id:
            habit = await client.get_habit(habit_id)
            weekly = await client.get_weekly_analytics()

            # Calculate streak from weekly data
            data = weekly.get("data", [])
            streak = sum(item.get("count", 0) for item in data if item.get("count", 0) > 0)

            return {
                "success": True,
                "habit": habit,
                "current_streak": streak,
                "weekly_data": data
            }
        else:
            habits = await client.list_habits()
            weekly = await client.get_weekly_analytics()

            # Calculate streaks for all habits
            habit_streaks = []
            data = weekly.get("data", [])

            for habit in habits:
                streak = sum(
                    item.get("count", 0)
                    for item in data
                    if item.get("count", 0) > 0
                )
                habit_streaks.append({
                    "id": habit["id"],
                    "name": habit["name"],
                    "current_streak": streak
                })

            return {
                "success": True,
                "habits": habit_streaks,
                "summary": {
                    "total_habits": len(habits),
                    "total_streak_days": sum(h["current_streak"] for h in habit_streaks)
                }
            }


class HabitSummaryTool(BaseMCPTool):
    """MCP tool for getting habit summary/analytics."""

    @property
    def name(self) -> str:
        return "habit_summary"

    @property
    def description(self) -> str:
        return "Get overall habit tracking summary including total habits and completions."

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {},
            "required": []
        }

    async def execute(self, jwt_token: str) -> Dict[str, Any]:
        """Execute the habit summary tool."""
        client = await create_phase2_client(jwt_token)

        summary = await client.get_summary()
        weekly = await client.get_weekly_analytics()

        return {
            "success": True,
            "summary": summary,
            "weekly_data": weekly.get("data", [])
        }


# Registry function for all habit tools
def get_habit_tools() -> List[BaseMCPTool]:
    """Return all habit-related MCP tools."""
    return [
        HabitListTool(),
        HabitGetTool(),
        HabitCreateTool(),
        HabitLogCompletionTool(),
        HabitStreakTool(),
        HabitSummaryTool()
    ]

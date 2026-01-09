"""
Phase II API client for delegation.

This module provides HTTP-based access to Phase II APIs.
Following constitution principles: AI NEVER touches database directly.
All data access goes through this client which delegates to Phase II APIs.
"""
import os
from typing import Any, Dict, List, Optional
from datetime import date
import httpx

# Phase II API base URL (same server, different routes)
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
DEV_MODE = os.getenv("DEV_MODE", "true").lower() == "true"


class Phase2APIClient:
    """
    HTTP client for delegating to Phase II APIs.

    This client ensures:
    - AI agents never access database directly
    - All operations go through Phase II APIs
    - Stateless and deterministic behavior
    """

    def __init__(self, jwt_token: str, user_id: Optional[str] = None):
        self.jwt_token = jwt_token
        self.user_id = user_id
        self.headers = {
            "Authorization": f"Bearer {jwt_token}",
            "Content-Type": "application/json"
        }

    async def _request(
        self,
        method: str,
        endpoint: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Make HTTP request to Phase II API."""
        async with httpx.AsyncClient() as client:
            url = f"{API_BASE_URL}{endpoint}"
            print(f"[DEBUG] Phase2APIClient: {method} {url}")
            print(f"[DEBUG] Headers: {self.headers}")
            
            response = await client.request(
                method,
                url,
                headers=self.headers,
                **kwargs
            )
            
            print(f"[DEBUG] Response status: {response.status_code}")
            
            if response.status_code >= 400:
                print(f"[DEBUG] Response error: {response.text}")
            
            response.raise_for_status()
            return response.json()

    # Habit APIs

    async def list_habits(self) -> List[Dict[str, Any]]:
        """List all habits for the authenticated user."""
        return await self._request("GET", "/api/habits/")

    async def get_habit(self, habit_id: str) -> Dict[str, Any]:
        """Get a specific habit."""
        return await self._request("GET", f"/api/habits/{habit_id}")

    async def create_habit(
        self,
        name: str,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a new habit."""
        return await self._request(
            "POST",
            "/api/habits/",
            json={"name": name, "description": description}
        )

    async def update_habit(
        self,
        habit_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """Update a habit."""
        update_data = {}
        if name is not None:
            update_data["name"] = name
        if description is not None:
            update_data["description"] = description
        return await self._request(
            "PUT",
            f"/api/habits/{habit_id}",
            json=update_data
        )

    async def delete_habit(self, habit_id: str) -> None:
        """Delete a habit."""
        await self._request("DELETE", f"/api/habits/{habit_id}")

    # Completion APIs

    async def toggle_habit_completion(
        self,
        habit_id: str,
        completion_date: str,
        status: bool = True,
        note: Optional[str] = None
    ) -> Dict[str, Any]:
        """Toggle or create a habit completion."""
        return await self._request(
            "POST",
            f"/api/habits/{habit_id}/toggle",
            json={
                "date": completion_date,
                "status": status,
                "note": note
            }
        )

    # Analytics APIs

    async def get_weekly_analytics(self) -> Dict[str, Any]:
        """Get weekly habit analytics."""
        return await self._request("GET", "/api/analytics/weekly")

    async def get_summary(self) -> Dict[str, Any]:
        """Get overall summary."""
        return await self._request("GET", "/api/analytics/summary")


# Factory function for creating client with JWT
async def create_phase2_client(jwt_token: str, user_id: Optional[str] = None) -> Phase2APIClient:
    """Create a Phase II API client with the given JWT token."""
    return Phase2APIClient(jwt_token, user_id)

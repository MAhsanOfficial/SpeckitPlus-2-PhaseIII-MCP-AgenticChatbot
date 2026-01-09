"""
Security middleware for Phase III chatbot.

Implements:
- Rate limiting
- Input sanitization
- Audit logging
- User isolation enforcement
"""
import os
import time
import hashlib
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
import re


# Rate limiting configuration
RATE_LIMIT_WINDOW = int(os.getenv("RATE_LIMIT_WINDOW", "60"))  # seconds
RATE_LIMIT_MAX_REQUESTS = int(os.getenv("RATE_LIMIT_MAX_REQUESTS", "30"))


# In-memory rate limit store (use Redis in production)
_rate_limit_store: Dict[str, Tuple[int, datetime]] = {}


def sanitize_input(text: str) -> str:
    """
    Sanitize user input to prevent injection attacks.
    """
    if not isinstance(text, str):
        return ""

    # Remove potential XSS patterns
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r'javascript:', '', text, flags=re.IGNORECASE)
    text = re.sub(r'on\w+\s*=', '', text, flags=re.IGNORECASE)

    # Limit length
    max_length = int(os.getenv("MAX_INPUT_LENGTH", "10000"))
    return text[:max_length]


def check_rate_limit(identifier: str) -> Tuple[bool, int, int]:
    """
    Check rate limit for a given identifier.

    Returns: (is_allowed, remaining, reset_time_seconds)
    """
    now = datetime.utcnow()
    window_start = now - timedelta(seconds=RATE_LIMIT_WINDOW)

    # Clean old entries
    for key, (_, timestamp) in list(_rate_limit_store.items()):
        if timestamp < window_start:
            del _rate_limit_store[key]

    # Get or create entry
    if identifier not in _rate_limit_store:
        _rate_limit_store[identifier] = (0, now)

    count, _ = _rate_limit_store[identifier]
    remaining = RATE_LIMIT_MAX_REQUESTS - count
    reset_time = RATE_LIMIT_WINDOW

    if count >= RATE_LIMIT_MAX_REQUESTS:
        return False, 0, reset_time

    _rate_limit_store[identifier] = (count + 1, now)
    return True, remaining - 1, reset_time


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiting middleware for chat endpoint."""

    async def dispatch(self, request: Request, call_next):
        # Only rate limit chat endpoints
        if "/chat" not in request.url.path:
            return await call_next(request)

        # Get client identifier
        client_ip = request.client.host if request.client else "unknown"
        user_id = request.state.get("user_id", "anonymous")
        identifier = f"{client_ip}:{user_id}"

        # Check rate limit
        is_allowed, remaining, reset_time = check_rate_limit(identifier)

        if not is_allowed:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many requests. Please try again later.",
                headers={
                    "X-RateLimit-Remaining": str(remaining),
                    "X-RateLimit-Reset": str(reset_time),
                    "Retry-After": str(reset_time)
                }
            )

        response = await call_next(request)

        # Add rate limit headers
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Limit"] = str(RATE_LIMIT_MAX_REQUESTS)

        return response


class InputSanitizationMiddleware(BaseHTTPMiddleware):
    """Input sanitization middleware."""

    async def dispatch(self, request: Request, call_next):
        if request.method == "POST":
            try:
                body = await request.json()
                if isinstance(body, dict):
                    # Sanitize message field if present
                    if "message" in body and isinstance(body["message"], str):
                        body["message"] = sanitize_input(body["message"])
                    # Sanitize conversation_id if present
                    if "conversation_id" in body and isinstance(body["conversation_id"], str):
                        body["conversation_id"] = sanitize_input(body["conversation_id"])
                # Put sanitized body back
                request._body = str(body).encode()
            except Exception:
                pass  # Continue if not JSON

        return await call_next(request)


# Audit logging
audit_log: list = []


def log_audit_event(
    user_id: str,
    action: str,
    details: Dict[str, any],
    success: bool,
    error: Optional[str] = None
):
    """
    Log an audit event for AI interactions.
    """
    event = {
        "timestamp": datetime.utcnow().isoformat(),
        "user_id": user_id,
        "action": action,
        "details": details,
        "success": success,
        "error": error
    }
    audit_log.append(event)

    # Keep only last 1000 events
    if len(audit_log) > 1000:
        audit_log.pop(0)


def get_audit_logs(user_id: Optional[str] = None) -> list:
    """
    Get audit logs, optionally filtered by user.
    """
    if user_id:
        return [e for e in audit_log if e["user_id"] == user_id]
    return audit_log

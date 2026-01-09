import os
from jose import JWTError, jwt
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Optional

# Better Auth JWT Shared Secret (should be in .env)
SECRET_KEY = os.getenv("JWT_SECRET", "change-me-in-production")
ALGORITHM = "HS256"

# Development mode - skip strict JWT validation
DEV_MODE = os.getenv("DEV_MODE", "true").lower() == "true"

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Skip auth for OPTIONS (CORS preflight), docs, health, etc.
        if request.method == "OPTIONS":
            return await call_next(request)
            
        if request.url.path in ["/docs", "/redoc", "/openapi.json", "/api/health"]:
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing or invalid authentication token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        token = auth_header.split(" ")[1]
        
        # Development mode: extract user_id from URL path for chat endpoints
        if DEV_MODE and "/chat" in request.url.path:
            # Extract user_id from path like /api/{user_id}/chat
            path_parts = request.url.path.split("/")
            if len(path_parts) >= 3 and path_parts[1] == "api":
                user_id = path_parts[2]
                request.state.user_id = user_id
                return await call_next(request)
        
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id: str = payload.get("sub")
            if user_id is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

            # Attach user_id to request state for use in endpoints/dependencies
            request.state.user_id = user_id

        except JWTError:
            # In dev mode, use a fallback user_id from the token itself
            if DEV_MODE:
                # Extract user_id from path for chat endpoints
                path_parts = request.url.path.split("/")
                if len(path_parts) >= 3 and path_parts[1] == "api":
                    user_id = path_parts[2]
                    request.state.user_id = user_id
                    return await call_next(request)
            
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        response = await call_next(request)
        return response

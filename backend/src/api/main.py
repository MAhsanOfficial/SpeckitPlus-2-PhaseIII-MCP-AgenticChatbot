from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api import habits, completions, analytics, chat
from src.core.auth import AuthMiddleware

app = FastAPI(title="Habit Tracker API")

# Add JWT Authentication Middleware FIRST
app.add_middleware(AuthMiddleware)

# Configure CORS AFTER Auth - Allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://127.0.0.1:3000", "http://127.0.0.1:3001"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Include Routers
app.include_router(habits.router, prefix="/api")  # Phase II: /api/habits
app.include_router(habits.router_v3, prefix="/api")  # Phase III: /api/{user_id}/habits
app.include_router(completions.router, prefix="/api")  # Phase II: /api/habits/{habit_id}/toggle
app.include_router(completions.router_v3, prefix="/api")  # Phase III: /api/{user_id}/habits/{habit_id}/toggle
app.include_router(completions.completions_router, prefix="/api")  # Phase III: /api/{user_id}/completions
app.include_router(analytics.router, prefix="/api")
app.include_router(chat.router)  # Phase III chatbot - includes /api/{user_id}/chat

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

"""
Phase III Chatbot API Router with INTELLIGENT AI.
AI understands natural language and extracts intent automatically.
"""
import logging
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import get_session
from src.core.deps import get_current_user_id
from src.db.conversation_service import ConversationService
from src.services.habit_service import HabitService
from src.agents.intelligent_chatbot import understand_user_intent, extract_habit_name_fuzzy

from .models import (
    ChatRequest,
    ChatResponse,
    ChatMessageResponse,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/{user_id}/chat", tags=["chatbot"])


def verify_user_isolation(user_id: str, token_user_id: str) -> None:
    """Verify the user_id in URL matches the authenticated user."""
    if user_id != token_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot access another user's conversations"
        )


@router.post("", response_model=ChatResponse)
async def chat_endpoint(
    user_id: str,
    request: Request,
    chat_request: ChatRequest,
    session: AsyncSession = Depends(get_session),
    token_user_id: str = Depends(get_current_user_id)
):
    """Stateless chat endpoint for AI-powered conversation."""
    try:
        verify_user_isolation(user_id, token_user_id)
        print(f"[CHATBOT] User {user_id} verified")

        conversation_service = ConversationService(session)

        if chat_request.conversation_id:
            conv_session = await conversation_service.get_session(
                chat_request.conversation_id, user_id
            )
            if not conv_session:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Conversation not found"
                )
        else:
            conv_session = await conversation_service.create_session(
                user_id=user_id,
                title=chat_request.message[:50] if len(chat_request.message) > 50 else chat_request.message
            )
        
        print(f"[CHATBOT] Processing: {chat_request.message}")
        
        ai_response = await process_chat_message(
            user_id=user_id,
            user_message=chat_request.message,
            session=session
        )
        
        print(f"[CHATBOT] Response: {ai_response.get('content', '')[:100]}...")

        await conversation_service.add_message(
            session_id=conv_session.id,
            role="user",
            content=chat_request.message
        )

        assistant_message = await conversation_service.add_message(
            session_id=conv_session.id,
            role="assistant",
            content=ai_response.get("content", "I'm here to help!")
        )

        return ChatResponse(
            conversation_id=conv_session.id,
            message=ChatMessageResponse(
                id=assistant_message.id,
                role="assistant",
                content=ai_response.get("content", "I'm here to help!"),
                timestamp=assistant_message.timestamp
            ),
            suggestions=ai_response.get("suggestions", [])
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Chat endpoint error: {e}", exc_info=True)
        print(f"[CHATBOT] ERROR: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal error: {str(e)}"
        )



async def process_chat_message(
    user_id: str,
    user_message: str,
    session: AsyncSession
) -> dict:
    """Process chat message using AI to understand intent."""
    
    habit_service = HabitService(session)
    
    try:
        # Get user's habits first (needed for update/delete operations)
        habits = await habit_service.list_habits(user_id)
        
        # Use AI to understand user intent (pass habits for better matching)
        intent_data = await understand_user_intent(user_message, habits)
        
        intent = intent_data.get("intent", "UNCLEAR")
        parameters = intent_data.get("parameters", {})
        confidence = intent_data.get("confidence", 0.0)
        
        print(f"[CHATBOT] Intent: {intent}, Confidence: {confidence}, Params: {parameters}")
        
        # CREATE HABIT
        if intent == "CREATE_HABIT":
            habit_name = parameters.get("name", "").strip()
            habit_description = parameters.get("description", "").strip()
            
            if not habit_name:
                return {
                    "content": "I'd love to help you create a habit! Please tell me the habit name.",
                    "suggestions": ["Create habit Morning Exercise", "Help"]
                }
            
            print(f"[CHATBOT] Creating habit: {habit_name} - {habit_description}")
            
            habit = await habit_service.create_habit(
                user_id, 
                habit_name, 
                habit_description if habit_description else None
            )
            
            print(f"[CHATBOT] Habit created successfully: {habit['id']}")
            
            response_text = f"✅ Great! I've created the habit **'{habit['name']}'** for you."
            if habit_description:
                response_text += f"\n\n📝 Description: {habit_description}"
            response_text += "\n\n🔄 Your dashboard will update automatically!"
            
            return {
                "content": response_text,
                "suggestions": ["Show my habits", "Create another habit"]
            }
        
        # SHOW HABITS
        elif intent == "SHOW_HABITS":
            habits = await habit_service.list_habits(user_id)
            
            if not habits:
                return {
                    "content": "📋 You don't have any habits yet. Let's create your first one!",
                    "suggestions": ["Create habit Morning Exercise", "Help"]
                }
            
            content = "📋 Here are your habits:\n\n"
            for i, habit in enumerate(habits, 1):
                streak = habit.get("streak", 0)
                streak_emoji = "🔥" if streak > 0 else "⭕"
                content += f"{i}. **{habit['name']}** - {streak_emoji} {streak} day streak\n"
                if habit.get("description"):
                    content += f"   _{habit['description']}_\n"
            
            return {
                "content": content,
                "suggestions": ["Create a new habit", "Log a completion"]
            }
        
        # UPDATE HABIT
        elif intent == "UPDATE_HABIT":
            habit_name = parameters.get("habit_name", "").strip()
            new_name = parameters.get("new_name", "").strip()
            new_description = parameters.get("new_description", "").strip()
            
            if not habit_name:
                return {
                    "content": "Which habit would you like to update?",
                    "suggestions": ["Show my habits", "Help"]
                }
            
            habits = await habit_service.list_habits(user_id)
            
            if not habits:
                return {
                    "content": "You don't have any habits to update. Create one first!",
                    "suggestions": ["Create habit Morning Exercise", "Help"]
                }
            
            matching_habit = extract_habit_name_fuzzy(habits, habit_name)
            
            if not matching_habit:
                return {
                    "content": f"I couldn't find a habit matching '{habit_name}'.",
                    "suggestions": [f"Update {h['name']}" for h in habits[:3]]
                }
            
            habit_id = UUID(matching_habit["id"])
            print(f"[CHATBOT] Updating habit: {habit_id}")
            
            updated_habit = await habit_service.update_habit(
                habit_id, 
                user_id, 
                name=new_name if new_name else None,
                description=new_description if new_description else None
            )
            
            if updated_habit:
                response_text = f"✅ Updated **'{matching_habit['name']}'**!"
                if new_name:
                    response_text += f" New name: **{new_name}**"
                if new_description:
                    response_text += f"\n📝 New description: {new_description}"
                response_text += "\n\n🔄 Dashboard updated!"
                
                return {
                    "content": response_text,
                    "suggestions": ["Show my habits", "Create another habit"]
                }
            else:
                return {
                    "content": "❌ Failed to update. Please try again.",
                    "suggestions": ["Show my habits", "Help"]
                }
        
        # DELETE HABIT
        elif intent == "DELETE_HABIT":
            habit_name = parameters.get("habit_name", "").strip()
            
            if not habit_name:
                return {
                    "content": "Which habit would you like to delete?",
                    "suggestions": ["Show my habits", "Help"]
                }
            
            habits = await habit_service.list_habits(user_id)
            
            if not habits:
                return {
                    "content": "You don't have any habits to delete.",
                    "suggestions": ["Create habit Morning Exercise", "Help"]
                }
            
            matching_habit = extract_habit_name_fuzzy(habits, habit_name)
            
            if not matching_habit:
                return {
                    "content": f"I couldn't find a habit matching '{habit_name}'.",
                    "suggestions": [f"Delete {h['name']}" for h in habits[:3]]
                }
            
            habit_id = UUID(matching_habit["id"])
            print(f"[CHATBOT] Deleting habit: {habit_id}")
            
            success = await habit_service.delete_habit(habit_id, user_id)
            
            if success:
                return {
                    "content": f"✅ Deleted **'{matching_habit['name']}'**!\n\n🔄 Dashboard updated!",
                    "suggestions": ["Show my habits", "Create a new habit"]
                }
            else:
                return {
                    "content": "❌ Failed to delete. Please try again.",
                    "suggestions": ["Show my habits", "Help"]
                }
        
        # DELETE ALL HABITS
        elif intent == "DELETE_ALL":
            habits = await habit_service.list_habits(user_id)
            
            if not habits:
                return {
                    "content": "You don't have any habits to delete.",
                    "suggestions": ["Create habit Morning Exercise", "Help"]
                }
            
            deleted_count = 0
            for habit in habits:
                habit_id = UUID(habit["id"])
                success = await habit_service.delete_habit(habit_id, user_id)
                if success:
                    deleted_count += 1
            
            return {
                "content": f"✅ Deleted all {deleted_count} habits!\n\n🔄 Dashboard cleared!",
                "suggestions": ["Create a new habit", "Help"]
            }
        
        # SELECT/CHECK HABIT
        elif intent == "SELECT_HABIT":
            habit_name = parameters.get("habit_name", "").strip()
            
            habits = await habit_service.list_habits(user_id)
            
            if not habits:
                return {
                    "content": "You don't have any habits yet!",
                    "suggestions": ["Create habit Morning Exercise", "Help"]
                }
            
            if habit_name:
                matching_habit = extract_habit_name_fuzzy(habits, habit_name)
                if matching_habit:
                    return {
                        "content": f"✅ Selected **'{matching_habit['name']}'**!\n\n📝 Description: {matching_habit.get('description', 'No description')}\n🔥 Streak: {matching_habit.get('streak', 0)} days\n\n💡 Click on the habit in dashboard to see more options.",
                        "suggestions": [f"Update {matching_habit['name']}", f"Delete {matching_habit['name']}", f"Complete {matching_habit['name']}"],
                        "selected_habit_id": matching_habit["id"]
                    }
            
            content = "Which habit would you like to select?\n\n"
            for i, h in enumerate(habits, 1):
                content += f"{i}. {h['name']}\n"
            return {
                "content": content,
                "suggestions": [f"Select {h['name']}" for h in habits[:3]]
            }
        
        # LOG COMPLETION
        elif intent == "LOG_COMPLETION":
            habit_name = parameters.get("habit_name", "").strip()
            habits = await habit_service.list_habits(user_id)
            
            if not habits:
                return {
                    "content": "You don't have any habits yet!",
                    "suggestions": ["Create habit Morning Exercise", "Help"]
                }
            
            if habit_name:
                matching_habit = extract_habit_name_fuzzy(habits, habit_name)
                if matching_habit:
                    habit_id = UUID(matching_habit["id"])
                    await habit_service.log_completion(habit_id, user_id)
                    return {
                        "content": f"🎉 Logged completion for **{matching_habit['name']}**!",
                        "suggestions": ["Show my habits", "Check streak"]
                    }
            
            if len(habits) == 1:
                habit_id = UUID(habits[0]["id"])
                await habit_service.log_completion(habit_id, user_id)
                return {
                    "content": f"🎉 Logged completion for **{habits[0]['name']}**!",
                    "suggestions": ["Show my habits", "Check streak"]
                }
            
            content = "Which habit did you complete?\n\n"
            for i, h in enumerate(habits, 1):
                content += f"{i}. {h['name']}\n"
            return {
                "content": content,
                "suggestions": [f"Completed {h['name']}" for h in habits[:3]]
            }
        
        # CHECK STREAK
        elif intent == "CHECK_STREAK":
            habits = await habit_service.list_habits(user_id)
            
            if not habits:
                return {
                    "content": "No habits tracked yet!",
                    "suggestions": ["Create habit Morning Exercise", "Help"]
                }
            
            content = "🔥 Your Streaks:\n\n"
            for habit in habits:
                streak = habit.get("streak", 0)
                emoji = "🔥" if streak > 0 else "⭕"
                content += f"• **{habit['name']}**: {emoji} {streak} days\n"
            
            return {
                "content": content,
                "suggestions": ["Log a completion", "Show my habits"]
            }
        
        # HELP
        elif intent == "HELP":
            return {
                "content": """🤖 I'm your Habit Tracking Assistant!

Just talk to me naturally:
• "Create habit cricket, I do it every Sunday"
• "Show my habits"
• "Update cricket description to morning practice"
• "Delete cricket habit"
• "I completed workout"
• "What's my streak?"

💡 All changes sync to your dashboard automatically!""",
                "suggestions": ["Show my habits", "Create a new habit"]
            }
        
        # GREETING
        elif intent == "GREETING":
            return {
                "content": "Hello! 👋 I'm your Habit Assistant. What would you like to do?",
                "suggestions": ["Show my habits", "Create a new habit", "Help"]
            }
        
        # UNCLEAR
        else:
            return {
                "content": "I didn't quite understand. Try: 'create habit', 'show habits', 'delete habit', or 'help'",
                "suggestions": ["Show my habits", "Create a new habit", "Help"]
            }
            
    except Exception as e:
        logger.error(f"Error processing message: {e}", exc_info=True)
        print(f"[CHATBOT] ERROR: {e}")
        return {
            "content": "Something went wrong. Please try again.",
            "suggestions": ["Show my habits", "Help"]
        }

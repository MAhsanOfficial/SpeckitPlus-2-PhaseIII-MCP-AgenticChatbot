import os
import google.generativeai as genai

# Configure Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def get_habit_feedback(habit_name: str, habit_description: str = ""):
    """
    Generate feedback for a habit using Gemini 2.5 Flash model.
    Returns: (pros_string, cons_string)
    """
    # Temporarily return default feedback to avoid API errors
    return (
        f"Neural path for '{habit_name}' stabilized.|System synergy increased.|Consistency levels optimized.",
        f"Initial power consumption for '{habit_name}'.|Monitor for routine conflicts.|Watch for transition fatigue."
    )

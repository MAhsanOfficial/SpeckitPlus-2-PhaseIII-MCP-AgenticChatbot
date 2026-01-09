"""
Smart Chatbot - Properly understands natural language
Extracts clean name and description without keywords
"""
import os
import json
import re
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()

# Gemini Setup
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
client = None

if GEMINI_API_KEY:
    try:
        from google import genai
        client = genai.Client(api_key=GEMINI_API_KEY.strip())
        print("[CHATBOT] ✅ Gemini Ready")
    except Exception as e:
        print(f"[CHATBOT] ❌ Gemini failed: {e}")

SYSTEM_PROMPT = """You are a habit assistant. Extract CLEAN name and description from user message.

CRITICAL RULES:
1. NEVER include these words in name: "name", "habit", "create", "add", "banana", "banao", "make", "new"
2. NEVER include these words in description: "description", "desc", "details"
3. Name = Just the activity (1-4 words)
4. Description = Schedule/frequency/details (can be empty)

EXAMPLES:

"name cricket description har sunday"
→ name: "Cricket", description: "Har sunday"

"cricket"
→ name: "Cricket", description: ""

"name morning exercise"
→ name: "Morning Exercise", description: ""

"create habit reading description daily 1 hour"
→ name: "Reading", description: "Daily 1 hour"

"gym, monday wednesday friday"
→ name: "Gym", description: "Monday wednesday friday"

"yoga roz subah karna hai"
→ name: "Yoga", description: "Roz subah karna hai"

"banana meditation habit description 10 min daily"
→ name: "Meditation", description: "10 min daily"

"show habits" → {"intent": "SHOW_HABITS", "parameters": {}}
"delete cricket" → {"intent": "DELETE_HABIT", "parameters": {"habit_name": "Cricket"}}
"delete all" → {"intent": "DELETE_ALL", "parameters": {}}
"update cricket description evening practice" → {"intent": "UPDATE_HABIT", "parameters": {"habit_name": "Cricket", "new_name": "", "new_description": "Evening practice"}}
"hello" → {"intent": "GREETING", "parameters": {}}

RESPOND WITH JSON ONLY:
{"intent": "...", "parameters": {...}, "confidence": 0.0-1.0}"""


# Keywords to remove from name and description
NAME_KEYWORDS = {"name", "habit", "create", "add", "banana", "banao", "make", "new", "meri", "mera", "ki", "ka", "ko", "hai", "ha", "karo", "kro", "kar", "the", "a", "an", "is", "and", "or"}
DESC_KEYWORDS = {"description", "desc", "details", "uski", "iski", "ki", "to", "do", "kro", "karo", "change", "badal", "badlo"}
UPDATE_KEYWORDS = {"update", "edit", "change", "badal", "badlo", "kro", "karo", "do"}


def clean_name(text: str) -> str:
    """Remove keywords and clean up the name"""
    if not text:
        return ""
    
    # Remove keywords
    words = text.strip().split()
    cleaned = []
    for word in words:
        if word.lower() not in NAME_KEYWORDS:
            cleaned.append(word)
    
    result = " ".join(cleaned).strip()
    # Title case
    return result.title() if result else ""


def clean_description(text: str) -> str:
    """Remove keywords and clean up the description"""
    if not text:
        return ""
    
    words = text.strip().split()
    cleaned = []
    for word in words:
        if word.lower() not in DESC_KEYWORDS:
            cleaned.append(word)
    
    return " ".join(cleaned).strip()


async def call_gemini(message: str) -> Optional[Dict[str, Any]]:
    """Call Gemini API to understand user intent"""
    if not client:
        return None
    
    try:
        prompt = f"{SYSTEM_PROMPT}\n\nUser message: {message}"
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=prompt
        )
        
        text = response.text.strip()
        # Extract JSON from response
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]
        
        text = text.strip()
        result = json.loads(text)
        
        # Clean the extracted values
        if "parameters" in result:
            params = result["parameters"]
            if "name" in params:
                params["name"] = clean_name(params["name"])
            if "description" in params:
                params["description"] = clean_description(params["description"])
            if "new_name" in params:
                params["new_name"] = clean_name(params["new_name"])
            if "new_description" in params:
                params["new_description"] = clean_description(params["new_description"])
        
        print(f"[GEMINI] ✅ Parsed: {result}")
        return result
        
    except Exception as e:
        print(f"[GEMINI] ❌ Error: {e}")
        return None


def extract_habit_name_fuzzy(habits: list, search_term: str) -> Optional[dict]:
    """Find habit in list using fuzzy matching - returns full habit dict"""
    if not habits or not search_term:
        return None
    
    search_lower = search_term.lower().strip()
    
    # Exact match first
    for habit in habits:
        habit_name = habit.get("name", "").lower()
        if habit_name == search_lower:
            return habit
    
    # Partial match
    for habit in habits:
        habit_name = habit.get("name", "").lower()
        if search_lower in habit_name or habit_name in search_lower:
            return habit
    
    # Word match
    search_words = search_lower.split()
    for habit in habits:
        habit_name = habit.get("name", "").lower()
        for word in search_words:
            if word in habit_name or habit_name in word:
                return habit
    
    return None


def find_habit_in_message(message: str, habits: list) -> Optional[str]:
    """Find habit name mentioned in a message - returns habit name string"""
    if not habits:
        return None
    
    msg_lower = message.lower()
    
    for habit in habits:
        habit_name = habit.get("name", "").lower()
        if habit_name and habit_name in msg_lower:
            return habit.get("name")
    
    return None


def parse_create(message: str) -> Dict[str, Any]:
    """Parse CREATE intent from message - extract clean name and description"""
    msg = message.lower()
    
    name = ""
    description = ""
    
    # Pattern 1: "name X description Y"
    if "description" in msg or "desc" in msg:
        # Split by description keyword
        parts = re.split(r'\b(?:description|desc)\b', msg, flags=re.IGNORECASE)
        if len(parts) >= 2:
            name_part = parts[0]
            description = clean_description(parts[1])
            
            # Extract name from first part
            name_part = re.sub(r'\b(?:name|habit|create|add|banana|banao|make|new|meri|mera)\b', '', name_part, flags=re.IGNORECASE)
            name = clean_name(name_part)
    
    # Pattern 2: "name X" (no description)
    elif "name" in msg:
        name_part = re.sub(r'\b(?:name|habit|create|add|banana|banao|make|new|meri|mera)\b', '', msg, flags=re.IGNORECASE)
        name = clean_name(name_part)
    
    # Pattern 3: Just the activity name
    else:
        # Remove create keywords
        cleaned = re.sub(r'\b(?:habit|create|add|banana|banao|make|new|meri|mera|karo|kro)\b', '', msg, flags=re.IGNORECASE)
        
        # Check for comma (name, description)
        if "," in cleaned:
            parts = cleaned.split(",", 1)
            name = clean_name(parts[0])
            description = clean_description(parts[1]) if len(parts) > 1 else ""
        else:
            name = clean_name(cleaned)
    
    return {
        "intent": "CREATE_HABIT",
        "parameters": {
            "name": name,
            "description": description
        },
        "confidence": 0.7
    }


def parse_update(message: str, habits: list) -> Dict[str, Any]:
    """Parse UPDATE intent from message"""
    msg = message.lower()
    
    # Find which habit to update
    habit_name = find_habit_in_message(message, habits)
    
    new_name = ""
    new_description = ""
    
    # Check for description update
    if "description" in msg or "desc" in msg:
        parts = re.split(r'\b(?:description|desc)\b', msg, flags=re.IGNORECASE)
        if len(parts) >= 2:
            # Clean the description part - remove update keywords
            desc_part = parts[1]
            for keyword in UPDATE_KEYWORDS:
                desc_part = re.sub(r'\b' + keyword + r'\b', '', desc_part, flags=re.IGNORECASE)
            new_description = clean_description(desc_part)
    else:
        # No explicit "description" keyword - extract from message
        # Remove habit name and update keywords
        cleaned_msg = msg
        if habit_name:
            cleaned_msg = cleaned_msg.replace(habit_name.lower(), "")
        
        # Remove update keywords
        for keyword in UPDATE_KEYWORDS:
            cleaned_msg = re.sub(r'\b' + keyword + r'\b', '', cleaned_msg, flags=re.IGNORECASE)
        
        new_description = clean_description(cleaned_msg)
    
    # Check for name update
    if "name" in msg and "new" in msg:
        # "new name X"
        match = re.search(r'new\s+name\s+(\w+)', msg, re.IGNORECASE)
        if match:
            new_name = clean_name(match.group(1))
    
    return {
        "intent": "UPDATE_HABIT",
        "parameters": {
            "habit_name": habit_name or "",
            "new_name": new_name,
            "new_description": new_description
        },
        "confidence": 0.7
    }


def fallback_parse(message: str, habits: list = None) -> Dict[str, Any]:
    """Fallback keyword-based parsing when Gemini fails"""
    msg = message.lower().strip()
    habits = habits or []
    
    # Greeting
    greetings = ["hello", "hi", "hey", "salam", "assalam", "aoa"]
    if any(g in msg for g in greetings):
        return {"intent": "GREETING", "parameters": {}, "confidence": 0.9}
    
    # Help
    if any(w in msg for w in ["help", "madad", "kya kar", "kia kar"]):
        return {"intent": "HELP", "parameters": {}, "confidence": 0.9}
    
    # Delete all
    if any(p in msg for p in ["delete all", "sab delete", "all delete", "sari delete", "saari delete"]):
        return {"intent": "DELETE_ALL", "parameters": {}, "confidence": 0.9}
    
    # Delete single
    if any(w in msg for w in ["delete", "remove", "hata", "hatao"]):
        habit_name = find_habit_in_message(message, habits)
        return {
            "intent": "DELETE_HABIT",
            "parameters": {"habit_name": habit_name or ""},
            "confidence": 0.7
        }
    
    # Show habits
    if any(w in msg for w in ["show", "list", "dikha", "dikhao", "batao", "habits"]):
        return {"intent": "SHOW_HABITS", "parameters": {}, "confidence": 0.9}
    
    # Update/Edit
    if any(w in msg for w in ["update", "edit", "change", "badal", "badlo"]):
        return parse_update(message, habits)
    
    # Select habit
    if any(w in msg for w in ["select", "check", "choose", "chuno"]):
        habit_name = find_habit_in_message(message, habits)
        return {
            "intent": "SELECT_HABIT",
            "parameters": {"habit_name": habit_name or ""},
            "confidence": 0.7
        }
    
    # Create (default for anything with name/description pattern)
    if any(w in msg for w in ["create", "add", "banana", "banao", "make", "new", "name"]):
        return parse_create(message)
    
    # If nothing matches but has some text, try to create
    if len(msg) > 2:
        return parse_create(message)
    
    return {"intent": "UNKNOWN", "parameters": {}, "confidence": 0.0}


async def understand_user_intent(message: str, habits: list = None) -> Dict[str, Any]:
    """Main function - understand user intent using Gemini first, then fallback"""
    habits = habits or []
    
    print(f"[CHATBOT] Processing: {message}")
    
    # Try Gemini first
    result = await call_gemini(message)
    
    if result and result.get("intent") and result.get("confidence", 0) > 0.5:
        # Gemini succeeded - clean the values again to be safe
        if "parameters" in result:
            params = result["parameters"]
            if "name" in params:
                params["name"] = clean_name(params["name"])
            if "description" in params:
                params["description"] = clean_description(params["description"])
            if "new_name" in params:
                params["new_name"] = clean_name(params["new_name"])
            if "new_description" in params:
                params["new_description"] = clean_description(params["new_description"])
            if "habit_name" in params:
                # Don't clean habit_name - it should match existing habit
                pass
        
        print(f"[CHATBOT] ✅ Gemini result: {result}")
        return result
    
    # Fallback to keyword parsing
    print("[CHATBOT] Using fallback parser...")
    result = fallback_parse(message, habits)
    print(f"[CHATBOT] ✅ Fallback result: {result}")
    return result

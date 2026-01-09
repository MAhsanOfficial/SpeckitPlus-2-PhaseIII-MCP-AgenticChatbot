# Habit Tracker - Complete Setup & Usage Guide

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL database
- Gemini API key

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn src.api.main:app --reload --port 8000
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Environment Variables

**backend/.env**:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/habit_tracker
JWT_SECRET=your-secret-key
GEMINI_API_KEY=your-gemini-api-key
```

**frontend/.env**:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 🤖 Chatbot Features

### Natural Language Understanding
The chatbot understands both English and Roman Urdu:

### CREATE Habits
```
✅ "name cricket description har sunday"
✅ "create habit reading description daily 1 hour"
✅ "banana meditation habit"
✅ "gym, monday wednesday friday"
```

**Result**: Creates habit with clean name and description (no keywords like "name", "habit", "create", "banana")

### UPDATE Habits
```
✅ "cricket description change kro evening practice"
✅ "update cricket description to morning"
✅ "edit reading description daily 1 hour"
✅ "cricket ki description badal do evening"
```

**Result**: Updates habit description (removes keywords like "change", "kro", "badal", "to", "do")

### DELETE Habits
```
✅ "delete cricket"
✅ "cricket ko hata do"
✅ "remove reading habit"
✅ "delete all habits"
```

**Result**: Deletes specified habit or all habits

### OTHER Commands
```
✅ "show my habits" - List all habits
✅ "hello" - Greeting
✅ "help" - Show help
```

---

## 📊 Dashboard Features

### Manual Operations (No Refresh Needed!)

1. **Create Habit**:
   - Click "NEW HABIT" button
   - Fill name and description
   - Submit
   - ✅ Appears instantly in dashboard
   - ✅ Persists after page refresh

2. **Update Habit**:
   - Click on habit card
   - Click edit button
   - Change name/description
   - Submit
   - ✅ Updates instantly
   - ✅ Persists after page refresh

3. **Delete Habit**:
   - Click on habit card
   - Click delete button
   - ✅ Removes instantly
   - ✅ Gone after page refresh

4. **Toggle Complete**:
   - Click checkbox on habit
   - ✅ Marks complete/incomplete instantly
   - ✅ Updates streak

### Auto-Refresh
- Dashboard auto-refreshes every 2 seconds
- Syncs with chatbot operations automatically
- No manual refresh needed

---

## 🔧 Technical Details

### Backend Architecture
- **FastAPI** - REST API
- **SQLModel** - ORM
- **PostgreSQL** - Database
- **Gemini AI** - Natural language processing
- **JWT** - Authentication

### Frontend Architecture
- **Next.js 14** - React framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Framer Motion** - Animations
- **Context API** - State management

### Key Components

**Backend**:
- `src/agents/intelligent_chatbot.py` - Natural language processing
- `src/api/chat/router.py` - Chatbot API endpoints
- `src/services/habit_service.py` - Habit CRUD operations
- `src/api/habits.py` - Habit API endpoints

**Frontend**:
- `src/context/HabitContext.tsx` - Habit state management
- `src/components/chat/ChatContainer.tsx` - Chatbot UI
- `src/app/dashboard/page.tsx` - Dashboard UI

---

## 🎯 How It Works

### Natural Language Processing

1. **Gemini AI (Primary)**:
   - Tries to understand intent using Gemini LLM
   - Extracts clean name and description
   - Removes keywords automatically

2. **Fallback Parser (Secondary)**:
   - If Gemini fails (quota exceeded), uses keyword-based parsing
   - Pattern matching for intents
   - Fuzzy matching for habit names

### Optimistic Updates

1. **Manual Operations**:
   - Update UI immediately (optimistic)
   - Send request to server (background)
   - Refresh after 1 second (confirm)
   - Revert only if server fails

2. **Chatbot Operations**:
   - Server processes request
   - Dashboard polls every 2 seconds
   - Updates appear automatically

---

## 🐛 Troubleshooting

### Gemini Quota Exceeded
- Fallback parser automatically activates
- All features still work
- Wait for quota to reset (daily limit)

### Dashboard Not Updating
- Check if backend is running (port 8000)
- Check browser console for errors
- Verify JWT token is valid

### Chatbot Not Responding
- Check backend logs
- Verify Gemini API key is set
- Check network requests in browser

---

## 📝 API Endpoints

### Habits
- `GET /api/{user_id}/habits/` - List habits
- `POST /api/{user_id}/habits/` - Create habit
- `PUT /api/{user_id}/habits/{habit_id}` - Update habit
- `DELETE /api/{user_id}/habits/{habit_id}` - Delete habit

### Chatbot
- `POST /api/{user_id}/chat` - Send message to chatbot

### Completions
- `POST /api/{user_id}/habits/{habit_id}/toggle` - Toggle completion
- `GET /api/{user_id}/completions/?date={date}` - Get completions

---

## ✅ Status: Production Ready

All features are working:
- ✅ Natural language chatbot (English + Roman Urdu)
- ✅ Create, Update, Delete habits via chatbot
- ✅ Manual CRUD operations on dashboard
- ✅ Optimistic updates (instant UI)
- ✅ Auto-refresh (no manual refresh needed)
- ✅ Keyword cleaning (clean names/descriptions)
- ✅ Fallback parser (works without Gemini)
- ✅ Persistent storage (PostgreSQL)

---

## 🎉 Ready to Use!

Start both servers and open http://localhost:3001 in your browser. Happy habit tracking! 🚀

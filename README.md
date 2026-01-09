# Habit Tracker & Goal Management - Phase II

Welcome to Phase II of the Habit Tracker. This application features a secure FastAPI backend and a modern, animated Next.js frontend, built using Spec-Driven Development (SDD).

## Features
- **Daily habit creation**: Define your goals with names and descriptions.
- **Completion toggle**: Mark habits as done with smooth animations.
- **Automatic streaks**: Recursive logic calculates your consistency automatically.
- **Visual Analytics**: Weekly and monthly reports to track your progress.
- **Secure by design**: Mandatory JWT verification and strict user data isolation.

## Tech Stack
- **Frontend**: Next.js 14+, Tailwind CSS, Framer Motion, TypeScript
- **Backend**: FastAPI, SQLModel, PostgreSQL (Neon), JWT
- **Design**: Yellow & Orange Gradient Theme

---

## 🚀 How to Run the Project

### 1. Prerequisites
- Python 3.12+
- Node.js 18+
- PostgreSQL database (e.g., Neon.tech)

### 2. Backend Setup (FastAPI)
Navigate to the `backend` directory:
```bash
cd backend
```

Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Create a `.env` file in the `backend` directory:
```env
DATABASE_URL=postgresql+asyncpg://user:password@host/dbname
JWT_SECRET=your-secret-key-matches-frontend
```

Start the backend server:
```bash
uvicorn src.api.main:app --reload
```
The API will be available at `http://localhost:8000`. You can view the docs at `/docs`.

---

### 3. Frontend Setup (Next.js)
Navigate to the `frontend` directory:
```bash
cd ../frontend
```

Install dependencies:
```bash
npm install
```

Create a `.env.local` file in the `frontend` directory:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
# Better Auth credentials (if configured)
```

Run the development server:
```bash
npm run dev
```
Open `http://localhost:3000` in your browser.

---

## 🛠 Project Structure
- `backend/src/api`: FastAPI routes (Habits, Completions, Analytics).
- `backend/src/models`: Database schemas using SQLModel.
- `backend/src/services`: Core logic like streak calculation.
- `frontend/src/components`: UI components with Framer Motion.
- `frontend/src/services`: API client for communicating with the backend.
- `specs/001-habit-tracker`: Design artifacts (Spec, Plan, Tasks).

## 🛡 Security Note
All endpoints are secured via JWT. Make sure to include the `Authorization: Bearer <token>` header in your requests. The backend enforces strict user isolation, meaning you can only see and modify your own data.



🤖 Generated with [Claude Code](https://claude.com/claude-code)

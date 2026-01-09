# Tasks: Habit Tracker Core Implementation

**Input**: Design documents from `/specs/001-habit-tracker/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md

## Layer: Backend (Python/FastAPI/SQLModel)

| Task ID | Task Name | Description | Related Specs |
|---------|-----------|-------------|---------------|
| T-B-001 | JWT Middleware | Implement FastAPI middleware to verify Better Auth JWTs in `Bearer <token>` and reject invalid requests with 401. | FR-006, CON-III |
| T-B-002 | SQLModel Schemas | Create `Habit` and `Completion` models with primary/foreign keys and metadata tracking. | FR-001, FR-002, DM-1, DM-2 |
| T-B-003 | User-Scoped Queries | Define a CRUD service layer that automatically appends `user_id` filters to all SQLModel sessions. | FR-007, CON-III |
| T-B-004 | Habit CRUD Endpoints | Implement `GET /habits`, `POST /habits`, `PUT /habits/{id}`, and `DELETE /habits/{id}` for authenticated users. | FR-001, API-1 |
| T-B-005 | Toggle Completion | Implement `POST /habits/{id}/toggle` to create or update completion status for a specific date. | FR-002, API-3 |
| T-B-006 | Streak Calculation Service | Implement recursive logic to calculate current and longest streaks based on daily history. | FR-003, RES-2, US-2 |
| T-B-007 | Weekly/Monthly Aggregations | Implement `GET /analytics/weekly` and `GET /analytics/monthly` using SQL `GROUP BY` and date truncating functions. | FR-004, FR-005, API-4, API-5 |
| T-B-008 | Security & Isolation Tests | Write integration tests verifying that User A cannot access or modify User B's habits or completions. | SC-004, FR-007 |

## Layer: Frontend (Next.js/TS/Tailwind/Motion)

| Task ID | Task Name | Description | Related Specs |
|---------|-----------|-------------|---------------|
| T-F-001 | API Client Integration | Setup Axios or Fetch client with request interceptors to include Bearer tokens from Better Auth context. | FR-006, CON-III |
| T-F-002 | Yellow/Orange Theme Setup | Configure Tailwind colors and global CSS for the mandatory constitutional palette. | UI-001, CON-V |
| T-F-003 | Dashboard View | Build the main user dashboard with animated list entries for current habits. | US-1, UI-004 |
| T-F-004 | Habit Item Component | Create a reusable card component with Framer Motion hover/active states. | UI-004, CON-V |
| T-F-005 | Animated Toggle | Implement the completion toggle with Framer Motion "check" and scale animations. | UI-002, US-1 |
| T-F-006 | Habit Creation Flow | Build the form/modal for adding new habits with validation feedback. | FR-001, SC-001 |
| T-F-007 | Reports Page | Implement the `/reports` route with layout for analytics visualization. | US-3, FR-004 |
| T-F-008 | Animated Analytics Charts | Create visual reports using Framer Motion for data point/bar entry transitions. | UI-003, SC-003 |

## Layer: Database (Neon/SQL)

| Task ID | Task Name | Description | Related Specs |
|---------|-----------|-------------|---------------|
| T-D-001 | Migrations Setup | Initialize Alembic or SQLModel migrations logic to manage schema evolution on Neon. | DM-1, DM-2 |
| T-D-002 | Index Optimization | Create composite indexes on `(habit_id, date)` and `(user_id, created_at)` for aggregation performance. | FR-007, DM-2 |

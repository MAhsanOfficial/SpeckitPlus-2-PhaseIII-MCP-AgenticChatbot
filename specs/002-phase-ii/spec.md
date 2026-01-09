# Feature Specification: Habit Tracker Phase II

**Feature Branch**: `002-phase-ii`
**Created**: 2025-12-30
**Status**: Draft
**Input**: User description: "Generate complete Spec-Kit Plus specifications for Phase II including Habit CRUD, Daily completion, Streak logic, Weekly/Monthly reports, User auth, API, Database, UI/UX, and Motion."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Secure Habit Management (Priority: P1)
As an authenticated user, I want to manage my personal habits (create, read, update, delete) securely so that I can organize my personal goals without others seeing them.

**Why this priority**: Core functionality required before tracking and analytics can occur.

**Independent Test**: Authenticate as User A, create a habit, verify User B cannot see or modify User A's habit via API or UI.

**Acceptance Scenarios**:
1. **Given** a valid JWT for User A, **When** they request `POST /api/habits`, **Then** a habit is created and associated with User A's ID.
2. **Given** a valid JWT for User B, **When** they request `GET /api/habits/{UserA_HabitID}`, **Then** the system returns a 403 or 404 error.

---

### User Story 2 - Daily Progress and Streak Calculation (Priority: P1)
As a user, I want to toggle my habit completion daily and see an accurate streak count so that I stay motivated through consistency.

**Why this priority**: Primary engagement mechanic for the product.

**Independent Test**: Toggle a habit for 3 consecutive days and verify the streak count is exactly 3. Skip a day and verify the streak resets to 0 or 1 upon the next completion.

**Acceptance Scenarios**:
1. **Given** a habit completed yesterday, **When** user toggles "Complete" today, **Then** streak increments and visual feedback reflects the new streak.
2. **Given** a habit missed yesterday, **When** user toggles "Complete" today, **Then** streak resets to 1.

---

### User Story 3 - Visual Analytics Reports (Priority: P2)
As a user, I want to see weekly and monthly summaries of my progress in an animated dashboard so that I can analyze my long-term behavioral trends.

**Why this priority**: Advanced insight feature that builds on top of completion data.

**Independent Test**: View the reports page and confirm that the bar/line charts accurately reflect the percentage of completed tasks for the selected period.

**Acceptance Scenarios**:
1. **Given** 5 completed habits out of 7 for the week, **When** navigating to the Weekly Report, **Then** the chart shows a 71% completion rate with animated entry transitions.

---

## Requirements *(mandatory)*

### Functional Requirements
- **FR-001**: System MUST allow users to Register/Login via Better Auth and receive a JWT.
- **FR-002**: System MUST require a valid JWT `Bearer` token for all API endpoints under `/api/`.
- **FR-003**: System MUST verify that the `sub` claim in the JWT matches the `user_id` of the requested resource.
- **FR-004**: System MUST return 401 for missing/invalid tokens and 403 for unauthorized access to others' data.
- **FR-005**: System MUST support CRUD operations (Create, Read, Update, Delete) for Habits.
- **FR-006**: System MUST persist Daily Completion history as discrete records.
- **FR-007**: System MUST automatically calculate Current Streak and Longest Streak for each habit.
- **FR-008**: System MUST generate aggregations for Weekly (7 days) and Monthly (calendar month) completion percentages.

### Database Requirements
- **DB-001**: Schema MUST be compatible with SQLModel and Neon Serverless PostgreSQL.
- **DB-002**: `habits` table must include: `id` (UUID), `user_id` (UUID, Index), `name` (String), `description` (Text), `created_at` (Timestamp).
- **DB-003**: `completions` table must include: `id` (UUID), `habit_id` (UUID, Index), `date` (Date, Index), `status` (Boolean).
- **DB-004**: Database queries for reports MUST use optimized indexing on `(habit_id, date)`.

### Authentication Requirements
- **AUTH-001**: Better Auth MUST issue JWTs with a configurable expiration (e.g., 24h).
- **AUTH-002**: Backend and Frontend MUST share a `JWT_SECRET` via environment variables.
- **AUTH-003**: Backend MUST implement a middleware to verify JWT signatures and extract user context.

### UI & Motion Requirements *(mandatory)*
- **UI-001**: Application MUST use Next.js 16+ App Router and Tailwind CSS.
- **UI-002**: Theme MUST utilize a "Yellow & Orange" modern gradient system.
- **UI-003**: Transitions for habit toggles and list item entries MUST use Framer Motion.
- **UI-004**: Progress charts MUST have animated entry and update behaviors.
- **UI-005**: Layout MUST be responsive for Mobile and Desktop views.

## Key Entities
- **User**: Managed by Better Auth; primary owner of habits.
- **Habit**: The goal definition (e.g., "Drink Water").
- **Completion**: A junction entity linking a Habit to a specific Date with a True/False status.
- **Analytics**: A computed object containing streak counts and period-based percentages.

## Success Criteria *(mandatory)*
- **SC-001**: 100% of API endpoints are secured by JWT verification.
- **SC-002**: Unauthorized users are blocked with 401/403 status 100% of the time.
- **SC-003**: Streak calculation is accurate within the current session and persistent across logins.
- **SC-004**: UI rendering of 10+ habits reflects animated transitions at 60fps.
- **SC-005**: Weekly/Monthly reports match the raw database completion count with 0% margin of error.

## Assumptions
- "Next day" for streak calculation is determined by the server's UTC time unless user timezone is provided.
- Better Auth handles the actual registration/login flow, while our app consumes the issued tokens.

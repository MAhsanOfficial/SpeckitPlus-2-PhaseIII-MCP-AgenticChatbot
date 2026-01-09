# Feature Specification: Habit Tracker Core

**Feature Branch**: `001-habit-tracker`
**Created**: 2025-12-30
**Status**: Draft
**Input**: User description: "Using the Constitution, generate complete specifications for the Habit Tracker app. Features: Daily habit creation, Completion toggle, Automatic streak tracking, Weekly & monthly reports, User-specific dashboards."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Create and Track Daily Habits (Priority: P1)

As a user, I want to create daily habits and toggle their completion status so that I can monitor my daily progress.

**Why this priority**: Core functionality of the application; provides immediate value and is the foundation for all other features.

**Independent Test**: Can be fully tested by creating a habit, viewing it on the dashboard, and clicking the toggle to mark it as complete.

**Acceptance Scenarios**:

1. **Given** an authenticated user on the dashboard, **When** they submit a new habit name and frequency, **Then** the habit is saved and appears in their daily list.
2. **Given** an existing incomplete habit, **When** the user toggles the completion checkbox, **Then** the habit status updates to "Complete" and the visual state changes.

---

### User Story 2 - Automated Streak Monitoring (Priority: P2)

As a user, I want the system to calculate my current streak automatically so that I stay motivated to maintain consistency.

**Why this priority**: Motivation is a key user goal; requires functioning daily tracking to calculate.

**Independent Test**: Can be tested by marking a habit complete for multiple consecutive days and verifying the incrementing streak counter.

**Acceptance Scenarios**:

1. **Given** a habit completed yesterday, **When** the user completes it today, **Then** the streak count increments by 1.
2. **Given** a habit NOT completed yesterday, **When** the user completes it today, **Then** the streak count resets to 1.

---

### User Story 3 - Visual Progress Reports (Priority: P3)

As a user, I want to view weekly and monthly reports of my completions so that I can see long-term trends.

**Why this priority**: Provides insight into long-term behavior change; dependent on historical data.

**Independent Test**: Can be tested by navigating to the "Reports" view and verifying the data visualization matches the historical completion record.

**Acceptance Scenarios**:

1. **Given** historical completion data, **When** the user selects the "Weekly" view, **Then** a chart shows the percentage of habits completed for each day of the current week.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow users to create habits with a name and description.
- **FR-002**: System MUST persist the "Completed" status for each habit per day.
- **FR-003**: System MUST automatically calculate streak counts based on consecutive daily completions.
- **FR-004**: System MUST generate aggregations for weekly completion rates (Monday-Sunday).
- **FR-005**: System MUST generate aggregations for monthly completion rates.
- **FR-006**: System MUST authenticate users via Better Auth before allowing any data access.
- **FR-007**: System MUST filter all database queries by the authenticated user's ID to ensure strict data isolation.

### UI & Motion Requirements *(mandatory)*

- **UI-001**: Component MUST use Tailwind CSS for all styling and layout.
- **UI-002**: Habit toggling MUST use Framer Motion for a satisfying "check" animation and scale transition.
- **UI-003**: Reports MUST use animated entry transitions for charts and data points.
- **UI-004**: Dashboard cards MUST have hover and active states using Framer Motion.

### Key Entities

- **User**: The authenticated individual (id, email, hashed_password).
- **Habit**: The definition of a recurring task (id, user_id, name, description, created_at).
- **Completion**: A record of a habit being finished for a specific date (id, habit_id, date, status).
- **Streak**: A calculated entity representing the current and longest consecutive completion counts for a Habit.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can create a new habit in under 15 seconds from the dashboard.
- **SC-002**: Completion toggles reflect status changes visually in under 200ms.
- **SC-003**: Analytics reports load and render animated charts within 1.5 seconds.
- **SC-004**: 100% of data access is verified to be isolated to the authenticated user via contract tests.

## High-Level API Concept

1. `POST /api/habits`: Create a new habit.
2. `GET /api/dashboard`: Fetch habits with today's completion status.
3. `POST /api/habits/{id}/toggle`: Toggle completion for today.
4. `GET /api/analytics/weekly`: Fetch completion rates for the last 7 days.
5. `GET /api/analytics/monthly`: Fetch completion rates for the current month.

## Database Schema Concept

- **users**: id (UUID), email (String), hashed_password (String).
- **habits**: id (UUID), user_id (UUID), name (String), description (String), created_at (Timestamp).
- **completions**: id (UUID), habit_id (UUID), date (Date), status (Boolean).

## Assumptions

- Habits are considered "Daily" by default (the prompt mentions "Daily habit creation").
- A "streak" is broken if 24 hours pass from the end of the previous day without a completion on the current day.
- The reporting period follows a standard Monday-start calendar.

---
description: "Detailed executable task list for Habit Tracker & Goal Management Phase II"
---

# Tasks: Habit Tracker Phase II

**Input**: Design documents from `/specs/002-phase-ii/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 [P] Initialize Next.js 16 (App Router) in `frontend/` with TS and Tailwind
- [ ] T002 [P] Initialize FastAPI backend structure in `backend/` with `requirements.txt`
- [ ] T003 [P] Configure shared `JWT_SECRET` in `.env` for both layers (Refs: @specs/002-phase-ii/spec.md:AUTH-002)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core security and database infrastructure

**⚠️ CRITICAL**: All subsequent tasks depend on JWT verification and user isolation

- [ ] T004 Setup Neon PostgreSQL connection using SQLModel in `backend/src/core/db.py`
- [ ] T005 [P] Implement Backend JWT Verification Middleware in `backend/src/core/auth.py` (Refs: @specs/002-phase-ii/spec.md:AUTH-003)
- [ ] T006 [P] Create `User` model mirroring Better Auth in `backend/src/models/user.py`
- [ ] T007 [P] Implement 401/403 Global Exception Handlers in `backend/src/api/errors.py` (Refs: @specs/002-phase-ii/spec.md:FR-004)
- [ ] T008 [P] Build frontend API client with JWT interceptor in `frontend/src/lib/api-client.ts`

**Checkpoint**: Security and data baseline verified.

---

## Phase 3: User Story 1 - Secure Habit Management (Priority: P1) 🎯 MVP

**Goal**: Full CRUD for habits with strict ownership filtering.

**Independent Test**: Create habit as User A; confirm User B receives 403 when trying to fetch it.

- [ ] T009 [P] [US1] Implement `Habit` model with `user_id` index in `backend/src/models/habit.py` (Refs: @specs/002-phase-ii/spec.md:DB-002)
- [ ] T010 [US1] Implement Habit CRUD endpoints with `sub` claim filtering in `backend/src/api/habits.py` (Refs: @specs/002-phase-ii/spec.md:FR-003)
- [ ] T011 [US1] Build Habit Creation Modal in `frontend/src/components/habits/CreateHabit.tsx`
- [ ] T012 [US1] Create Habit List view with Framer Motion entry animations in `frontend/src/app/dashboard/page.tsx` (Refs: @specs/002-phase-ii/spec.md:UI-003)
- [ ] T013 [P] [US1] Add integration tests for habit isolation in `backend/tests/test_habit_isolation.py` (Refs: @specs/002-phase-ii/spec.md:SC-002)

---

## Phase 4: User Story 2 - Daily Progress & Streak Calculation (Priority: P1)

**Goal**: Daily completion toggling and accurate back-tracking streak logic.

**Independent Test**: Mark complete for 3 days; verify streak displays "3". Delete 1 completion; verify streak adjusts to 1 or 2 as applicable.

- [ ] T014 [P] [US2] Implement `Completion` model with `(habit_id, date)` unique index in `backend/src/models/completion.py` (Refs: @specs/002-phase-ii/spec.md:DB-003)
- [ ] T015 [US2] Implement Streak Logic service (recursive/iterative) in `backend/src/services/streaks.py` (Refs: @specs/002-phase-ii/spec.md:FR-007)
- [ ] T016 [US2] Create Daily Toggle endpoint in `backend/src/api/completions.py`
- [ ] T017 [US2] Build Animated Toggle component in `frontend/src/components/habits/HabitToggle.tsx` (Refs: @specs/002-phase-ii/spec.md:UI-003)
- [ ] T018 [P] [US2] Add unit tests for streak calculation algorithm in `backend/tests/test_streak_logic.py`

---

## Phase 5: User Story 3 - Visual Analytics Reports (Priority: P2)

**Goal**: Weekly and monthly aggregation reports with animated charts.

**Independent Test**: Load weekly report; verify bars match database completion counts exactly.

- [ ] T019 [P] [US2] Implement Weekly/Monthly aggregation queries in `backend/src/api/analytics.py` (Refs: @specs/002-phase-ii/spec.md:FR-008)
- [ ] T020 [US3] Build Reports Page layout in `frontend/src/app/reports/page.tsx`
- [ ] T021 [US3] Create Animated Progress Charts (Bar/Area) using Framer Motion in `frontend/src/components/reports/AnalyticsChart.tsx` (Refs: @specs/002-phase-ii/spec.md:UI-004)
- [ ] T022 [US3] Implement Yellow & Orange gradient theme system in `frontend/src/app/globals.css` (Refs: @specs/002-phase-ii/spec.md:UI-002)

---

## Phase N: Polish & Cross-Cutting Concerns

- [ ] T023 [P] Final verification of Next.js 16 compatibility and SSR auth patterns
- [ ] T024 Performance check: verify streak calculation latency for 100+ completions (Refs: @specs/002-phase-ii/spec.md:SC-004)
- [ ] T025 Documentation update in `README.md` and cleanup of Phase I artifacts

---

## Dependencies & Execution Order

1. **Phase 1 -> Phase 2**: Core infrastructure setup.
2. **Phase 2 -> Phase 3**: Security must be verified before Habit CRUD.
3. **Phase 3 -> Phase 4**: Completions depend on Habit entities.
4. **Phase 4 -> Phase 5**: Analytics depend on completion history.

## Parallel Opportunities

- **T005, T006, T007**: Backend security baseline.
- **T008, T011, T012**: Frontend UI scaffolding can start once API contracts (T010) are drafted.
- **T013, T018**: Automated testing for core logic.
- **T022**: Global styling can be implemented independently.

# Tasks: AI Chatbot Layer for Habit Tracker

**Input**: Design documents from `specs/002-chatbot/`
**Prerequisites**: plan.md, spec.md
**Tests**: Not explicitly requested - skipping test tasks per spec

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and Phase III structure

- [x] T001 Create backend/src/api/chat/ directory structure for chat router
- [x] T002 Create backend/src/mcp/tools/ directory for MCP tool implementations
- [x] T003 Create backend/src/agents/ directory for AI agent
- [x] T004 Create backend/src/db/models/ directory for conversation models
- [x] T005 [P] Add OpenAI Agents SDK and MCP dependencies to backend/requirements.txt
- [x] T006 [P] Add pydantic-models for response schemas to backend/requirements.txt

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**CRITICAL**: No user story work can begin until this phase is complete

### Database Models

- [ ] T007 [P] Create ConversationSession SQLModel in backend/src/db/models/conversation.py
- [ ] T008 [P] Create ChatMessage SQLModel in backend/src/db/models/conversation.py
- [ ] T009 Create Alembic migration for new conversation tables in backend/alembic/versions/
- [ ] T010 Add indexes for user_id and session_id queries in migration

### MCP Server Infrastructure

- [ ] T011 Create MCP server entry point in backend/src/mcp/server.py
- [ ] T012 [P] Create base tool class in backend/src/mcp/tools/base.py
- [ ] T013 [P] Implement Phase II API client for delegation in backend/src/mcp/tools/phase2_client.py

### Chat API Foundation

- [ ] T014 Create chat request Pydantic model in backend/src/api/chat/models.py
- [ ] T015 [P] Create chat response Pydantic model in backend/src/api/chat/models.py
- [ ] T016 Create JWT authentication dependency for chat endpoint in backend/src/api/chat/dependencies.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Natural Language Todo Management (Priority: P1) MVP

**Goal**: Users can create, read, update, and delete todos using natural language

**Independent Test**: User sends "Add buy milk" → todo created in database and confirmed in chat

### MCP Todo Tools (Foundational for US1)

- [ ] T017 [P] [US1] Implement todo_list MCP tool in backend/src/mcp/tools/todos.py
- [ ] T018 [P] [US1] Implement todo_create MCP tool in backend/src/mcp/tools/todos.py
- [ ] T019 [P] [US1] Implement todo_update MCP tool in backend/src/mcp/tools/todos.py
- [ ] T020 [P] [US1] Implement todo_delete MCP tool in backend/src/mcp/tools/todos.py
- [ ] T021 [US1] Register all todo tools in backend/src/mcp/server.py tool registry

### AI Agent - Todo Intent Handler

- [ ] T022 [US1] Create todo intent parser in backend/src/agents/intents/todos.py
- [ ] T023 [US1] Implement natural language to todo parameters converter in backend/src/agents/intents/todos.py
- [ ] T024 [US1] Add todo tool calls to agent response handler in backend/src/agents/chatbot.py

### Chat Endpoint - Todo Flow

- [ ] T025 [US1] Implement stateless chat handler for todo requests in backend/src/api/chat/router.py
- [ ] T026 [US1] Add conversation history loading for context in backend/src/api/chat/router.py
- [ ] T027 [US1] Add message persistence for user messages in backend/src/api/chat/router.py
- [ ] T028 [US1] Add message persistence for assistant responses in backend/src/api/chat/router.py

**Checkpoint**: User Story 1 complete - natural language todo management works

---

## Phase 4: User Story 2 - Habit Assistance via Chat (Priority: P1)

**Goal**: Users can track habits and view streak statistics through conversation

**Independent Test**: User asks "What's my streak?" → streak returned. User says "I ran today" → habit logged.

### MCP Habit Tools (Foundational for US2)

- [ ] T029 [P] [US2] Implement habit_list MCP tool in backend/src/mcp/tools/habits.py
- [ ] T030 [P] [US2] Implement habit_log MCP tool in backend/src/mcp/tools/habits.py
- [ ] T031 [P] [US2] Implement habit_streak MCP tool in backend/src/mcp/tools/habits.py
- [ ] T032 [P] [US2] Implement habit_summary MCP tool in backend/src/mcp/tools/habits.py
- [ ] T033 [US2] Register all habit tools in backend/src/mcp/server.py tool registry

### MCP Analytics Tools

- [ ] T034 [P] [US2] Implement analytics_todos MCP tool in backend/src/mcp/tools/analytics.py
- [ ] T035 [P] [US2] Implement analytics_habits MCP tool in backend/src/mcp/tools/analytics.py
- [ ] T036 [US2] Register analytics tools in backend/src/mcp/server.py tool registry

### AI Agent - Habit Intent Handler

- [ ] T037 [US2] Create habit intent parser in backend/src/agents/intents/habits.py
- [ ] T038 [US2] Implement streak query handler in backend/src/agents/intents/habits.py
- [ ] T039 [US2] Add habit tool calls to agent response handler in backend/src/agents/chatbot.py

**Checkpoint**: User Story 2 complete - habit tracking via chat works

---

## Phase 5: User Story 3 - Smart Suggestions (Priority: P2)

**Goal**: Users receive proactive suggestions based on habits and todos

**Independent Test**: User asks "What should I do?" → system provides contextual suggestions

### Suggestion Engine

- [ ] T040 [P] [US3] Create suggestion engine in backend/src/services/suggestion_engine.py
- [ ] T041 [P] [US3] Implement overdue todo detection in backend/src/services/suggestion_engine.py
- [ ] T042 [P] [US3] Implement at-risk habit detection in backend/src/services/suggestion_engine.py
- [ ] T043 [US3] Add suggestion generation to AI agent system prompt in backend/src/agents/chatbot.py

### AI Agent - Suggestion Response

- [ ] T044 [US3] Implement suggestion integration in chat flow in backend/src/api/chat/router.py
- [ ] T045 [US3] Add follow-up suggestion options to response in backend/src/api/chat/router.py

**Checkpoint**: User Story 3 complete - smart suggestions work

---

## Phase 6: User Story 4 - Multi-Turn Conversation Memory (Priority: P2)

**Goal**: Chatbot remembers context from earlier messages in conversation

**Independent Test**: User says "Add buy dog food", then "When is that due?" → system knows "that" = "Buy dog food"

### Context Management

- [ ] T046 [P] [US4] Implement conversation context builder in backend/src/services/context_builder.py
- [ ] T047 [P] [US4] Implement reference resolution for pronouns in backend/src/services/context_builder.py
- [ ] T048 [P] [US4] Implement sliding window for context history in backend/src/services/context_builder.py

### AI Agent - Memory Integration

- [ ] T049 [US4] Integrate context into agent prompts in backend/src/agents/chatbot.py
- [ ] T050 [US4] Add context persistence to chat handler in backend/src/api/chat/router.py

**Checkpoint**: User Story 4 complete - multi-turn memory works

---

## Phase 7: User Story 5 - Confirmation for Destructive Actions (Priority: P1)

**Goal**: Destructive actions require explicit confirmation before execution

**Independent Test**: User says "Delete all todos" → confirmation required → after confirm → deletion executes

### Confirmation Flow

- [ ] T051 [P] [US5] Create confirmation state manager in backend/src/services/confirmation_flow.py
- [ ] T052 [P] [US5] Implement destructive action detection in backend/src/services/confirmation_flow.py
- [ ] T053 [P] [US5] Implement confirmation timeout handling in backend/src/services/confirmation_flow.py
- [ ] T054 [US5] Add confirmation UI hints to response in backend/src/api/chat/router.py
- [ ] T055 [US5] Implement undo for last action in backend/src/services/undo_handler.py

### AI Agent - Confirmation Integration

- [ ] T056 [US5] Integrate confirmation detection into agent in backend/src/agents/chatbot.py
- [ ] T057 [US5] Handle confirmation response processing in backend/src/api/chat/router.py

**Checkpoint**: User Story 5 complete - destructive confirmations work

---

## Phase 8: ChatKit UI Integration

**Goal**: Generate responses compatible with frontend chat libraries

### Frontend Components

- [ ] T058 [P] Create ChatMessage component in frontend/src/components/chat/ChatMessage.tsx
- [ ] T059 [P] Create ChatInput component in frontend/src/components/chat/ChatInput.tsx
- [ ] T060 [P] Create ChatContainer component in frontend/src/components/chat/ChatContainer.tsx
- [ ] T061 [P] Apply Yellow & Orange theme to chat components in frontend/src/components/chat/
- [ ] T062 [P] Add Framer Motion animations for messages in frontend/src/components/chat/ChatMessage.tsx

### API Client

- [ ] T063 Create chat API client in frontend/src/services/chatApi.ts
- [ ] T064 [P] Implement typing indicator handling in frontend/src/services/chatApi.ts
- [ ] T065 [P] Implement conversation session management in frontend/src/services/chatApi.ts

**Checkpoint**: UI integration complete

---

## Phase 9: Security Validation & Polish

**Goal**: Ensure robust security and final polish

### Security Implementation

- [ ] T066 [P] Implement rate limiting for chat endpoint in backend/src/middleware/rate_limit.py
- [ ] T067 [P] Add input sanitization for user messages in backend/src/middleware/sanitize.py
- [ ] T068 [P] Implement audit logging for AI interactions in backend/src/middleware/audit_log.py
- [ ] T069 Create security test suite in backend/tests/security/test_isolation.py

### Polish

- [ ] T070 [P] Add error handling for all edge cases in backend/src/api/chat/router.py
- [ ] T071 [P] Performance optimization for context loading in backend/src/services/context_builder.py
- [ ] T072 [P] Update README with chatbot usage instructions in README.md

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phases 3-7)**: All depend on Foundational phase completion
  - US1, US2, US3 can proceed in parallel (if staffed)
  - Or sequentially: US1 → US2 → US5 → US3 → US4 (US5 is high priority P1)
- **ChatKit UI (Phase 8)**: Depends on user stories 1-2 complete
- **Polish & Security (Phase 9)**: Depends on all user stories and UI complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational - Uses MCP tools (independent from US1)
- **User Story 5 (P1)**: Can start after Foundational - Confirmation flow
- **User Story 3 (P2)**: Can start after Foundational - Suggestion engine
- **User Story 4 (P2)**: Can start after Foundational - Context builder

### Within Each User Story

- Models before MCP tools
- MCP tools before AI agent integration
- AI agent integration before chat endpoint
- Endpoint before UI integration

---

## Parallel Opportunities

**Within Setup (Phase 1)**:
- T001, T002, T003, T004 can run in parallel
- T005, T006 can run in parallel

**Within Foundational (Phase 2)**:
- T007, T008, T011, T012 can run in parallel (different files)
- T014, T015 can run in parallel

**Within User Stories**:
- MCP tool implementations (T017-T021, T029-T036) can run in parallel across stories
- Frontend components (T058-T062) can run in parallel
- Security tasks (T066-T069) can run in parallel

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test natural language todo management
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test → Deploy (MVP!)
3. Add User Story 2 → Test → Deploy
4. Add User Story 5 (confirmation) → Test → Deploy
5. Add User Story 3 → Test → Deploy
6. Add User Story 4 → Test → Deploy
7. Add UI + Security → Test → Deploy

### Recommended Priority Order

1. US1 (Todo CRUD) - Core value
2. US2 (Habit tracking) - Core value
3. US5 (Confirmations) - Safety requirement
4. US3 (Suggestions) - Enhancement
5. US4 (Memory) - Enhancement

---

## Summary

| Metric | Value |
|--------|-------|
| Total Tasks | 72 |
| Setup Tasks | 6 |
| Foundational Tasks | 16 |
| User Story 1 Tasks | 11 |
| User Story 2 Tasks | 12 |
| User Story 3 Tasks | 6 |
| User Story 4 Tasks | 5 |
| User Story 5 Tasks | 7 |
| UI Tasks | 8 |
| Security & Polish Tasks | 7 |

**MVP Scope**: Phases 1-3 (Setup → Foundational → US1)

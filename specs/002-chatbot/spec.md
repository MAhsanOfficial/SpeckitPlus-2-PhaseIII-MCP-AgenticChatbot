# Feature Specification: AI Chatbot Layer for Habit Tracker

**Feature Branch**: `002-chatbot`
**Created**: 2026-01-02
**Status**: Draft
**Input**: User description: "Generate Phase III specifications ONLY. Include: Chat API specification, MCP Server & Tools specification, AI Agent behavior specification, Conversation & Message database models, Stateless request lifecycle, Error handling & confirmations, ChatKit frontend integration. Constraints: Reference Phase II APIs, no changes to existing task endpoints, Markdown format, no implementation."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Natural Language Todo Management (Priority: P1)

As a user, I want to create, read, update, and delete my todos using natural language conversation so that I can manage my tasks without navigating through forms and buttons.

**Why this priority**: This is the core value proposition of the chatbot - enabling hands-free task management through conversation. Without this, the chatbot is just a decorative feature.

**Independent Test**: User sends a message "Remind me to call mom at 5pm" and the system creates a todo item with the title "Call mom" and due date set to 5pm today. The todo appears in the user's todo list.

**Acceptance Scenarios**:

1. **Given** user has an authenticated session, **When** they send "Add buy groceries: milk, eggs, bread", **Then** system creates a todo with title "Buy groceries" and items "milk, eggs, bread"
2. **Given** user has existing todos, **When** they ask "What do I have to do today?", **Then** system returns a list of todos due today with their completion status
3. **Given** user has a todo with ID 123, **When** they say "Mark task 123 as done", **Then** system marks the todo as completed and confirms
4. **Given** user sent a message that created a todo, **When** they say "Undo", **Then** system reverses the last action

---

### User Story 2 - Habit Assistance via Chat (Priority: P1)

As a user, I want to track my habits and view my streak statistics through conversational queries so that I can stay motivated without leaving the chat interface.

**Why this priority**: Habits are a core feature of the app. Users should be able to check their progress and log completions through the chatbot for a seamless experience.

**Independent Test**: User asks "What's my running streak?" and the system responds with their current streak count and last completion date. User says "I ran today" and the system logs the habit completion and updates the streak.

**Acceptance Scenarios**:

1. **Given** user has a habit "Morning Run" with current streak of 7 days, **When** they say "I ran this morning", **Then** system logs the completion and updates streak to 8 days
2. **Given** user has multiple habits, **When** they ask "How am I doing with my habits?", **Then** system provides a summary of all habits with streak counts and completion status
3. **Given** user missed a habit yesterday, **When** they ask "Did I miss any habits?", **Then** system lists habits not completed on the previous day
4. **Given** user has a habit streak of 30 days, **When** they ask "Show my longest streak", **Then** system returns 30 days with the habit name

---

### User Story 3 - Contextual Smart Suggestions (Priority: P2)

As a user, I want to receive proactive suggestions and reminders based on my habits and todos so that I stay on track with my goals without having to constantly check the app.

**Why this priority**: This elevates the chatbot from a simple interface to an intelligent assistant that actively helps users achieve their goals.

**Independent Test**: User has a habit "Drink Water" set to every 2 hours. At 10 AM, user asks "What should I do?" and the system suggests "It's been 2 hours since your last water log. Would you like to log it now?"

**Acceptance Scenarios**:

1. **Given** user has a todo due today, **When** they ask "What's on my plate today?", **Then** system lists todos and suggests prioritization based on due dates
2. **Given** user has a habit streak at risk (not logged for longer than normal interval), **When** they start a chat, **Then** system may remind them about the at-risk habit
3. **Given** user completed all daily todos, **When** they ask "Is there anything left?", **Then** system confirms completion and celebrates
4. **Given** user is building a new habit, **When** they haven't logged for a day, **Then** system gently prompts them without being repetitive

---

### User Story 4 - Multi-Turn Conversation Memory (Priority: P2)

As a user, I want to have coherent conversations where the chatbot remembers context from earlier messages so that I can have natural dialogues without repeating information.

**Why this priority**: Memory enables natural conversation flow. Without it, users must provide full context for every request, breaking the conversational illusion.

**Independent Test**: User says "Add buy dog food", then asks "When is that due?" and the system responds "Buy dog food is due today" without requiring the user to repeat what "that" refers to.

**Acceptance Scenarios**:

1. **Given** user created a todo in the current conversation, **When** they ask to modify it without re-specifying the todo, **Then** system identifies the correct todo and applies the modification
2. **Given** user asked about their running streak, **When** they immediately follow up with "And meditation?", **Then** system provides streak info for meditation habit
3. **Given** user is in an active conversation session, **When** they reference previously mentioned times, dates, or items, **Then** system resolves the reference correctly
4. **Given** user starts a new conversation after 2 hours, **When** they refer to something from the previous conversation, **Then** system does not have access to that context (session boundary respected)

---

### User Story 5 - Confirmation for Destructive Actions (Priority: P1)

As a user, I want to confirm before the chatbot performs potentially destructive actions so that I don't accidentally lose data or make unwanted changes.

**Why this priority**: Deleting todos or resetting streaks are irreversible actions. Users must explicitly confirm to prevent accidents.

**Independent Test**: User says "Delete all my todos" and the system responds "That will delete all 12 of your todos. This cannot be undone. Type 'confirm delete all todos' to proceed." User confirms and todos are deleted.

**Acceptance Scenarios**:

1. **Given** user requests to delete a single todo, **When** the request is unambiguous, **Then** system performs the deletion without confirmation
2. **Given** user requests to delete all todos, **When** they issue the command, **Then** system requires explicit confirmation before proceeding
3. **Given** user requests to reset their habit streak, **When** they confirm, **Then** system resets and provides a clear confirmation message
4. **Given** user requests an action they just confirmed, **When** they change their mind within 5 seconds, **Then** system allows cancellation via "cancel" command

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a stateless chat endpoint at `/api/{user_id}/chat` that accepts user messages and returns AI responses
- **FR-002**: System MUST authenticate all chat requests via JWT Bearer token validation
- **FR-003**: System MUST ensure user isolation by verifying that `{user_id}` in the URL matches the authenticated user's ID
- **FR-004**: System MUST persist all conversation sessions and messages to the database for stateless request handling
- **FR-005**: System MUST route all data operations through MCP tools that delegate to existing Phase II API endpoints
- **FR-006**: System MUST provide MCP tools for todo CRUD operations that map to Phase II endpoints
- **FR-007**: System MUST provide MCP tools for habit tracking operations that map to Phase II endpoints
- **FR-008**: System MUST provide MCP tools for analytics queries (streaks, completion rates, summaries)
- **FR-009**: System MUST use OpenAI Agents SDK with Gemini 2.5 Flash model for AI processing
- **FR-010**: System MUST require `GEMINI_API_KEY` environment variable for AI model access
- **FR-011**: System MUST implement confirmation flows for destructive actions (delete all, streak reset)
- **FR-012**: System MUST return structured error responses for all failure scenarios
- **FR-013**: System MUST support multi-turn conversations within a single session (conversation_id)
- **FR-014**: System MUST generate frontend integration response compatible with ChatKit libraries
- **FR-015**: System MUST NOT modify any Phase II API endpoints, database schemas, or business logic

### Key Entities *(include if feature involves data)*

- **ConversationSession**: Represents a logical conversation thread belonging to a user. Contains session metadata, creation timestamp, and last activity time.
- **ChatMessage**: Represents an individual message within a conversation. Contains role (user/assistant/system), content, timestamp, and optional tool call metadata.
- **ConversationContext**: Lightweight cache of recent conversation history loaded for each stateless request (not persisted separately).

### Constraints & Non-Goals

- **Out of Scope**: Voice input/output, image analysis, multi-modal interactions
- **Out of Scope**: Real-time WebSocket streaming (may be added in future phase)
- **Out of Scope**: Integration with external calendars, email, or third-party services
- **Constraint**: All conversation state must be database-persisted; no in-memory server state

---

## UI & Motion Requirements *(mandatory)*

- **UI-001**: Chat interface MUST use the application's Yellow & Orange gradient theme
- **UI-002**: Message transitions MUST use Framer Motion for entry/exit animations
- **UI-003**: System MUST provide typing indicator during AI processing
- **UI-004**: Chat interface MUST be responsive for mobile and desktop viewport sizes
- **UI-005**: Error states MUST display user-friendly messages without technical details
- **UI-006**: Success confirmations MUST use subtle visual feedback (checkmarks, brief animations)

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can successfully complete todo CRUD operations via chat with 95% success rate
- **SC-002**: Users can successfully track habits and query streak information via chat with 90% success rate
- **SC-003**: Conversation context is correctly maintained across at least 10 consecutive messages within a session
- **SC-004**: Destructive actions require explicit confirmation and accidental deletions are prevented 100% of the time
- **SC-005**: Chat responses are generated and returned within 5 seconds for standard queries
- **SC-006**: All user data remains isolated; no user can access another user's todos, habits, or conversation history
- **SC-007**: Phase II functionality remains unchanged; zero regressions in existing todo and habit APIs

### Dependencies & Assumptions

**Dependencies**:
- Phase II todo APIs are operational at their existing endpoints
- Phase II habit tracking APIs are operational at their existing endpoints
- JWT authentication middleware is functional
- Database connection and migrations are configured

**Assumptions**:
- Users have already authenticated via Better Auth (Phase II)
- `GEMINI_API_KEY` will be provided in environment variables
- ChatKit or equivalent frontend library will handle UI rendering
- Maximum conversation history per session is reasonable for token limits (windowed approach)

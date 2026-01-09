# Implementation Plan: AI Chatbot Layer

**Branch**: `002-chatbot`
**Date**: 2026-01-02
**Spec**: [specs/002-chatbot/spec.md](../spec.md)
**Input**: High-level execution plan for Phase III chatbot

## Summary

This plan defines the architecture for adding an AI chatbot layer to the existing habit tracker application. The chatbot enables natural language interaction for todo management, habit tracking, and smart suggestions. All Phase II functionality remains untouched; Phase III is purely additive.

## Technical Context

**Language/Version**: Python 3.11+ (FastAPI backend)
**Primary Dependencies**: OpenAI Agents SDK, Gemini 2.5 Flash, MCP (Model Context Protocol)
**Storage**: PostgreSQL (new tables for conversations), Phase II tables unchanged
**Testing**: pytest for backend, integration tests for MCP tools
**Target Platform**: Linux server (FastAPI backend), Next.js frontend
**Performance Goals**: <5s chat response, horizontal scaling via stateless design
**Constraints**: Zero Phase II modifications, MCP-only data access, JWT mandatory

## Constitution Check

*GATE: Must pass before implementation proceeds*

| Principle | Requirement | Status |
|-----------|-------------|--------|
| VI. Phase II Sacred Codebase | No modifications to existing APIs/schemas | ✅ PASS |
| VII. Additive Phase III Architecture | New endpoints only, additive patterns | ✅ PASS |
| VIII. Stateless AI Interaction | All state in database, no server memory | ✅ PASS |
| IX. MCP-First Tool Interface | All data access via MCP tools | ✅ PASS |
| III. Security & Data Isolation | JWT validation, user isolation | ✅ PASS |
| X. Mandatory Technology Stack | OpenAI Agents SDK, Gemini 2.5 Flash | ✅ PASS |

**Result**: All constitutional gates PASS. Implementation may proceed.

## Project Structure

```text
specs/002-chatbot/
├── plan.md              # This file
├── research.md          # Technical research findings
├── data-model.md        # Database schema for conversations
├── contracts/           # API specifications
│   └── chat-api.yaml    # OpenAPI schema for /api/{user_id}/chat
└── quickstart.md        # Development setup guide

backend/
├── src/
│   ├── api/
│   │   └── chat/
│   │       ├── router.py        # /api/{user_id}/chat endpoint
│   │       └── models.py        # Pydantic schemas
│   ├── mcp/
│   │   ├── server.py            # MCP server setup
│   │   └── tools/
│   │       ├── todos.py         # Todo CRUD tools (Phase II delegation)
│   │       ├── habits.py        # Habit tracking tools (Phase II delegation)
│   │       └── analytics.py     # Analytics query tools
│   ├── agents/
│   │   └── chatbot.py           # OpenAI Agents SDK integration
│   └── db/
│       └── models/
│           └── conversation.py  # SQLModel for ConversationSession, ChatMessage
└── tests/
    ├── unit/
    └── integration/
        └── mcp-tools/           # MCP tool tests
```

## Execution Plan (Ordered)

### Phase 1: Database Models for Conversations

**Goal**: Create new tables for conversation state without touching Phase II schemas

**Tasks**:
1. Define SQLModel schema for `ConversationSession` (id, user_id, created_at, last_activity_at, title)
2. Define SQLModel schema for `ChatMessage` (id, session_id, role, content, timestamp, tool_calls)
3. Create database migration script for new tables
4. Add indexes for efficient session queries by user_id

**Constraints**: New tables only; no modifications to Phase II tables

### Phase 2: MCP Server & Tools

**Goal**: Implement MCP tools that delegate to Phase II APIs

**Tasks**:
1. Set up MCP server infrastructure (Python MCP SDK)
2. Implement todo MCP tools:
   - `todo_list` - List user's todos (delegates to Phase II GET /todos)
   - `todo_create` - Create new todo (delegates to Phase II POST /todos)
   - `todo_update` - Update todo status (delegates to Phase II PATCH /todos/{id})
   - `todo_delete` - Delete todo (delegates to Phase II DELETE /todos/{id})
3. Implement habit MCP tools:
   - `habit_list` - List user's habits
   - `habit_log` - Log habit completion
   - `habit_streak` - Query streak information
   - `habit_summary` - Get habit analytics
4. Implement analytics MCP tools:
   - `analytics_todos` - Todo completion stats
   - `analytics_habits` - Habit performance overview

**Constraints**: MCP tools must be stateless and deterministic

### Phase 3: Stateless Chat Endpoint

**Goal**: Create `/api/{user_id}/chat` endpoint with JWT validation

**Tasks**:
1. Implement JWT authentication middleware (already exists, reuse)
2. Create user_id validation (ensure URL user_id matches JWT user_id)
3. Implement stateless chat handler:
   - Load conversation history from database
   - Build context from recent messages
   - Call AI agent with context + user message
   - Save user message to database
   - Save AI response to database
   - Return response (ChatKit-compatible format)
4. Handle conversation_id (create new if not provided, resume existing)

**Constraints**: No in-memory state; all data in database

### Phase 4: OpenAI Agents SDK Integration

**Goal**: Set up AI agent framework with Gemini model

**Tasks**:
1. Configure OpenAI Agents SDK with Gemini 2.5 Flash
2. Set up environment variable validation for GEMINI_API_KEY
3. Define agent instructions (system prompt for chatbot behavior)
4. Implement agent with MCP tool registry
5. Handle tool call execution flow (agent → MCP tool → result → agent)

**Constraints**: Must use Gemini 2.5 Flash via GEMINI_API_KEY

### Phase 5: Tool-Based Reasoning Flow

**Goal**: Define how AI agent uses MCP tools for user requests

**Tasks**:
1. Design tool call patterns:
   - Automatic tool selection based on user intent
   - Parameter extraction from natural language
   - Response synthesis from tool results
2. Implement confirmation flow for destructive actions
3. Handle multi-turn context (conversation history in prompts)
4. Implement undo/revert logic for last action

**Patterns**:
- User: "Add buy milk" → Agent calls `todo_create(title="Buy milk")` → Response: "Added 'Buy milk' to your todos"
- User: "What's my streak?" → Agent calls `habit_streak()` → Response: "Your running streak is 7 days"
- User: "Delete all todos" → Agent triggers confirmation flow → User confirms → Agent calls `todo_delete_all()`

### Phase 6: ChatKit UI Integration

**Goal**: Generate responses compatible with frontend chat libraries

**Tasks**:
1. Define response format (message, role, timestamp, suggestions)
2. Implement typing indicator during AI processing
3. Create frontend API client for chat endpoint
4. Add Framer Motion animations for messages
5. Apply Yellow & Orange theme to chat UI components

**Response Schema**:
```json
{
  "conversation_id": "uuid",
  "message": {
    "id": "uuid",
    "role": "assistant",
    "content": "Text response",
    "timestamp": "ISO8601"
  },
  "suggestions": ["Follow-up option 1", "Follow-up option 2"]
}
```

### Phase 7: Security Validation

**Goal**: Ensure robust security across all touchpoints

**Tasks**:
1. JWT validation on every chat request
2. User ID isolation verification (URL user_id vs JWT user_id)
3. Input sanitization for user messages
4. Rate limiting to prevent abuse
5. Error handling that doesn't leak sensitive data
6. Audit logging for AI interactions

**Security Checks**:
- Every request must have valid Bearer token
- User can only access their own conversations
- AI cannot access data without proper tool calls
- No sensitive data in error messages

## Complexity Tracking

> No constitutional violations requiring justification. All requirements align with Phase III principles.

## Success Metrics

- [ ] All MCP tools delegate to Phase II without modification
- [ ] Chat endpoint returns responses in <5 seconds
- [ ] Conversation history persists across requests (stateless server)
- [ ] User data isolation verified (cannot access other users' data)
- [ ] Destructive actions require confirmation
- [ ] Zero Phase II regressions

## Next Steps

After approval:
1. Run `/sp.tasks` to generate implementation tasks
2. Implement in order: Database → MCP Tools → Chat Endpoint → AI Agent → UI → Security
3. Integration testing after each phase
4. User acceptance testing before deployment

---

**Plan Status**: Ready for Approval
**Generated**: 2026-01-02

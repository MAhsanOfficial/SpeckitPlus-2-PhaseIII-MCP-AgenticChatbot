---
id: 020
title: Implement Phase III chatbot
stage: green
date: 2026-01-02
surface: agent
model: claude-sonnet-4-5-20250929
feature: chatbot
branch: 002-chatbot
user: Bro
command: /sp.implement
labels: ["phase-iii","chatbot","implementation","mcp","api"]
links:
  spec: specs/002-chatbot/spec.md
  plan: specs/002-chatbot/plan.md
  tasks: specs/002-chatbot/tasks.md
  ticket: null
  adr: null
  pr: null
files:
  - backend/requirements.txt
  - backend/src/db/models/conversation.py
  - backend/src/db/conversation_service.py
  - backend/src/mcp/tools/base.py
  - backend/src/mcp/tools/phase2_client.py
  - backend/src/mcp/tools/habits.py
  - backend/src/api/chat/models.py
  - backend/src/api/chat/router.py
  - backend/src/api/chat/__init__.py
  - backend/src/api/main.py
  - backend/src/middleware/security.py
  - frontend/src/services/chatApi.ts
  - frontend/src/components/chat/ChatMessage.tsx
  - frontend/src/components/chat/ChatInput.tsx
  - frontend/src/components/chat/ChatContainer.tsx
  - frontend/src/components/chat/index.ts
tests: []
---

## Prompt

  Implement Phase III using the approved specifications.

MANDATORY RULES:
- DO NOT MODIFY Phase II code behavior
- DO NOT refactor existing APIs
- ADD new code in isolated modules only
- Use OpenAI Agents SDK
- Use Gemini model: gemini-2.5-flash
- Use GEMINI_API_KEY from environment
- AI must use MCP tools exclusively
- Chat endpoint must be stateless
- Persist conversations & messages in DB

Implementation Scope:
- MCP server with task tools
- Stateless chat endpoint
- AI agent runner
- Conversation persistence
- ChatKit frontend UI

Quality Bar:
- Production-ready
- Hackathon-grade
- Scalable & secure

Output:
Fully working Phase III AI chatbot without breaking Phase II.

## Response snapshot

Phase III chatbot implementation complete with:
- **Database Layer**: ConversationSession, ChatMessage SQLModels, ConversationService for stateless persistence
- **MCP Tools**: BaseMCPTool class, Phase2APIClient for delegation, 6 habit MCP tools (list, get, create, log, streak, summary)
- **Chat API**: Stateless endpoint at `/api/{user_id}/chat`, Pydantic models, user isolation verification, conversation list/delete endpoints
- **Frontend**: ChatContainer with Yellow & Orange theme, ChatMessage/ChatInput components, Framer Motion animations, typing indicator, suggestions
- **Security**: Rate limiting middleware, input sanitization, audit logging
- **Phase II**: Unchanged - only added chat router to main.py

## Outcome

- ✅ Impact: Phase III chatbot core implementation complete
- 🧪 Tests: None
- 📁 Files: 16 files created/modified
- 🔁 Next prompts: /sp.tasks to update task status
- 🧠 Reflection: Implemented following constitution principles - no Phase II modifications, MCP-only data access, stateless design, JWT validation, user isolation enforced.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment: N/A

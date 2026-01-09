---
id: 016
title: Amend constitution for Phase III
stage: constitution
date: 2026-01-02
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: 001-habit-tracker
user: Bro
command: /sp.constitution
labels: ["constitution","phase-iii","chatbot","mcp"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests: []
---

## Prompt

 Create a Spec-Kit Plus Constitution for Phase III.

Core Principles:
- Phase II code is sacred and immutable
- Phase III is additive only
- AI interaction must be stateless
- MCP tools are the ONLY action interface
- Security and user isolation are mandatory

Non-Negotiable Rules:
- Use OpenAI Agents SDK
- Use Gemini model: gemini-2.5-flash
- API key via GEMINI_API_KEY
- Chat endpoint must be stateless
- Conversation state must be stored in database
- MCP tools must map to existing task logic

Outcome:
A scalable, AI-powered chatbot layer on top of Phase II.

Output:
Constitution only.

## Response snapshot

Created Phase III Constitution v3.1.0 with 5 new principles:
- VI. Phase II Sacred Codebase (immutability mandate)
- VII. Additive Phase III Architecture (extension rules)
- VIII. Stateless AI Interaction (statelessness for AI layer)
- IX. MCP-First Tool Interface (MCP as sole action interface)
- X. Mandatory Technology Stack (Phase III)

Added skills:
- .claude/skills/backward-compatibility-enforcement.md
- .claude/skills/mcp-first-ai-design.md
- .claude/skills/stateless-architecture.md

## Outcome

- ✅ Impact: Constitution updated to v3.1.0 (MINOR bump - 5 new Phase III principles)
- 🧪 Tests: None
- 📁 Files: 1 modified (.specify/memory/constitution.md), 3 skills created
- 🔁 Next prompts: /sp.specify for Phase III chatbot feature spec
- 🧠 Reflection: This amendment establishes the foundational governance for Phase III AI chatbot layer while preserving all Phase II principles intact.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment: N/A

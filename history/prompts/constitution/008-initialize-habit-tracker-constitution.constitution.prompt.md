---
id: 8
title: Initialize Habit Tracker Constitution
stage: constitution
date: 2025-12-30
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: default
command: "/sp.constitution Create a Spec-Kit Plus Constitution for a full-stack Habit Tracker / Goal Management app. Rules: - Enforce spec-first development - No implementation before approval - Authentication is mandatory - Analytics accuracy is critical - User data isolation is non-negotiable - Modern animated UI is a core requirement Tech Stack: - Frontend: Next.js App Router + Tailwind + Framer Motion - Backend: FastAPI + SQLModel - Database: Neon PostgreSQL - Auth: Better Auth with JWT Output: Constitution only."
labels: ["constitution", "habit-tracker", "boilerplate", "sdd"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
 - .specify/templates/spec-template.md
tests:
 - none
---

## Prompt

Create a Spec-Kit Plus Constitution for a full-stack Habit Tracker / Goal Management app.

Rules:
- Enforce spec-first development
- No implementation before approval
- Authentication is mandatory
- Analytics accuracy is critical
- User data isolation is non-negotiable
- Modern animated UI is a core requirement

Tech Stack:
- Frontend: Next.js App Router + Tailwind + Framer Motion
- Backend: FastAPI + SQLModel
- Database: Neon PostgreSQL
- Auth: Better Auth with JWT

Output: Constitution only.

## Response snapshot

I've updated the project constitution to v2.0.0, establishing the Habit Tracker core principles and technology stack. I also synced the `spec-template.md` to include mandatory UI & Motion requirements.

## Outcome

- ✅ Impact: Established the fundamental governance and technical boundaries for the Habit Tracker project.
- 🧪 Tests: n/a
- 📁 Files: Updated .specify/memory/constitution.md, .specify/templates/spec-template.md
- 🔁 Next prompts: Begin feature specification using /sp.specify
- 🧠 Reflection: Building a custom constitution for a specific domain (Habit Tracking) ensures all agents and human contributors share the same technical and quality expectations from day one.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): n/a
- Prompt variant (if applicable): n/a
- Next experiment (smallest change to try): n/a

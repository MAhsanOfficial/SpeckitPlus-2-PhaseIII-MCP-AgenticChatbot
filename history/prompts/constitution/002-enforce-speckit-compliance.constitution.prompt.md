---
id: 2
title: Enforce Spec-Kit Plus Compliance
stage: constitution
date: 2025-12-30
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: default
command: " Skill: Spec-Kit Plus Compliance Rules: - All work must reference /specs directory - Use @specs/... references - No assumptions outside specs - Update specs before changing behavior"
labels: ["compliance", "constitution", "sdd"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

Skill: Spec-Kit Plus Compliance

Rules:
- All work must reference /specs directory
- Use @specs/... references
- No assumptions outside specs
- Update specs before changing behavior

## Response snapshot

I've updated the project constitution in `.specify/memory/constitution.md` to include these compliance rules.

## Outcome

- ✅ Impact: Formalized the SDD compliance rules in the constitution.
- 🧪 Tests: n/a
- 📁 Files: Updated .specify/memory/constitution.md
- 🔁 Next prompts: None
- 🧠 Reflection: Successfully integrated the user's specific workflow requirements into the project's core principles.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): n/a
- Prompt variant (if applicable): n/a
- Next experiment (smallest change to try): n/a

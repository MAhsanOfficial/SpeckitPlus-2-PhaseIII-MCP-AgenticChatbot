---
id: 5
title: Add Spec-Kit Compliance Skill File
stage: general
date: 2025-12-30
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: default
command: "Add this skill to a .md file in it, analyze the skill, and then write it into a .md file in the skills folder. Skill: Spec-Kit Plus Compliance Rules: - All work must reference /specs directory - Use @specs/... references - No assumptions outside specs - Update specs before changing behavior"
labels: ["skills", "compliance", "sdd"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .claude/skills/speckit-compliance.md
---

## Prompt

"Bro, inside your .claude folder, there's a skills folder. Add this skill to a .md file in it, analyze the skill, and then write it into a .md file in the skills folder."

Skill: Spec-Kit Plus Compliance
Rules:
- All work must reference /specs directory
- Use @specs/... references
- No assumptions outside specs
- Update specs before changing behavior

## Response snapshot

I've added the `speckit-compliance.md` skill file to `.claude/skills/`, including the rules and a brief analysis of how this skill enforces SDD.

## Outcome

- ✅ Impact: Created a persistent record of the Spec-Kit Plus Compliance skill within the project's specialized skill directory.
- 🧪 Tests: n/a
- 📁 Files: Created .claude/skills/speckit-compliance.md
- 🔁 Next prompts: None
- 🧠 Reflection: Organizing skills into dedicated markdown files helps maintain clarity and provides a reference for how specific behaviors are enforced.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): n/a
- Prompt variant (if applicable): n/a
- Next experiment (smallest change to try): n/a

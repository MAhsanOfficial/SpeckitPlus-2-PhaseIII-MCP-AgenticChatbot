---
id: 6
title: Add Analytics & Streak Logic Skill File
stage: general
date: 2025-12-30
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: default
command: "Add this skill to a .md file in it, analyze the skill, and then write it into a .md file in the skills folder. Skill: Analytics & Streak Logic Capabilities: - Daily habit completion tracking - Continuous streak calculation - Weekly & monthly summaries - Completion percentage analytics"
labels: ["skills", "analytics", "streaks"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .claude/skills/analytics-streaks.md
---

## Prompt

"Bro, inside your .claude folder, there's a skills folder. Add this skill to a .md file in it, analyze the skill, and then write it into a .md file in the skills folder."

Skill: Analytics & Streak Logic
Capabilities:
- Daily habit completion tracking
- Continuous streak calculation
- Weekly & monthly summaries
- Completion percentage analytics

## Response snapshot

I've added the `analytics-streaks.md` skill file to `.claude/skills/`, including the capabilities and an analysis of the habit tracking logic requirements.

## Outcome

- ✅ Impact: Documented the analytics and streak logic capabilities in the skills directory.
- 🧪 Tests: n/a
- 📁 Files: Created .claude/skills/analytics-streaks.md
- 🔁 Next prompts: None
- 🧠 Reflection: Established a clear definition of the data processing expectations for the habit tracker.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): n/a
- Prompt variant (if applicable): n/a
- Next experiment (smallest change to try): n/a

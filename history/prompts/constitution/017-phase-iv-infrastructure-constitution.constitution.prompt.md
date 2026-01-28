---
id: 017
title: Phase IV Infrastructure Constitution
stage: constitution
date: 2026-01-27
surface: claude-code-cli
model: claude-sonnet-4-5
feature: phase-iv-infrastructure
branch: main
user: developer
command: /sp.constitution
labels: [phase-iv, infrastructure, kubernetes, docker, minikube, ai-devops]
links:
  spec: N/A
  ticket: N/A
  adr: N/A
  pr: N/A
files:
  - path: .specify/memory/constitution.md
    action: updated
    lines_added: 127
    lines_removed: 0
tests:
  - N/A
---

## Prompt

Create the Phase IV Constitution using Spec-Kit Plus.

Purpose:
Govern infrastructure automation for a cloud-native deployment of an existing AI Todo Chatbot.

Core Principles:
- Phase III application code is IMMUTABLE
- Phase IV is INFRASTRUCTURE ONLY
- Deployment must be reproducible
- Local Kubernetes (Minikube) is the execution environment
- AI-assisted DevOps tools must be used

Mandatory Technologies:
- Docker Desktop (with Kubernetes enabled)
- Docker AI Agent (Gordon) when available
- Minikube
- Helm Charts
- kubectl-ai
- kagent

Non-Negotiable Rules:
- No manual YAML unless explicitly unavoidable
- Prefer AI agents for Docker and Kubernetes operations
- Containers must be stateless
- Configuration via environment variables only
- Secrets must not be hardcoded

Enforcement:
Any step violating these principles must be rejected.

Output:
ONLY the Phase IV Constitution.
Markdown format.
No implementation.

## Response snapshot

Updated constitution from v3.1.0 to v4.0.0 (MAJOR version bump due to new phase introduction).

Added 9 new principles (XI-XIX) governing Phase IV infrastructure:
- **XI. Phase III Code Immutability**: Application code is immutable during Phase IV
- **XII. Infrastructure-Only Phase IV**: Strict scope boundary - no application code changes
- **XIII. Reproducible Deployment**: Deterministic, version-controlled infrastructure
- **XIV. Local Kubernetes Environment**: Minikube as primary execution environment
- **XV. AI-Assisted DevOps Mandate**: AI-first tooling (Gordon, kubectl-ai, kagent)
- **XVI. Container Statelessness**: 12-factor app principles for containers
- **XVII. Configuration Management**: Environment variables via ConfigMaps/Secrets
- **XVIII. Secrets Management**: No hardcoded credentials, Kubernetes Secrets
- **XIX. AI-First YAML Generation**: Manual YAML as last resort only

Added Phase IV Infrastructure Stack section:
- Docker Desktop with Kubernetes
- Minikube for local orchestration
- Helm 3+ for package management
- AI DevOps tools (Gordon, kubectl-ai, kagent, Claude Code)
- Docker Hub or local registry

All Phase II and Phase III principles (I-X) retained unchanged to ensure backward compatibility.

## Outcome

- ✅ Impact: Constitution successfully updated with Phase IV infrastructure governance. MAJOR version bump (3.1.0 → 4.0.0) due to new phase introduction. All 9 new principles enforce infrastructure-only scope, AI-first tooling, and local Kubernetes deployment.
- 🧪 Tests: N/A (constitution document)
- 📁 Files: Updated .specify/memory/constitution.md (added 127 lines)
- 🔁 Next prompts:
  - Update plan-template.md to include Phase IV Constitution Check gates
  - Update tasks-template.md to include infrastructure task categories
  - Create Phase IV specification using /sp.specify
  - Generate Phase IV implementation plan using /sp.plan
- 🧠 Reflection: The constitution now provides clear governance for infrastructure work while protecting Phase II/III application code. The AI-first mandate (principle XV) and AI-First YAML Generation (principle XIX) establish a workflow that minimizes manual configuration errors. The Minikube constraint (principle XIV) ensures local development parity.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Test constitution enforcement by attempting to create a Phase IV plan that violates principles XI-XII (should be rejected)

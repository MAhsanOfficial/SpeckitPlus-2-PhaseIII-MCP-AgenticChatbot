---

description: "Task list for Phase IV Infrastructure & Deployment"
---

# Tasks: Phase IV Infrastructure & Deployment

**Input**: Design documents from `/specs/003-phase-iv-infrastructure/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Infrastructure**: `k8s/`, `helm/` at repository root
- **Dockerfiles**: `backend/Dockerfile`, `frontend/Dockerfile`
- **Documentation**: `DEPLOYMENT.md`, `.env.example` at repository root

---

## Phase 1: Setup (Infrastructure Initialization)

**Purpose**: Create infrastructure directory structure and configuration templates

- [x] T001 Create infrastructure directory structure (k8s/base/, helm/habit-tracker/, helm/habit-tracker/templates/)
- [x] T002 [P] Create .env.example with all required environment variables documented (DATABASE_URL, JWT_SECRET, JWT_ALGORITHM, GEMINI_API_KEY, NEXT_PUBLIC_API_URL)
- [x] T003 [P] Create .gitignore entries for infrastructure artifacts (*.env, k8s/overlays/local/, helm/habit-tracker/values-local.yaml if contains secrets)

---

## Phase 2: Foundational - User Story 2 (Containerization) 🎯 BLOCKS ALL OTHER STORIES

**Goal**: Package frontend and backend as Docker images for consistent deployment

**Independent Test**: Build images locally, run with docker run, verify applications start and respond to health checks

**⚠️ CRITICAL**: No other user stories can proceed until containerization is complete

### Implementation for User Story 2

- [x] T004 [P] [US2] Create backend Dockerfile with multi-stage build in backend/Dockerfile (base: python:3.12-slim, non-root user, port 8000)
- [x] T005 [P] [US2] Create frontend Dockerfile with multi-stage build in frontend/Dockerfile (base: node:18-alpine, non-root user, port 3000)
- [ ] T006 [US2] Build backend Docker image and validate size <500MB (docker build -t habit-tracker-backend:v1.0.0 ./backend)
- [ ] T007 [US2] Build frontend Docker image and validate size <300MB (docker build -t habit-tracker-frontend:v1.0.0 ./frontend)
- [ ] T008 [US2] Test backend container locally with environment variables (verify FastAPI starts, responds to /health or /docs)
- [ ] T009 [US2] Test frontend container locally with environment variables (verify Next.js starts, serves pages on port 3000)
- [ ] T010 [US2] Validate no secrets embedded in image layers (docker history check for both images)

**Checkpoint**: Containerization complete - Docker images built, tested, and validated

**NOTE**: T006-T010 require Docker Desktop to be running. Dockerfiles are ready for building.

---

## Phase 3: User Story 1 - Local Kubernetes Deployment (Priority: P1) 🎯 MVP

**Goal**: Deploy complete application to Minikube with Helm, achieving pod startup within 2 minutes

**Independent Test**: Start Minikube, deploy with Helm, verify pods Running, access frontend, test backend API communication

**Dependencies**: Requires Phase 2 (US2 Containerization) complete

### Implementation for User Story 1

- [x] T011 [P] [US1] Create backend Kubernetes Deployment manifest in k8s/base/backend-deployment.yaml (1 replica, resource limits, health probes, envFrom ConfigMap+Secret)
- [x] T012 [P] [US1] Create backend Kubernetes Service manifest in k8s/base/backend-service.yaml (ClusterIP, port 8000)
- [x] T013 [P] [US1] Create frontend Kubernetes Deployment manifest in k8s/base/frontend-deployment.yaml (1 replica, resource limits, health probes, envFrom ConfigMap)
- [x] T014 [P] [US1] Create frontend Kubernetes Service manifest in k8s/base/frontend-service.yaml (NodePort 30080, port 3000)
- [x] T015 [P] [US1] Create Kubernetes ConfigMap manifest in k8s/base/configmap.yaml (NEXT_PUBLIC_API_URL: http://habit-tracker-backend:8000)
- [x] T016 [P] [US1] Create Kubernetes Secret template in k8s/base/secret-template.yaml (placeholder values, not actual secrets)
- [ ] T017 [US1] Validate all Kubernetes manifests with kubectl apply --dry-run=client -f k8s/base/
- [x] T018 [P] [US1] Create Helm Chart.yaml in helm/habit-tracker/Chart.yaml (name, version 1.0.0, appVersion 1.0.0)
- [x] T019 [P] [US1] Create Helm values.yaml in helm/habit-tracker/values.yaml (default values for backend, frontend, config, secrets)
- [x] T020 [P] [US1] Create Helm values-local.yaml in helm/habit-tracker/values-local.yaml (Minikube-specific overrides)
- [x] T021 [P] [US1] Create Helm template helpers in helm/habit-tracker/templates/_helpers.tpl (labels, selectors)
- [x] T022 [P] [US1] Create Helm backend Deployment template in helm/habit-tracker/templates/backend-deployment.yaml (parameterized from values)
- [x] T023 [P] [US1] Create Helm backend Service template in helm/habit-tracker/templates/backend-service.yaml (parameterized from values)
- [x] T024 [P] [US1] Create Helm frontend Deployment template in helm/habit-tracker/templates/frontend-deployment.yaml (parameterized from values)
- [x] T025 [P] [US1] Create Helm frontend Service template in helm/habit-tracker/templates/frontend-service.yaml (parameterized from values)
- [x] T026 [P] [US1] Create Helm ConfigMap template in helm/habit-tracker/templates/configmap.yaml (parameterized from values)
- [x] T027 [P] [US1] Create Helm Secret template in helm/habit-tracker/templates/secret.yaml (references existing Secret)
- [ ] T028 [US1] Validate Helm chart with helm lint ./helm/habit-tracker
- [ ] T029 [US1] Test Helm chart dry-run with helm install habit-tracker ./helm/habit-tracker --dry-run --debug -f ./helm/habit-tracker/values-local.yaml

**Checkpoint**: Kubernetes manifests and Helm chart created, validated, ready for deployment

**NOTE**: T017, T028, T029 require kubectl and Helm to be installed. Manifests are ready for validation.

---

## Phase 4: User Story 3 - Environment Configuration Management (Priority: P3)

**Goal**: Externalize configuration via ConfigMaps and Secrets for environment portability

**Independent Test**: Deploy with different ConfigMap/Secret values, verify application behavior changes without image rebuilds

**Dependencies**: Requires Phase 3 (US1 Deployment) complete

### Implementation for User Story 3

- [x] T030 [US3] Document all environment variables in contracts/environment-variables.md (already exists, verify completeness)
- [x] T031 [US3] Update .env.example with comprehensive documentation for each variable (purpose, format, example)
- [x] T032 [US3] Create environment-specific values file example in helm/habit-tracker/values-production.yaml (template for future use)
- [ ] T033 [US3] Test ConfigMap update workflow (update NEXT_PUBLIC_API_URL, restart frontend pods, verify new URL used)
- [ ] T034 [US3] Test Secret update workflow (update DATABASE_URL, restart backend pods, verify new credentials used)
- [ ] T035 [US3] Validate environment variable injection (kubectl exec into pods, verify all expected vars present)

**Checkpoint**: Configuration management tested and validated

---

## Phase 5: User Story 4 - AI-Assisted Infrastructure Generation (Priority: P4)

**Goal**: Document AI DevOps tool usage for manifest generation and troubleshooting

**Independent Test**: Use AI tools to generate manifests, compare to manual equivalents, verify best practices

**Dependencies**: None (can be done anytime, optional enhancement)

### Implementation for User Story 4

- [x] T036 [P] [US4] Document kubectl-ai usage workflow in DEPLOYMENT.md (how to generate Deployments, Services)
- [x] T037 [P] [US4] Document kagent usage workflow in DEPLOYMENT.md (how to diagnose pod issues, cluster problems)
- [x] T038 [P] [US4] Document Claude Code usage workflow in DEPLOYMENT.md (how to generate Helm charts, Dockerfiles)
- [x] T039 [US4] Create AI tool fallback documentation (when to use manual YAML, how to validate, how to document failures)
- [x] T040 [US4] Add AI tool validation checklist to DEPLOYMENT.md (verify resource limits, health probes, labels in AI-generated manifests)

**Checkpoint**: AI tooling workflows documented

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Documentation, validation, and deployment guide

- [x] T041 [P] Create DEPLOYMENT.md with step-by-step Minikube deployment guide (prerequisites, setup, deployment, access, troubleshooting)
- [x] T042 [P] Add troubleshooting section to DEPLOYMENT.md (pods not starting, cannot access frontend, backend/database connectivity, common errors)
- [x] T043 [P] Add resource monitoring section to DEPLOYMENT.md (kubectl top pods, resource usage validation)
- [x] T044 [P] Add update and rollback procedures to DEPLOYMENT.md (helm upgrade, helm rollback, image updates)
- [x] T045 [P] Add uninstall procedures to DEPLOYMENT.md (helm uninstall, secret cleanup, Minikube stop/delete)
- [ ] T046 Validate complete deployment workflow on clean Minikube cluster (end-to-end test: start Minikube → build images → create secrets → helm install → access frontend → verify backend API)
- [ ] T047 Validate resource consumption <2GB RAM, <2 CPU cores (kubectl top pods, verify within constraints)
- [ ] T048 Validate pod startup time <2 minutes (measure from helm install to all pods Running and Ready)
- [ ] T049 Validate deployment time <5 minutes (measure complete workflow from start to accessible application)
- [x] T050 Create quick reference commands section in DEPLOYMENT.md (status checks, logs, debug, cleanup)

**NOTE**: T041 includes comprehensive troubleshooting, monitoring, update/rollback, and uninstall procedures. T042-T045 are already covered in DEPLOYMENT.md. T046-T050 require Docker Desktop and Minikube to be running.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2 - US2)**: Depends on Setup completion - BLOCKS all other user stories
- **US1 (Phase 3)**: Depends on Foundational (US2) completion - Kubernetes deployment requires Docker images
- **US3 (Phase 4)**: Depends on US1 completion - Configuration management requires deployed application
- **US4 (Phase 5)**: No dependencies - Can be done anytime (documentation only)
- **Polish (Phase 6)**: Depends on US1 completion (minimum), ideally all user stories complete

### User Story Dependencies

- **User Story 2 (P2 - Containerization)**: FOUNDATIONAL - Blocks all other stories
- **User Story 1 (P1 - Deployment)**: Depends on US2 (needs Docker images)
- **User Story 3 (P3 - Configuration)**: Depends on US1 (needs deployed application to test)
- **User Story 4 (P4 - AI Tooling)**: Independent (documentation only)

### Within Each User Story

- **US2 (Containerization)**: Dockerfiles → Build images → Test locally → Validate
- **US1 (Deployment)**: K8s manifests → Helm chart → Validate → Dry-run
- **US3 (Configuration)**: Document → Test updates → Validate injection
- **US4 (AI Tooling)**: Document workflows → Document fallbacks → Create checklists

### Parallel Opportunities

- **Phase 1 (Setup)**: All 3 tasks can run in parallel (T001, T002, T003)
- **Phase 2 (US2)**: T004 and T005 (Dockerfiles) can run in parallel
- **Phase 3 (US1)**:
  - T011-T016 (K8s manifests) can run in parallel
  - T018-T027 (Helm templates) can run in parallel after manifests
- **Phase 4 (US3)**: T030-T032 (documentation) can run in parallel
- **Phase 5 (US4)**: T036-T038 (AI tool docs) can run in parallel
- **Phase 6 (Polish)**: T041-T045 (documentation sections) can run in parallel

---

## Parallel Example: User Story 1 (Kubernetes Deployment)

```bash
# Launch all Kubernetes manifest tasks together:
Task T011: Create backend Deployment manifest
Task T012: Create backend Service manifest
Task T013: Create frontend Deployment manifest
Task T014: Create frontend Service manifest
Task T015: Create ConfigMap manifest
Task T016: Create Secret template

# Then launch all Helm template tasks together:
Task T018: Create Chart.yaml
Task T019: Create values.yaml
Task T020: Create values-local.yaml
Task T021: Create _helpers.tpl
Task T022: Create backend Deployment template
Task T023: Create backend Service template
Task T024: Create frontend Deployment template
Task T025: Create frontend Service template
Task T026: Create ConfigMap template
Task T027: Create Secret template
```

---

## Implementation Strategy

### MVP First (User Story 2 + User Story 1 Only)

1. Complete Phase 1: Setup (T001-T003)
2. Complete Phase 2: Foundational - US2 Containerization (T004-T010)
3. Complete Phase 3: US1 Local Kubernetes Deployment (T011-T029)
4. **STOP and VALIDATE**: Test complete deployment on clean Minikube cluster
5. Deploy/demo if ready

**MVP Deliverable**: Docker images + Kubernetes deployment + Helm chart = Deployable application

### Incremental Delivery

1. Complete Setup + Foundational (US2) → Docker images ready
2. Add US1 (Deployment) → Test independently → Deploy/Demo (MVP!)
3. Add US3 (Configuration) → Test independently → Deploy/Demo
4. Add US4 (AI Tooling) → Document workflows → Deploy/Demo
5. Each story adds value without breaking previous stories

### Full Implementation

1. Complete all phases in order (Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5 → Phase 6)
2. Validate at each checkpoint
3. Final validation in Phase 6 (T046-T049)

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- **Constitution Compliance**: All tasks maintain Phase III code immutability (no changes to backend/src/ or frontend/src/)
- **AI-First Approach**: Tasks T036-T040 document AI tool usage, but manual YAML creation is acceptable with justification
- **Validation Focus**: Multiple validation tasks (T017, T028, T029, T046-T049) ensure quality and compliance

---

## Task Count Summary

- **Total Tasks**: 50
- **Phase 1 (Setup)**: 3 tasks
- **Phase 2 (US2 - Containerization)**: 7 tasks
- **Phase 3 (US1 - Deployment)**: 19 tasks
- **Phase 4 (US3 - Configuration)**: 6 tasks
- **Phase 5 (US4 - AI Tooling)**: 5 tasks
- **Phase 6 (Polish)**: 10 tasks

**Parallel Opportunities**: 28 tasks marked [P] can run in parallel within their phase

**MVP Scope**: Phase 1 + Phase 2 + Phase 3 = 29 tasks (Setup + Containerization + Deployment)

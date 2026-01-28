# Implementation Plan: Phase IV Infrastructure & Deployment

**Branch**: `003-phase-iv-infrastructure` | **Date**: 2026-01-27 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-phase-iv-infrastructure/spec.md`

## Summary

Deploy the Phase III Todo AI Chatbot application to local Kubernetes (Minikube) using containerized images, Helm charts, and AI-assisted DevOps tooling. This infrastructure-only phase packages the existing application without modifying any Phase II/III code, enabling reproducible local deployment with externalized configuration.

**Primary Requirement**: Enable developers to deploy the complete application stack (frontend, backend, database connection) to Minikube with a single Helm command, achieving pod startup within 2 minutes and consuming less than 2GB RAM total.

**Technical Approach**: Use Docker multi-stage builds for optimized images, Kubernetes Deployments with health probes and resource limits, ConfigMaps/Secrets for configuration, and Helm charts for parameterized deployment. Leverage AI tools (kubectl-ai, kagent, Claude Code) for manifest generation where possible.

## Technical Context

**Language/Version**: Infrastructure-as-Code (Docker 24+, Kubernetes 1.28+, Helm 3.12+)
**Primary Dependencies**: Docker Desktop with Kubernetes enabled OR Minikube 1.32+, kubectl 1.28+, Helm 3.12+
**Storage**: External Neon PostgreSQL (not deployed in-cluster)
**Testing**: kubectl apply --dry-run=client, helm lint, docker build validation, local container testing
**Target Platform**: Minikube (local Kubernetes cluster) on Windows/macOS/Linux development machines
**Project Type**: Infrastructure (containerization + orchestration)
**Performance Goals**: Deployment <5 min, pod startup <2 min, image builds <3 min
**Constraints**: <2GB RAM total, <2 CPU cores total, <500MB backend image, <300MB frontend image
**Scale/Scope**: Local development only, 2 services (frontend + backend), 1-2 replicas each

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Phase IV Infrastructure Gates

✅ **Phase III Code Immutability (XI)**: Plan does NOT modify any Phase II/III application code - only creates Dockerfiles, Kubernetes manifests, and Helm charts

✅ **Infrastructure-Only Scope (XII)**: Plan ONLY includes Docker, Kubernetes, Helm artifacts - no changes to `backend/src/` or `frontend/src/`

✅ **Reproducible Deployment (XIII)**: All base image versions will be pinned (python:3.12-slim, node:18-alpine), no `latest` tags, declarative Kubernetes manifests

✅ **Minikube Compatibility (XIV)**: Resources sized for local dev (500m CPU, 512Mi RAM per service), NodePort services, no cloud-specific resources

✅ **AI-Assisted DevOps (XV)**: Plan includes kubectl-ai for Deployment generation, Claude Code for Helm chart structure, kagent for troubleshooting

✅ **Container Statelessness (XVI)**: No persistent data in container filesystems - database is external, logs to stdout/stderr, configuration via environment variables

✅ **Configuration Externalized (XVII)**: All config via ConfigMaps (API URLs) and Secrets (database credentials, JWT secrets, API keys)

✅ **Secrets Management (XVIII)**: No secrets in version control - `.env.example` with placeholders, Kubernetes Secrets for runtime

✅ **AI-First YAML (XIX)**: Manual YAML only as fallback with documented justification

**Constitution Check: PASSED** - All Phase IV gates satisfied

## Project Structure

### Documentation (this feature)

```text
specs/003-phase-iv-infrastructure/
├── plan.md              # This file
├── research.md          # Phase 0: Docker/K8s/Helm best practices
├── data-model.md        # Phase 1: Infrastructure resource model
├── quickstart.md        # Phase 1: Deployment guide
└── contracts/           # Phase 1: Infrastructure contracts
    ├── docker-images.md
    ├── kubernetes-resources.md
    └── environment-variables.md
```

### Infrastructure Artifacts (repository root)

```text
# Infrastructure directory structure (NEW - Phase IV only)
k8s/
├── base/                # Base Kubernetes manifests
│   ├── backend-deployment.yaml
│   ├── backend-service.yaml
│   ├── frontend-deployment.yaml
│   ├── frontend-service.yaml
│   ├── configmap.yaml
│   └── secret-template.yaml
└── overlays/            # Environment-specific overlays (future)
    └── local/

helm/
└── habit-tracker/       # Helm chart
    ├── Chart.yaml
    ├── values.yaml
    ├── values-local.yaml
    └── templates/
        ├── backend-deployment.yaml
        ├── backend-service.yaml
        ├── frontend-deployment.yaml
        ├── frontend-service.yaml
        ├── configmap.yaml
        └── secret.yaml

# Dockerfiles (NEW - Phase IV only)
backend/
└── Dockerfile           # Multi-stage build for FastAPI

frontend/
└── Dockerfile           # Multi-stage build for Next.js

# Configuration templates (NEW - Phase IV only)
.env.example             # Updated with all K8s-required variables
DEPLOYMENT.md            # Step-by-step deployment guide

# Existing application code (IMMUTABLE - Phase II/III)
backend/src/             # NO CHANGES
frontend/src/            # NO CHANGES
```

**Structure Decision**: Infrastructure artifacts are isolated in new directories (`k8s/`, `helm/`) and Dockerfiles at application roots. Existing Phase II/III application code remains untouched, satisfying Constitution principles XI and XII.

## Complexity Tracking

> No Constitution violations - all gates passed

---

## Phase 0: Research & Best Practices

**Objective**: Resolve infrastructure unknowns and establish best practices for Docker, Kubernetes, and Helm in the context of local Minikube deployment.

### Research Tasks

1. **Docker Multi-Stage Build Patterns**
   - Research: Optimal multi-stage build for Next.js 14 (build stage + production stage)
   - Research: Optimal multi-stage build for FastAPI with Python 3.12
   - Research: Base image selection (alpine vs slim vs distroless)
   - Research: Non-root user configuration for security
   - Decision: Choose base images and build patterns that minimize size while maintaining compatibility

2. **Kubernetes Resource Limits for Minikube**
   - Research: Appropriate CPU/memory requests and limits for local development
   - Research: Health probe configurations (liveness, readiness) for FastAPI and Next.js
   - Research: Rolling update strategy parameters (maxSurge, maxUnavailable)
   - Decision: Define resource boundaries that fit within 2GB RAM / 2 CPU constraint

3. **Helm Chart Best Practices**
   - Research: Helm chart structure and templating patterns
   - Research: values.yaml organization for multi-environment support
   - Research: Secret management in Helm (external secrets vs inline)
   - Decision: Choose Helm patterns that support local development with future cloud extensibility

4. **AI DevOps Tool Capabilities**
   - Research: kubectl-ai capabilities for Deployment/Service generation
   - Research: kagent capabilities for cluster diagnostics
   - Research: Claude Code capabilities for Helm chart generation
   - Decision: Define AI tool usage workflow with manual fallback procedures

5. **Environment Variable Mapping**
   - Research: Phase III application environment variable requirements
   - Research: Kubernetes ConfigMap vs Secret classification
   - Research: Environment variable injection patterns in Kubernetes
   - Decision: Map all Phase III variables to ConfigMaps/Secrets appropriately

### Research Output

**Output**: `research.md` documenting:
- Chosen Docker base images with version pins
- Kubernetes resource limits and probe configurations
- Helm chart structure and templating approach
- AI tool usage workflow
- Environment variable mapping strategy
- Rationale for each decision
- Alternatives considered and rejected

---

## Phase 1: Infrastructure Design & Contracts

**Prerequisites**: `research.md` complete with all decisions finalized

### 1.1 Infrastructure Resource Model (`data-model.md`)

Define the infrastructure "entities" (resources) that will be created:

**Docker Images**:
- **Backend Image**: `habit-tracker-backend:v1.0.0`
  - Base: python:3.12-slim
  - Layers: dependencies, application code, non-root user
  - Exposed Port: 8000
  - Health Endpoint: /health
  - Size Target: <500MB

- **Frontend Image**: `habit-tracker-frontend:v1.0.0`
  - Base: node:18-alpine
  - Layers: dependencies, build artifacts, production server
  - Exposed Port: 3000
  - Health Endpoint: /
  - Size Target: <300MB

**Kubernetes Resources**:
- **Backend Deployment**:
  - Replicas: 1 (configurable via Helm)
  - Resource Requests: 250m CPU, 256Mi RAM
  - Resource Limits: 500m CPU, 512Mi RAM
  - Liveness Probe: HTTP GET /health every 10s
  - Readiness Probe: HTTP GET /health every 5s
  - Environment: ConfigMap + Secret injection

- **Backend Service**:
  - Type: ClusterIP
  - Port: 8000
  - Selector: app=habit-tracker-backend

- **Frontend Deployment**:
  - Replicas: 1 (configurable via Helm)
  - Resource Requests: 250m CPU, 256Mi RAM
  - Resource Limits: 500m CPU, 512Mi RAM
  - Liveness Probe: HTTP GET / every 10s
  - Readiness Probe: HTTP GET / every 5s
  - Environment: ConfigMap injection (backend URL)

- **Frontend Service**:
  - Type: NodePort
  - Port: 3000
  - NodePort: 30080 (configurable)
  - Selector: app=habit-tracker-frontend

- **ConfigMap**:
  - NEXT_PUBLIC_API_URL: http://habit-tracker-backend:8000
  - (Other non-sensitive config)

- **Secret**:
  - DATABASE_URL: (base64 encoded)
  - JWT_SECRET: (base64 encoded)
  - GEMINI_API_KEY: (base64 encoded)

**Helm Chart**:
- **Chart.yaml**: name, version, appVersion, description
- **values.yaml**: Default values for local Minikube
- **values-local.yaml**: Local development overrides
- **Templates**: Parameterized Kubernetes manifests

### 1.2 Infrastructure Contracts (`contracts/`)

**`contracts/docker-images.md`**:
- Backend image contract: base image, exposed ports, health endpoints, environment variables required
- Frontend image contract: base image, exposed ports, health endpoints, environment variables required
- Build requirements: Docker 24+, build context paths
- Image tagging strategy: semantic versioning

**`contracts/kubernetes-resources.md`**:
- Deployment contracts: replica counts, resource limits, probe configurations
- Service contracts: types, ports, selectors
- ConfigMap contract: keys and expected values
- Secret contract: keys and expected values (no actual secrets)
- Label conventions: app, component, version

**`contracts/environment-variables.md`**:
- Complete list of environment variables required by Phase III application
- Classification: ConfigMap vs Secret
- Default values for local development
- Validation rules (required vs optional)

### 1.3 Deployment Quickstart (`quickstart.md`)

Step-by-step guide for deploying to Minikube:

1. **Prerequisites Check**
   - Docker Desktop with Kubernetes enabled OR Minikube installed
   - kubectl installed and configured
   - Helm 3.12+ installed
   - Minimum 4GB RAM, 2 CPU cores available

2. **Environment Setup**
   - Start Minikube (if using Minikube)
   - Verify cluster connectivity
   - Create namespace (optional)

3. **Secret Configuration**
   - Copy `.env.example` to create Kubernetes Secret
   - Encode secrets to base64
   - Apply Secret to cluster

4. **Helm Deployment**
   - Build Docker images locally
   - Load images into Minikube (if using Minikube)
   - Install Helm chart with local values
   - Verify pod status

5. **Access Application**
   - Get frontend NodePort or start minikube tunnel
   - Access frontend URL in browser
   - Verify backend connectivity

6. **Troubleshooting**
   - Check pod logs
   - Verify ConfigMap/Secret values
   - Use kagent for diagnostics

### 1.4 Agent Context Update

Run `.specify/scripts/powershell/update-agent-context.ps1 -AgentType claude` to update agent context with Phase IV infrastructure technologies:
- Docker multi-stage builds
- Kubernetes Deployments, Services, ConfigMaps, Secrets
- Helm charts and templating
- Minikube local deployment
- kubectl-ai, kagent usage patterns

---

## Phase 2: Implementation Planning (Completed by /sp.tasks)

**Note**: Phase 2 (task generation) is handled by the `/sp.tasks` command, not `/sp.plan`.

The task list will break down implementation into:
- **Phase 1 (Setup)**: Create infrastructure directories, .env.example
- **Phase 2 (Foundational)**: Create Dockerfiles, build and test images locally
- **Phase 3 (User Story 2 - Containerization)**: Optimize images, security hardening
- **Phase 4 (User Story 1 - K8s Deployment)**: Generate Kubernetes manifests, create Helm chart
- **Phase 5 (User Story 3 - Configuration)**: Create ConfigMaps/Secrets, test environment portability
- **Phase 6 (User Story 4 - AI Tooling)**: Integrate kubectl-ai/kagent workflows
- **Phase 7 (Polish)**: Create DEPLOYMENT.md, validate full deployment, troubleshooting guide

---

## Validation Criteria

Before proceeding to `/sp.tasks`, verify:

✅ **Research Complete**: All unknowns in Technical Context resolved in research.md
✅ **Infrastructure Model Defined**: data-model.md documents all Docker images and Kubernetes resources
✅ **Contracts Documented**: contracts/ directory contains complete infrastructure contracts
✅ **Quickstart Guide Created**: quickstart.md provides step-by-step deployment instructions
✅ **Constitution Re-Check**: All Phase IV gates still satisfied after design phase
✅ **No Application Code Changes**: Plan maintains Phase III code immutability

---

## Next Steps

1. **User Review**: Review this plan for approval
2. **Generate Tasks**: Run `/sp.tasks` to create detailed task list
3. **Begin Implementation**: Execute tasks following Spec-Kit Plus workflow
4. **Validate Deployment**: Test full deployment on clean Minikube cluster
5. **Document Learnings**: Update research.md with implementation insights

# Phase IV Infrastructure Research

**Date**: 2026-01-27
**Feature**: Phase IV Infrastructure & Deployment
**Objective**: Establish best practices for Docker, Kubernetes, and Helm in local Minikube deployment context

---

## 1. Docker Multi-Stage Build Patterns

### Research Findings

**Next.js 14 Multi-Stage Build**:
- **Build Stage**: Use `node:18-alpine` for dependency installation and production build
- **Production Stage**: Use `node:18-alpine` with only production dependencies and built artifacts
- **Optimization**: Copy only `.next/standalone` and `.next/static` for minimal image size
- **Non-root User**: Create `nextjs` user with UID 1001 for security

**FastAPI Multi-Stage Build**:
- **Build Stage**: Use `python:3.12-slim` for dependency compilation
- **Production Stage**: Use `python:3.12-slim` with only runtime dependencies
- **Optimization**: Use `--no-cache-dir` and remove build tools after installation
- **Non-root User**: Create `appuser` with UID 1000 for security

### Decision: Base Images

- **Backend**: `python:3.12-slim` (Debian-based, good compatibility, ~150MB base)
- **Frontend**: `node:18-alpine` (Alpine-based, minimal size, ~120MB base)

**Rationale**:
- `slim` variants provide better compatibility than `alpine` for Python (C extensions work without musl issues)
- `alpine` is ideal for Node.js (no native dependencies in Next.js)
- Both provide security updates and are officially maintained
- Distroless rejected due to debugging complexity in local development

**Alternatives Considered**:
- `python:3.12-alpine`: Rejected due to potential issues with asyncpg and other C extensions
- `node:18-slim`: Rejected due to larger size (~180MB vs 120MB for alpine)
- Distroless images: Rejected due to lack of shell for debugging in local environment

---

## 2. Kubernetes Resource Limits for Minikube

### Research Findings

**CPU/Memory Sizing for Local Development**:
- **Backend (FastAPI)**:
  - Requests: 250m CPU, 256Mi RAM (minimum for startup)
  - Limits: 500m CPU, 512Mi RAM (allows burst for AI operations)
- **Frontend (Next.js)**:
  - Requests: 250m CPU, 256Mi RAM (minimum for SSR)
  - Limits: 500m CPU, 512Mi RAM (allows burst for initial page loads)
- **Total**: 1 CPU, 1Gi RAM (fits within 2GB/2CPU constraint with overhead)

**Health Probe Configurations**:
- **Liveness Probe**: HTTP GET, 10s interval, 3 failures = restart
  - Backend: `GET /health` or `GET /docs` (FastAPI auto-generated)
  - Frontend: `GET /` (Next.js always responds)
- **Readiness Probe**: HTTP GET, 5s interval, 3 failures = remove from service
  - Same endpoints as liveness
  - Faster interval to detect readiness quickly

**Rolling Update Strategy**:
- **maxSurge**: 1 (allow 1 extra pod during update)
- **maxUnavailable**: 0 (ensure zero downtime)
- **Rationale**: With 1 replica, maxSurge=1 ensures new pod starts before old pod terminates

### Decision: Resource Configuration

```yaml
resources:
  requests:
    cpu: 250m
    memory: 256Mi
  limits:
    cpu: 500m
    memory: 512Mi

livenessProbe:
  httpGet:
    path: /health  # or / for frontend
    port: 8000     # or 3000 for frontend
  initialDelaySeconds: 30
  periodSeconds: 10
  failureThreshold: 3

readinessProbe:
  httpGet:
    path: /health  # or / for frontend
    port: 8000     # or 3000 for frontend
  initialDelaySeconds: 10
  periodSeconds: 5
  failureThreshold: 3

strategy:
  type: RollingUpdate
  rollingUpdate:
    maxSurge: 1
    maxUnavailable: 0
```

**Rationale**: Balances resource efficiency with application needs, ensures zero-downtime updates, fits within Minikube constraints.

**Alternatives Considered**:
- Lower limits (128Mi RAM): Rejected due to potential OOMKilled errors during startup
- Higher limits (1Gi RAM): Rejected due to exceeding 2GB total constraint
- Recreate strategy: Rejected due to downtime during updates

---

## 3. Helm Chart Best Practices

### Research Findings

**Chart Structure**:
```
helm/habit-tracker/
├── Chart.yaml           # Metadata (name, version, appVersion)
├── values.yaml          # Default values (production-ready)
├── values-local.yaml    # Local development overrides
└── templates/
    ├── _helpers.tpl     # Template helpers (labels, selectors)
    ├── backend-deployment.yaml
    ├── backend-service.yaml
    ├── frontend-deployment.yaml
    ├── frontend-service.yaml
    ├── configmap.yaml
    └── secret.yaml
```

**values.yaml Organization**:
- Group by component (backend, frontend, database)
- Separate image configuration (repository, tag, pullPolicy)
- Separate resource configuration (requests, limits)
- Separate service configuration (type, port, nodePort)
- Use nested structure for clarity

**Secret Management**:
- **External Secrets**: Use Kubernetes Secret created manually (not in Helm chart)
- **Helm Chart**: Reference existing Secret by name
- **Rationale**: Secrets should not be in version control, even templated

### Decision: Helm Chart Approach

**Chart.yaml**:
```yaml
apiVersion: v2
name: habit-tracker
version: 1.0.0
appVersion: "1.0.0"
description: Habit Tracker with AI Chatbot - Local Kubernetes Deployment
```

**values.yaml Structure**:
```yaml
backend:
  image:
    repository: habit-tracker-backend
    tag: v1.0.0
    pullPolicy: IfNotPresent
  replicas: 1
  resources:
    requests: {cpu: 250m, memory: 256Mi}
    limits: {cpu: 500m, memory: 512Mi}
  service:
    type: ClusterIP
    port: 8000

frontend:
  image:
    repository: habit-tracker-frontend
    tag: v1.0.0
    pullPolicy: IfNotPresent
  replicas: 1
  resources:
    requests: {cpu: 250m, memory: 256Mi}
    limits: {cpu: 500m, memory: 512Mi}
  service:
    type: NodePort
    port: 3000
    nodePort: 30080

config:
  backendUrl: http://habit-tracker-backend:8000

secrets:
  existingSecret: habit-tracker-secrets
```

**Rationale**: Clear separation of concerns, easy to override for different environments, secrets managed externally.

**Alternatives Considered**:
- Inline secrets in Helm: Rejected due to security risk
- Sealed Secrets: Rejected as overkill for local development
- Single values file: Rejected due to lack of environment separation

---

## 4. AI DevOps Tool Capabilities

### Research Findings

**kubectl-ai**:
- **Capabilities**: Generate Kubernetes manifests from natural language prompts
- **Usage**: `kubectl-ai "create deployment for fastapi app with 1 replica"`
- **Limitations**: May not include all best practices (resource limits, probes)
- **Validation**: Always validate with `kubectl apply --dry-run=client`

**kagent**:
- **Capabilities**: Diagnose cluster issues, analyze pod logs, suggest fixes
- **Usage**: `kagent diagnose pod <pod-name>`
- **Limitations**: Requires cluster access, may not understand application-specific issues
- **Use Cases**: Pod crashes, resource exhaustion, networking issues

**Claude Code**:
- **Capabilities**: Generate Helm chart structure, Dockerfiles, documentation
- **Usage**: Conversational prompts for infrastructure generation
- **Limitations**: Requires human review and validation
- **Use Cases**: Complex multi-file generation, best practices application

### Decision: AI Tool Workflow

1. **Dockerfile Generation**: Use Claude Code for initial Dockerfiles, validate with `docker build`
2. **Kubernetes Manifest Generation**: Use kubectl-ai for basic manifests, enhance manually with resource limits and probes
3. **Helm Chart Generation**: Use Claude Code for chart structure, customize templates manually
4. **Troubleshooting**: Use kagent for cluster diagnostics, supplement with `kubectl logs` and `kubectl describe`
5. **Fallback**: If AI tools fail, write YAML manually and document failure reason

**Rationale**: AI tools accelerate initial generation but require human validation for production-readiness.

**Alternatives Considered**:
- Manual YAML only: Rejected due to slower development and higher error rate
- AI-only without validation: Rejected due to potential for missing best practices

---

## 5. Environment Variable Mapping

### Research Findings

**Phase III Application Requirements** (from existing .env files):
- `DATABASE_URL`: PostgreSQL connection string (SECRET)
- `JWT_SECRET` / `JWT_ALGORITHM`: Authentication secrets (SECRET)
- `GEMINI_API_KEY`: AI model API key (SECRET)
- `NEXT_PUBLIC_API_URL`: Backend API URL (CONFIGMAP)

**ConfigMap vs Secret Classification**:
- **ConfigMap**: Non-sensitive configuration (URLs, feature flags, timeouts)
- **Secret**: Sensitive data (credentials, API keys, tokens)
- **Rule**: If exposure causes security risk, use Secret

### Decision: Environment Variable Mapping

**ConfigMap** (`habit-tracker-config`):
```yaml
NEXT_PUBLIC_API_URL: "http://habit-tracker-backend:8000"
# Future: Add feature flags, timeouts, etc.
```

**Secret** (`habit-tracker-secrets`):
```yaml
DATABASE_URL: <base64-encoded>
JWT_SECRET: <base64-encoded>
JWT_ALGORITHM: <base64-encoded>
GEMINI_API_KEY: <base64-encoded>
```

**Injection Pattern**:
```yaml
envFrom:
  - configMapRef:
      name: habit-tracker-config
  - secretRef:
      name: habit-tracker-secrets
```

**Rationale**: Simple injection pattern, clear separation of sensitive vs non-sensitive data, easy to update independently.

**Alternatives Considered**:
- Individual env vars: Rejected due to verbosity
- Mounted files: Rejected due to application expecting environment variables
- External secret managers: Rejected as overkill for local development

---

## Summary of Decisions

| Decision Area | Choice | Rationale |
|---------------|--------|-----------|
| Backend Base Image | python:3.12-slim | Best compatibility for C extensions, security updates |
| Frontend Base Image | node:18-alpine | Minimal size, sufficient for Next.js |
| CPU/Memory Limits | 500m CPU, 512Mi RAM per service | Fits 2GB/2CPU constraint, allows burst |
| Health Probes | HTTP GET every 10s (liveness), 5s (readiness) | Fast detection, zero downtime |
| Helm Chart Structure | Separate values files per environment | Clear separation, easy overrides |
| Secret Management | External Kubernetes Secret | Security best practice, no secrets in Git |
| AI Tool Usage | kubectl-ai + Claude Code with validation | Accelerates development, ensures quality |
| Environment Variables | ConfigMap (non-sensitive) + Secret (sensitive) | Clear classification, simple injection |

---

## Implementation Notes

- All Docker images will use non-root users (UID 1000/1001)
- All Kubernetes manifests will include proper labels (app, component, version)
- All Helm templates will use `_helpers.tpl` for consistent label generation
- All AI-generated artifacts will be validated before committing
- Manual YAML will include comments explaining why AI generation failed

# Phase IV Infrastructure Resource Model

**Date**: 2026-01-27
**Feature**: Phase IV Infrastructure & Deployment
**Purpose**: Define all infrastructure resources (Docker images, Kubernetes objects, Helm charts) that will be created

---

## Docker Images

### Backend Image: `habit-tracker-backend:v1.0.0`

**Purpose**: Containerized FastAPI application with Python dependencies

**Specifications**:
- **Base Image**: `python:3.12-slim` (pinned version)
- **Build Context**: `backend/` directory
- **Exposed Port**: 8000
- **Health Endpoint**: `/health` or `/docs`
- **Size Target**: <500MB
- **User**: Non-root user `appuser` (UID 1000)

**Layers**:
1. Base image (python:3.12-slim)
2. System dependencies (if needed)
3. Python dependencies (from requirements.txt)
4. Application code (backend/src/)
5. Non-root user creation
6. Working directory and permissions

**Environment Variables Required**:
- `DATABASE_URL` (from Secret)
- `JWT_SECRET` (from Secret)
- `JWT_ALGORITHM` (from Secret)
- `GEMINI_API_KEY` (from Secret)

**Build Validation**:
- Image builds without errors
- Image size <500MB
- No secrets embedded in layers
- Application starts and responds to health checks

---

### Frontend Image: `habit-tracker-frontend:v1.0.0`

**Purpose**: Containerized Next.js application with Node.js dependencies

**Specifications**:
- **Base Image**: `node:18-alpine` (pinned version)
- **Build Context**: `frontend/` directory
- **Exposed Port**: 3000
- **Health Endpoint**: `/`
- **Size Target**: <300MB
- **User**: Non-root user `nextjs` (UID 1001)

**Layers**:
1. Base image (node:18-alpine)
2. Build stage: Install dependencies, build Next.js
3. Production stage: Copy built artifacts (.next/standalone, .next/static)
4. Non-root user creation
5. Working directory and permissions

**Environment Variables Required**:
- `NEXT_PUBLIC_API_URL` (from ConfigMap)

**Build Validation**:
- Image builds without errors
- Image size <300MB
- No secrets embedded in layers
- Application starts and serves pages

---

## Kubernetes Resources

### Backend Deployment: `habit-tracker-backend`

**Purpose**: Manage backend pod lifecycle with desired state

**Specifications**:
- **API Version**: apps/v1
- **Kind**: Deployment
- **Replicas**: 1 (configurable via Helm)
- **Selector**: `app: habit-tracker-backend`
- **Labels**:
  - `app: habit-tracker-backend`
  - `component: backend`
  - `version: v1.0.0`

**Pod Template**:
- **Container Name**: backend
- **Image**: habit-tracker-backend:v1.0.0
- **Image Pull Policy**: IfNotPresent
- **Port**: 8000
- **Resources**:
  - Requests: 250m CPU, 256Mi RAM
  - Limits: 500m CPU, 512Mi RAM
- **Liveness Probe**: HTTP GET /health, 10s interval, 30s initial delay
- **Readiness Probe**: HTTP GET /health, 5s interval, 10s initial delay
- **Environment**: From ConfigMap + Secret

**Update Strategy**:
- Type: RollingUpdate
- Max Surge: 1
- Max Unavailable: 0

---

### Backend Service: `habit-tracker-backend`

**Purpose**: Provide stable network endpoint for backend pods

**Specifications**:
- **API Version**: v1
- **Kind**: Service
- **Type**: ClusterIP (internal only)
- **Selector**: `app: habit-tracker-backend`
- **Port**: 8000
- **Target Port**: 8000
- **Protocol**: TCP

**DNS Name**: `habit-tracker-backend.default.svc.cluster.local` (or custom namespace)

---

### Frontend Deployment: `habit-tracker-frontend`

**Purpose**: Manage frontend pod lifecycle with desired state

**Specifications**:
- **API Version**: apps/v1
- **Kind**: Deployment
- **Replicas**: 1 (configurable via Helm)
- **Selector**: `app: habit-tracker-frontend`
- **Labels**:
  - `app: habit-tracker-frontend`
  - `component: frontend`
  - `version: v1.0.0`

**Pod Template**:
- **Container Name**: frontend
- **Image**: habit-tracker-frontend:v1.0.0
- **Image Pull Policy**: IfNotPresent
- **Port**: 3000
- **Resources**:
  - Requests: 250m CPU, 256Mi RAM
  - Limits: 500m CPU, 512Mi RAM
- **Liveness Probe**: HTTP GET /, 10s interval, 30s initial delay
- **Readiness Probe**: HTTP GET /, 5s interval, 10s initial delay
- **Environment**: From ConfigMap

**Update Strategy**:
- Type: RollingUpdate
- Max Surge: 1
- Max Unavailable: 0

---

### Frontend Service: `habit-tracker-frontend`

**Purpose**: Provide external access to frontend pods

**Specifications**:
- **API Version**: v1
- **Kind**: Service
- **Type**: NodePort (for Minikube access)
- **Selector**: `app: habit-tracker-frontend`
- **Port**: 3000
- **Target Port**: 3000
- **Node Port**: 30080 (configurable)
- **Protocol**: TCP

**Access Methods**:
- NodePort: `http://<minikube-ip>:30080`
- Minikube Tunnel: `http://localhost:3000` (requires `minikube tunnel`)

---

### ConfigMap: `habit-tracker-config`

**Purpose**: Store non-sensitive configuration

**Specifications**:
- **API Version**: v1
- **Kind**: ConfigMap
- **Data**:
  - `NEXT_PUBLIC_API_URL`: `http://habit-tracker-backend:8000`
  - (Future: Add feature flags, timeouts, etc.)

**Usage**: Injected into frontend pods via `envFrom`

---

### Secret: `habit-tracker-secrets`

**Purpose**: Store sensitive configuration (credentials, API keys)

**Specifications**:
- **API Version**: v1
- **Kind**: Secret
- **Type**: Opaque
- **Data** (base64 encoded):
  - `DATABASE_URL`: PostgreSQL connection string
  - `JWT_SECRET`: JWT signing secret
  - `JWT_ALGORITHM`: JWT algorithm (e.g., HS256)
  - `GEMINI_API_KEY`: Gemini AI API key

**Creation**: Manual creation via kubectl or from .env file
**Usage**: Injected into backend pods via `envFrom`

**Security Notes**:
- Never commit actual secrets to version control
- Use `.env.example` with placeholder values
- Document secret creation process in quickstart.md

---

## Helm Chart: `habit-tracker`

**Purpose**: Package all Kubernetes resources with parameterization

**Specifications**:
- **Chart Name**: habit-tracker
- **Chart Version**: 1.0.0
- **App Version**: 1.0.0
- **Description**: Habit Tracker with AI Chatbot - Local Kubernetes Deployment

**Files**:
- `Chart.yaml`: Metadata
- `values.yaml`: Default values (production-ready)
- `values-local.yaml`: Local development overrides
- `templates/_helpers.tpl`: Template helpers (labels, selectors)
- `templates/backend-deployment.yaml`: Backend Deployment template
- `templates/backend-service.yaml`: Backend Service template
- `templates/frontend-deployment.yaml`: Frontend Deployment template
- `templates/frontend-service.yaml`: Frontend Service template
- `templates/configmap.yaml`: ConfigMap template
- `templates/secret.yaml`: Secret template (references existing Secret)

**Parameterization**:
- Image repositories and tags
- Replica counts
- Resource limits
- Service types and ports
- ConfigMap values
- Secret name reference

**Installation**:
```bash
helm install habit-tracker ./helm/habit-tracker -f ./helm/habit-tracker/values-local.yaml
```

**Upgrade**:
```bash
helm upgrade habit-tracker ./helm/habit-tracker -f ./helm/habit-tracker/values-local.yaml
```

**Uninstall**:
```bash
helm uninstall habit-tracker
```

---

## Resource Relationships

```
┌─────────────────────────────────────────────────────────────┐
│                     Minikube Cluster                        │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Namespace: default                      │  │
│  │                                                      │  │
│  │  ┌────────────────────┐    ┌────────────────────┐  │  │
│  │  │  ConfigMap         │    │  Secret            │  │  │
│  │  │  habit-tracker-    │    │  habit-tracker-    │  │  │
│  │  │  config            │    │  secrets           │  │  │
│  │  └────────────────────┘    └────────────────────┘  │  │
│  │           │                          │              │  │
│  │           │ envFrom                  │ envFrom      │  │
│  │           ▼                          ▼              │  │
│  │  ┌────────────────────┐    ┌────────────────────┐  │  │
│  │  │  Frontend          │    │  Backend           │  │  │
│  │  │  Deployment        │    │  Deployment        │  │  │
│  │  │  (1 replica)       │    │  (1 replica)       │  │  │
│  │  └────────────────────┘    └────────────────────┘  │  │
│  │           │                          │              │  │
│  │           │ manages                  │ manages      │  │
│  │           ▼                          ▼              │  │
│  │  ┌────────────────────┐    ┌────────────────────┐  │  │
│  │  │  Frontend Pod      │    │  Backend Pod       │  │  │
│  │  │  (port 3000)       │    │  (port 8000)       │  │  │
│  │  └────────────────────┘    └────────────────────┘  │  │
│  │           │                          │              │  │
│  │           │ selected by              │ selected by  │  │
│  │           ▼                          ▼              │  │
│  │  ┌────────────────────┐    ┌────────────────────┐  │  │
│  │  │  Frontend Service  │    │  Backend Service   │  │  │
│  │  │  (NodePort 30080)  │    │  (ClusterIP 8000)  │  │  │
│  │  └────────────────────┘    └────────────────────┘  │  │
│  │           │                          ▲              │  │
│  └───────────┼──────────────────────────┼──────────────┘  │
│              │                          │                 │
└──────────────┼──────────────────────────┼─────────────────┘
               │                          │
               │ External Access          │ Internal Access
               │ (NodePort/Tunnel)        │ (ClusterIP)
               ▼                          │
         ┌──────────┐                     │
         │  Browser │─────────────────────┘
         │  (User)  │   API Calls
         └──────────┘
```

---

## Resource Sizing Summary

| Resource | CPU Request | CPU Limit | RAM Request | RAM Limit | Replicas | Total CPU | Total RAM |
|----------|-------------|-----------|-------------|-----------|----------|-----------|-----------|
| Backend  | 250m        | 500m      | 256Mi       | 512Mi     | 1        | 250m      | 256Mi     |
| Frontend | 250m        | 500m      | 256Mi       | 512Mi     | 1        | 250m      | 256Mi     |
| **Total**| **500m**    | **1000m** | **512Mi**   | **1024Mi**| **2**    | **500m**  | **512Mi** |

**Constraint Validation**: ✅ Fits within 2GB RAM / 2 CPU cores (with overhead for Kubernetes system components)

---

## Validation Checklist

Before implementation, verify:

- [ ] All Docker images have pinned base image versions
- [ ] All Docker images run as non-root users
- [ ] All Kubernetes resources have proper labels
- [ ] All Deployments have resource requests and limits
- [ ] All Deployments have liveness and readiness probes
- [ ] All Services have correct selectors
- [ ] ConfigMap contains only non-sensitive data
- [ ] Secret creation is documented (not in version control)
- [ ] Helm chart templates use proper parameterization
- [ ] Total resource usage fits within Minikube constraints

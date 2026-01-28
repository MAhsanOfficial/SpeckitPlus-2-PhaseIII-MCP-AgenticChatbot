# Kubernetes Resources Contract

**Date**: 2026-01-27
**Feature**: Phase IV Infrastructure & Deployment
**Purpose**: Define the contract for Kubernetes resources (specifications, behavior, relationships)

---

## Deployment Contracts

### Backend Deployment: `habit-tracker-backend`

**API Version**: `apps/v1`
**Kind**: `Deployment`

**Metadata**:
- **Name**: `habit-tracker-backend`
- **Labels**:
  - `app: habit-tracker-backend`
  - `component: backend`
  - `version: v1.0.0`

**Spec**:
- **Replicas**: 1 (configurable via Helm: `backend.replicas`)
- **Selector**: `matchLabels: {app: habit-tracker-backend}`
- **Strategy**:
  - Type: `RollingUpdate`
  - `maxSurge: 1`
  - `maxUnavailable: 0`

**Pod Template**:
- **Labels**: Same as Deployment labels
- **Container**:
  - Name: `backend`
  - Image: `habit-tracker-backend:v1.0.0` (configurable via Helm)
  - ImagePullPolicy: `IfNotPresent`
  - Ports: `containerPort: 8000`
  - Resources:
    - Requests: `cpu: 250m, memory: 256Mi`
    - Limits: `cpu: 500m, memory: 512Mi`
  - LivenessProbe:
    - `httpGet: {path: /health, port: 8000}`
    - `initialDelaySeconds: 30`
    - `periodSeconds: 10`
    - `failureThreshold: 3`
  - ReadinessProbe:
    - `httpGet: {path: /health, port: 8000}`
    - `initialDelaySeconds: 10`
    - `periodSeconds: 5`
    - `failureThreshold: 3`
  - EnvFrom:
    - `configMapRef: {name: habit-tracker-config}`
    - `secretRef: {name: habit-tracker-secrets}`

**Behavior**:
- Maintains 1 running pod at all times
- Restarts pod if liveness probe fails 3 times
- Removes pod from service if readiness probe fails 3 times
- Rolling updates ensure zero downtime (new pod starts before old pod terminates)

---

### Frontend Deployment: `habit-tracker-frontend`

**API Version**: `apps/v1`
**Kind**: `Deployment`

**Metadata**:
- **Name**: `habit-tracker-frontend`
- **Labels**:
  - `app: habit-tracker-frontend`
  - `component: frontend`
  - `version: v1.0.0`

**Spec**:
- **Replicas**: 1 (configurable via Helm: `frontend.replicas`)
- **Selector**: `matchLabels: {app: habit-tracker-frontend}`
- **Strategy**:
  - Type: `RollingUpdate`
  - `maxSurge: 1`
  - `maxUnavailable: 0`

**Pod Template**:
- **Labels**: Same as Deployment labels
- **Container**:
  - Name: `frontend`
  - Image: `habit-tracker-frontend:v1.0.0` (configurable via Helm)
  - ImagePullPolicy: `IfNotPresent`
  - Ports: `containerPort: 3000`
  - Resources:
    - Requests: `cpu: 250m, memory: 256Mi`
    - Limits: `cpu: 500m, memory: 512Mi`
  - LivenessProbe:
    - `httpGet: {path: /, port: 3000}`
    - `initialDelaySeconds: 30`
    - `periodSeconds: 10`
    - `failureThreshold: 3`
  - ReadinessProbe:
    - `httpGet: {path: /, port: 3000}`
    - `initialDelaySeconds: 10`
    - `periodSeconds: 5`
    - `failureThreshold: 3`
  - EnvFrom:
    - `configMapRef: {name: habit-tracker-config}`

**Behavior**:
- Maintains 1 running pod at all times
- Restarts pod if liveness probe fails 3 times
- Removes pod from service if readiness probe fails 3 times
- Rolling updates ensure zero downtime

---

## Service Contracts

### Backend Service: `habit-tracker-backend`

**API Version**: `v1`
**Kind**: `Service`

**Metadata**:
- **Name**: `habit-tracker-backend`
- **Labels**:
  - `app: habit-tracker-backend`
  - `component: backend`

**Spec**:
- **Type**: `ClusterIP` (internal only)
- **Selector**: `app: habit-tracker-backend`
- **Ports**:
  - Name: `http`
  - Protocol: `TCP`
  - Port: `8000`
  - TargetPort: `8000`

**Behavior**:
- Provides stable internal DNS name: `habit-tracker-backend.default.svc.cluster.local`
- Routes traffic to pods matching selector
- Load balances across multiple pods (if replicas > 1)
- Only accessible within cluster (ClusterIP)

**Access**:
- From frontend: `http://habit-tracker-backend:8000`
- From other pods: `http://habit-tracker-backend.default.svc.cluster.local:8000`

---

### Frontend Service: `habit-tracker-frontend`

**API Version**: `v1`
**Kind**: `Service`

**Metadata**:
- **Name**: `habit-tracker-frontend`
- **Labels**:
  - `app: habit-tracker-frontend`
  - `component: frontend`

**Spec**:
- **Type**: `NodePort` (external access)
- **Selector**: `app: habit-tracker-frontend`
- **Ports**:
  - Name: `http`
  - Protocol: `TCP`
  - Port: `3000`
  - TargetPort: `3000`
  - NodePort: `30080` (configurable via Helm: `frontend.service.nodePort`)

**Behavior**:
- Provides stable internal DNS name: `habit-tracker-frontend.default.svc.cluster.local`
- Routes traffic to pods matching selector
- Exposes service on all nodes at port 30080
- Accessible from outside cluster via NodePort

**Access**:
- NodePort: `http://<minikube-ip>:30080`
- Minikube Tunnel: `http://localhost:3000` (requires `minikube tunnel`)
- Internal: `http://habit-tracker-frontend:3000`

---

## ConfigMap Contract

### ConfigMap: `habit-tracker-config`

**API Version**: `v1`
**Kind**: `ConfigMap`

**Metadata**:
- **Name**: `habit-tracker-config`
- **Labels**:
  - `app: habit-tracker`
  - `component: config`

**Data**:
| Key | Value | Description |
|-----|-------|-------------|
| `NEXT_PUBLIC_API_URL` | `http://habit-tracker-backend:8000` | Backend API URL for frontend |

**Behavior**:
- Injected into pods via `envFrom.configMapRef`
- Updates require pod restart to take effect
- Non-sensitive data only

**Usage**:
```yaml
envFrom:
  - configMapRef:
      name: habit-tracker-config
```

---

## Secret Contract

### Secret: `habit-tracker-secrets`

**API Version**: `v1`
**Kind**: `Secret`
**Type**: `Opaque`

**Metadata**:
- **Name**: `habit-tracker-secrets`
- **Labels**:
  - `app: habit-tracker`
  - `component: secrets`

**Data** (base64 encoded):
| Key | Description | Example (plaintext) |
|-----|-------------|---------------------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host:5432/db` |
| `JWT_SECRET` | JWT signing secret | `your-secret-key-here` |
| `JWT_ALGORITHM` | JWT algorithm | `HS256` |
| `GEMINI_API_KEY` | Gemini AI API key | `your-api-key-here` |

**Behavior**:
- Injected into backend pods via `envFrom.secretRef`
- Updates require pod restart to take effect
- Sensitive data only
- Never committed to version control

**Creation**:
```bash
kubectl create secret generic habit-tracker-secrets \
  --from-literal=DATABASE_URL="postgresql://..." \
  --from-literal=JWT_SECRET="..." \
  --from-literal=JWT_ALGORITHM="HS256" \
  --from-literal=GEMINI_API_KEY="..."
```

**Usage**:
```yaml
envFrom:
  - secretRef:
      name: habit-tracker-secrets
```

---

## Label Conventions

### Standard Labels
All resources MUST include these labels:

| Label | Description | Example |
|-------|-------------|---------|
| `app` | Application name | `habit-tracker-backend`, `habit-tracker-frontend` |
| `component` | Component type | `backend`, `frontend`, `config`, `secrets` |
| `version` | Application version | `v1.0.0` |

### Selector Labels
Deployments and Services MUST use consistent selectors:

- Backend: `app: habit-tracker-backend`
- Frontend: `app: habit-tracker-frontend`

---

## Resource Limits Summary

| Resource | CPU Request | CPU Limit | Memory Request | Memory Limit |
|----------|-------------|-----------|----------------|--------------|
| Backend Pod | 250m | 500m | 256Mi | 512Mi |
| Frontend Pod | 250m | 500m | 256Mi | 512Mi |
| **Total (1 replica each)** | **500m** | **1000m** | **512Mi** | **1024Mi** |

**Constraint Validation**: ✅ Fits within 2GB RAM / 2 CPU cores

---

## Health Probe Specifications

### Liveness Probe
- **Purpose**: Detect if container is alive (restart if dead)
- **Mechanism**: HTTP GET request
- **Initial Delay**: 30 seconds (allow startup time)
- **Period**: 10 seconds (check every 10s)
- **Failure Threshold**: 3 (restart after 3 consecutive failures)

### Readiness Probe
- **Purpose**: Detect if container is ready to serve traffic
- **Mechanism**: HTTP GET request
- **Initial Delay**: 10 seconds (faster than liveness)
- **Period**: 5 seconds (check every 5s)
- **Failure Threshold**: 3 (remove from service after 3 consecutive failures)

---

## Validation Commands

### Check Deployments
```bash
kubectl get deployments
kubectl describe deployment habit-tracker-backend
kubectl describe deployment habit-tracker-frontend
```

### Check Pods
```bash
kubectl get pods
kubectl describe pod <pod-name>
kubectl logs <pod-name>
```

### Check Services
```bash
kubectl get services
kubectl describe service habit-tracker-backend
kubectl describe service habit-tracker-frontend
```

### Check ConfigMap
```bash
kubectl get configmap habit-tracker-config -o yaml
```

### Check Secret
```bash
kubectl get secret habit-tracker-secrets -o yaml
# Note: Values are base64 encoded
```

### Test Service Connectivity
```bash
# From within cluster
kubectl run -it --rm debug --image=alpine --restart=Never -- sh
wget -O- http://habit-tracker-backend:8000/health
wget -O- http://habit-tracker-frontend:3000/

# From outside cluster (NodePort)
curl http://$(minikube ip):30080
```

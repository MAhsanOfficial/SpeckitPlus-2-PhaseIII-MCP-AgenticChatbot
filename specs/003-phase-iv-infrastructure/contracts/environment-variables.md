# Environment Variables Contract

**Date**: 2026-01-27
**Feature**: Phase IV Infrastructure & Deployment
**Purpose**: Define all environment variables required by the application and their Kubernetes mapping

---

## Environment Variable Classification

### ConfigMap Variables (Non-Sensitive)
Environment variables that can be stored in plain text ConfigMaps.

| Variable | Value | Description | Required | Component |
|----------|-------|-------------|----------|-----------|
| `NEXT_PUBLIC_API_URL` | `http://habit-tracker-backend:8000` | Backend API URL for frontend | Yes | Frontend |

### Secret Variables (Sensitive)
Environment variables that must be stored in Kubernetes Secrets (base64 encoded).

| Variable | Example Value | Description | Required | Component |
|----------|---------------|-------------|----------|-----------|
| `DATABASE_URL` | `postgresql://user:pass@host:5432/db` | PostgreSQL connection string | Yes | Backend |
| `JWT_SECRET` | `your-secret-key-here` | JWT signing secret | Yes | Backend |
| `JWT_ALGORITHM` | `HS256` | JWT algorithm | Yes | Backend |
| `GEMINI_API_KEY` | `your-api-key-here` | Gemini AI API key | Yes | Backend |

---

## Phase III Application Requirements

### Backend Environment Variables

**From `backend/.env`**:
```env
DATABASE_URL=postgresql://neondb_owner:npg_xxx@ep-xxx.aws.neon.tech/neondb?sslmode=require
JWT_ALGORITHM=a9f3c1e8b24f7d9c2e1f0b8a9d4c6e7f1234567890abcdef1234567890abcd
GEMINI_API_KEY=your-gemini-api-key-here
```

**Mapping to Kubernetes**:
- `DATABASE_URL` → Secret (`habit-tracker-secrets`)
- `JWT_ALGORITHM` → Secret (`habit-tracker-secrets`) [Note: This appears to be JWT_SECRET based on value]
- `GEMINI_API_KEY` → Secret (`habit-tracker-secrets`)

**Additional Variables** (from Phase III code analysis):
- `JWT_SECRET` → Secret (if different from JWT_ALGORITHM)

### Frontend Environment Variables

**From `frontend/.env`**:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Mapping to Kubernetes**:
- `NEXT_PUBLIC_API_URL` → ConfigMap (`habit-tracker-config`)
- **Value Change**: `http://localhost:8000` → `http://habit-tracker-backend:8000` (Kubernetes service DNS)

---

## Kubernetes Resource Mapping

### ConfigMap: `habit-tracker-config`

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: habit-tracker-config
data:
  NEXT_PUBLIC_API_URL: "http://habit-tracker-backend:8000"
```

**Injection**:
```yaml
envFrom:
  - configMapRef:
      name: habit-tracker-config
```

### Secret: `habit-tracker-secrets`

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: habit-tracker-secrets
type: Opaque
data:
  DATABASE_URL: <base64-encoded-value>
  JWT_SECRET: <base64-encoded-value>
  JWT_ALGORITHM: <base64-encoded-value>
  GEMINI_API_KEY: <base64-encoded-value>
```

**Injection**:
```yaml
envFrom:
  - secretRef:
      name: habit-tracker-secrets
```

---

## Environment Variable Validation Rules

### Required Variables
All variables marked as "Required: Yes" MUST be present for the application to start.

**Backend Required**:
- `DATABASE_URL`
- `JWT_SECRET` (or `JWT_ALGORITHM` if that's the actual secret)
- `GEMINI_API_KEY`

**Frontend Required**:
- `NEXT_PUBLIC_API_URL`

### Optional Variables
None currently defined. Future additions should be documented here.

### Validation at Startup
- Backend: FastAPI will fail to start if database connection fails
- Frontend: Next.js will build with missing `NEXT_PUBLIC_API_URL` but API calls will fail

---

## Default Values for Local Development

### ConfigMap Defaults (values-local.yaml)
```yaml
config:
  backendUrl: "http://habit-tracker-backend:8000"
```

### Secret Defaults (.env.example)
```env
# Database Configuration
DATABASE_URL=postgresql://user:password@host:5432/database?sslmode=require

# JWT Configuration
JWT_SECRET=your-jwt-secret-key-here-minimum-32-characters
JWT_ALGORITHM=HS256

# AI Configuration
GEMINI_API_KEY=your-gemini-api-key-here
```

**Note**: These are placeholder values. Actual secrets must be provided by developers.

---

## Secret Creation Guide

### From .env File
```bash
# Create Secret from .env file
kubectl create secret generic habit-tracker-secrets \
  --from-env-file=backend/.env
```

### From Literal Values
```bash
# Create Secret from individual values
kubectl create secret generic habit-tracker-secrets \
  --from-literal=DATABASE_URL="postgresql://user:pass@host:5432/db" \
  --from-literal=JWT_SECRET="your-secret-key" \
  --from-literal=JWT_ALGORITHM="HS256" \
  --from-literal=GEMINI_API_KEY="your-api-key"
```

### Verify Secret Creation
```bash
# Check Secret exists
kubectl get secret habit-tracker-secrets

# View Secret (base64 encoded)
kubectl get secret habit-tracker-secrets -o yaml

# Decode Secret values (for verification only)
kubectl get secret habit-tracker-secrets -o jsonpath='{.data.DATABASE_URL}' | base64 --decode
```

---

## Environment Variable Injection Pattern

### Backend Deployment
```yaml
spec:
  template:
    spec:
      containers:
      - name: backend
        image: habit-tracker-backend:v1.0.0
        envFrom:
        - configMapRef:
            name: habit-tracker-config
        - secretRef:
            name: habit-tracker-secrets
```

**Result**: All ConfigMap and Secret keys become environment variables in the container.

### Frontend Deployment
```yaml
spec:
  template:
    spec:
      containers:
      - name: frontend
        image: habit-tracker-frontend:v1.0.0
        envFrom:
        - configMapRef:
            name: habit-tracker-config
```

**Result**: Only ConfigMap keys become environment variables (frontend doesn't need secrets).

---

## Troubleshooting Environment Variables

### Check Pod Environment Variables
```bash
# List all environment variables in a pod
kubectl exec <pod-name> -- env

# Check specific variable
kubectl exec <pod-name> -- env | grep DATABASE_URL
```

### Verify ConfigMap Values
```bash
# View ConfigMap
kubectl get configmap habit-tracker-config -o yaml

# Check if ConfigMap is mounted
kubectl describe pod <pod-name> | grep -A 5 "Environment"
```

### Verify Secret Values
```bash
# View Secret (base64 encoded)
kubectl get secret habit-tracker-secrets -o yaml

# Decode specific secret
kubectl get secret habit-tracker-secrets -o jsonpath='{.data.DATABASE_URL}' | base64 --decode
```

### Common Issues

**Issue**: Pod fails to start with "Secret not found"
**Solution**: Create the Secret before deploying the application
```bash
kubectl create secret generic habit-tracker-secrets --from-env-file=backend/.env
```

**Issue**: Frontend cannot connect to backend
**Solution**: Verify `NEXT_PUBLIC_API_URL` points to Kubernetes service DNS
```bash
kubectl get configmap habit-tracker-config -o yaml
# Should show: NEXT_PUBLIC_API_URL: "http://habit-tracker-backend:8000"
```

**Issue**: Backend cannot connect to database
**Solution**: Verify `DATABASE_URL` is correct and database is accessible
```bash
kubectl exec <backend-pod> -- env | grep DATABASE_URL
# Test connection from pod
kubectl exec <backend-pod> -- python -c "import asyncpg; print('OK')"
```

---

## Security Best Practices

### Never Commit Secrets
- ✅ Commit: `.env.example` with placeholder values
- ❌ Never commit: `.env` with actual secrets
- ❌ Never commit: Kubernetes Secret YAML with actual values

### Secret Rotation
To rotate secrets:
1. Update Secret values: `kubectl edit secret habit-tracker-secrets`
2. Restart pods to pick up new values: `kubectl rollout restart deployment habit-tracker-backend`

### Access Control
- Limit Secret access using RBAC
- Use namespace isolation for multi-tenant deployments
- Consider external secret managers (Sealed Secrets, External Secrets Operator) for production

---

## Validation Checklist

Before deployment, verify:

- [ ] `.env.example` exists with all required variables documented
- [ ] Actual `.env` file is in `.gitignore`
- [ ] ConfigMap created with correct values
- [ ] Secret created with actual credentials (not placeholders)
- [ ] Backend Deployment references both ConfigMap and Secret
- [ ] Frontend Deployment references only ConfigMap
- [ ] `NEXT_PUBLIC_API_URL` uses Kubernetes service DNS (not localhost)
- [ ] All required variables are present (no missing keys)

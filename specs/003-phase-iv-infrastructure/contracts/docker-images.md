# Docker Images Contract

**Date**: 2026-01-27
**Feature**: Phase IV Infrastructure & Deployment
**Purpose**: Define the contract for Docker images (inputs, outputs, behavior)

---

## Backend Image Contract

### Image Identifier
- **Repository**: `habit-tracker-backend`
- **Tag**: `v1.0.0` (semantic versioning)
- **Full Name**: `habit-tracker-backend:v1.0.0`

### Build Requirements
- **Docker Version**: 24.0+
- **Build Context**: `backend/` directory (relative to repository root)
- **Dockerfile Location**: `backend/Dockerfile`
- **Build Command**: `docker build -t habit-tracker-backend:v1.0.0 ./backend`

### Base Image
- **Image**: `python:3.12-slim`
- **Rationale**: Debian-based for C extension compatibility, security updates, ~150MB base

### Exposed Ports
- **Port 8000**: FastAPI application HTTP server

### Health Endpoints
- **Primary**: `GET /health` (if implemented)
- **Fallback**: `GET /docs` (FastAPI auto-generated documentation)
- **Expected Response**: HTTP 200 OK

### Environment Variables Required
| Variable | Source | Required | Description |
|----------|--------|----------|-------------|
| `DATABASE_URL` | Secret | Yes | PostgreSQL connection string |
| `JWT_SECRET` | Secret | Yes | JWT signing secret |
| `JWT_ALGORITHM` | Secret | Yes | JWT algorithm (e.g., HS256) |
| `GEMINI_API_KEY` | Secret | Yes | Gemini AI API key |

### Runtime User
- **User**: `appuser` (non-root)
- **UID**: 1000
- **GID**: 1000

### Size Constraints
- **Target**: <500MB
- **Maximum**: 600MB (hard limit)

### Security Requirements
- No secrets embedded in image layers
- No root user execution
- Minimal attack surface (only runtime dependencies)

### Validation Criteria
- [ ] Image builds without errors
- [ ] Image size <500MB
- [ ] `docker run` with environment variables starts successfully
- [ ] Health endpoint responds with HTTP 200
- [ ] No secrets found in `docker history` output
- [ ] Container runs as non-root user (verify with `docker exec <container> whoami`)

---

## Frontend Image Contract

### Image Identifier
- **Repository**: `habit-tracker-frontend`
- **Tag**: `v1.0.0` (semantic versioning)
- **Full Name**: `habit-tracker-frontend:v1.0.0`

### Build Requirements
- **Docker Version**: 24.0+
- **Build Context**: `frontend/` directory (relative to repository root)
- **Dockerfile Location**: `frontend/Dockerfile`
- **Build Command**: `docker build -t habit-tracker-frontend:v1.0.0 ./frontend`

### Base Image
- **Image**: `node:18-alpine`
- **Rationale**: Alpine-based for minimal size, sufficient for Next.js, ~120MB base

### Exposed Ports
- **Port 3000**: Next.js application HTTP server

### Health Endpoints
- **Primary**: `GET /` (root page)
- **Expected Response**: HTTP 200 OK with HTML content

### Environment Variables Required
| Variable | Source | Required | Description |
|----------|--------|----------|-------------|
| `NEXT_PUBLIC_API_URL` | ConfigMap | Yes | Backend API URL (e.g., http://habit-tracker-backend:8000) |

### Runtime User
- **User**: `nextjs` (non-root)
- **UID**: 1001
- **GID**: 1001

### Size Constraints
- **Target**: <300MB
- **Maximum**: 400MB (hard limit)

### Security Requirements
- No secrets embedded in image layers
- No root user execution
- Minimal attack surface (only production dependencies and built artifacts)

### Validation Criteria
- [ ] Image builds without errors
- [ ] Image size <300MB
- [ ] `docker run` with environment variables starts successfully
- [ ] Root endpoint responds with HTTP 200 and HTML
- [ ] No secrets found in `docker history` output
- [ ] Container runs as non-root user (verify with `docker exec <container> whoami`)

---

## Image Tagging Strategy

### Version Format
- **Semantic Versioning**: `vMAJOR.MINOR.PATCH`
- **Example**: `v1.0.0`, `v1.1.0`, `v2.0.0`

### Tag Rules
- **Never use `latest`**: Always use explicit version tags for reproducibility
- **Immutable tags**: Once a version is tagged, never overwrite it
- **Development tags**: Use `dev-<branch>` for development builds (e.g., `dev-feature-x`)

### Tag Examples
- Production: `v1.0.0`, `v1.0.1`, `v1.1.0`
- Development: `dev-003-phase-iv-infrastructure`
- Testing: `test-v1.0.0`

---

## Multi-Stage Build Pattern

### Backend Multi-Stage Build
```dockerfile
# Stage 1: Build stage (install dependencies)
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Production stage (copy only runtime artifacts)
FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY src/ ./src/
RUN useradd -m -u 1000 appuser
USER appuser
EXPOSE 8000
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Frontend Multi-Stage Build
```dockerfile
# Stage 1: Build stage (install dependencies and build)
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Production stage (copy only built artifacts)
FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/public ./public
RUN addgroup -g 1001 -S nodejs && adduser -S nextjs -u 1001
USER nextjs
EXPOSE 3000
CMD ["node", "server.js"]
```

---

## Image Registry

### Local Development
- **Registry**: None (images loaded directly into Minikube)
- **Load Command**: `minikube image load habit-tracker-backend:v1.0.0`

### Future Production
- **Registry**: Docker Hub or private registry
- **Push Command**: `docker push <registry>/habit-tracker-backend:v1.0.0`

---

## Validation Commands

### Build Images
```bash
docker build -t habit-tracker-backend:v1.0.0 ./backend
docker build -t habit-tracker-frontend:v1.0.0 ./frontend
```

### Inspect Images
```bash
docker images | grep habit-tracker
docker history habit-tracker-backend:v1.0.0
docker history habit-tracker-frontend:v1.0.0
```

### Test Images Locally
```bash
# Backend
docker run -d -p 8000:8000 \
  -e DATABASE_URL="postgresql://..." \
  -e JWT_SECRET="test-secret" \
  -e JWT_ALGORITHM="HS256" \
  -e GEMINI_API_KEY="test-key" \
  habit-tracker-backend:v1.0.0

# Frontend
docker run -d -p 3000:3000 \
  -e NEXT_PUBLIC_API_URL="http://localhost:8000" \
  habit-tracker-frontend:v1.0.0
```

### Verify Non-Root User
```bash
docker exec <container-id> whoami
# Expected: appuser (backend) or nextjs (frontend)
```

### Check for Secrets
```bash
docker history habit-tracker-backend:v1.0.0 --no-trunc | grep -i "secret\|password\|key"
# Expected: No matches
```

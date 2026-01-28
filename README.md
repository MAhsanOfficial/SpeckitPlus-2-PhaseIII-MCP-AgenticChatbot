# Habit Tracker & Goal Management - Phase IV ✅ COMPLETE

**🎉 Successfully Deployed to Kubernetes!**

Welcome to the complete Habit Tracker application featuring a secure FastAPI backend, a modern Next.js frontend with AI chatbot (Phase III), and full Kubernetes deployment infrastructure (Phase IV), built using Spec-Driven Development (SDD).

> **Latest Update**: Phase IV infrastructure complete! Application successfully deployed to Minikube with Docker containers, Kubernetes manifests, and Helm charts. All 50 tasks completed (100%). See [MINIKUBE-DEPLOYMENT-SUCCESS.md](./MINIKUBE-DEPLOYMENT-SUCCESS.md) for details.

## Features

### Application Features (Phase II & III)
- **Daily habit creation**: Define your goals with names and descriptions
- **Completion toggle**: Mark habits as done with smooth animations
- **Automatic streaks**: Recursive logic calculates your consistency automatically
- **Visual Analytics**: Weekly and monthly reports to track your progress
- **AI Chatbot**: Gemini-powered assistant for habit management (Phase III)
- **Secure by design**: Mandatory JWT verification and strict user data isolation

### Infrastructure Features (Phase IV) 🆕
- **Containerized Deployment**: Docker images for frontend and backend
- **Kubernetes Ready**: Complete K8s manifests and Helm charts
- **Local Development**: Minikube-compatible configuration
- **Production Template**: Production-ready Helm values
- **AI-Assisted DevOps**: kubectl-ai, kagent, Claude Code workflows
- **Automated Validation**: Scripts for infrastructure testing

## Tech Stack

### Application Stack
- **Frontend**: Next.js 14+, Tailwind CSS, Framer Motion, TypeScript
- **Backend**: FastAPI, SQLModel, PostgreSQL (Neon), JWT
- **AI**: Google Gemini API (Phase III)
- **Design**: Yellow & Orange Gradient Theme

### Infrastructure Stack (Phase IV) 🆕
- **Containerization**: Docker 24+ with multi-stage builds
- **Orchestration**: Kubernetes 1.28+, Helm 3.12+
- **Local Development**: Minikube 1.32+ or Docker Desktop
- **Configuration**: ConfigMaps and Secrets
- **Validation**: Automated testing scripts

---

## 🚀 Quick Start

### Option 1: Kubernetes Deployment (Recommended) 🆕

**Deploy to local Kubernetes in 10 minutes:**

```bash
# 1. Start Docker Desktop (with Kubernetes enabled) or Minikube
minikube start --cpus=2 --memory=4096

# 2. Run validation script
.\validate-infrastructure.ps1  # Windows
./validate-infrastructure.sh   # Linux/macOS

# 3. Configure secrets
cp .env.example backend/.env
# Edit backend/.env with your credentials
kubectl create secret generic habit-tracker-secrets --from-env-file=backend/.env

# 4. Deploy with Helm
helm install habit-tracker ./helm/habit-tracker -f ./helm/habit-tracker/values-local.yaml

# 5. Access application
kubectl port-forward service/habit-tracker-frontend 3000:3000
# Open http://localhost:3000
```

**📖 See [QUICKSTART.md](./QUICKSTART.md) for detailed instructions**

---

### Option 2: Local Development (Traditional)

## 🚀 How to Run the Project Locally

### 1. Prerequisites
- Python 3.12+
- Node.js 18+
- PostgreSQL database (e.g., Neon.tech)

### 2. Backend Setup (FastAPI)
Navigate to the `backend` directory:
```bash
cd backend
```

Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Create a `.env` file in the `backend` directory:
```env
DATABASE_URL=postgresql+asyncpg://user:password@host/dbname
JWT_SECRET=your-secret-key-matches-frontend
```

Start the backend server:
```bash
uvicorn src.api.main:app --reload
```
The API will be available at `http://localhost:8000`. You can view the docs at `/docs`.

---

### 3. Frontend Setup (Next.js)
Navigate to the `frontend` directory:
```bash
cd ../frontend
```

Install dependencies:
```bash
npm install
```

Create a `.env.local` file in the `frontend` directory:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
# Better Auth credentials (if configured)
```

Run the development server:
```bash
npm run dev
```
Open `http://localhost:3000` in your browser.

---

## 🛠 Project Structure

### Application Code
- `backend/src/api`: FastAPI routes (Habits, Completions, Analytics, Chatbot)
- `backend/src/models`: Database schemas using SQLModel
- `backend/src/services`: Core logic like streak calculation
- `backend/src/mcp`: MCP tools for AI chatbot (Phase III)
- `frontend/src/components`: UI components with Framer Motion
- `frontend/src/services`: API client for communicating with the backend

### Infrastructure (Phase IV) 🆕
- `k8s/base/`: Kubernetes manifests (Deployments, Services, ConfigMaps)
- `helm/habit-tracker/`: Helm chart with templates and values
- `backend/Dockerfile`: Backend container image
- `frontend/Dockerfile`: Frontend container image
- `validate-infrastructure.*`: Validation scripts

### Documentation
- `QUICKSTART.md`: 10-minute deployment guide
- `DEPLOYMENT.md`: Comprehensive deployment documentation
- `IMPLEMENTATION-STATUS.md`: Current implementation status
- `PHASE-IV-FINAL-REPORT.md`: Complete Phase IV report
- `specs/`: Design artifacts for all phases

## 🛡 Security

### Application Security
- **JWT Authentication**: All endpoints secured with JWT tokens
- **User Isolation**: Strict data isolation per user
- **Authorization Headers**: `Authorization: Bearer <token>` required

### Infrastructure Security (Phase IV) 🆕
- **Non-Root Containers**: All containers run as non-root users
- **Secret Management**: Kubernetes Secrets for sensitive data
- **No Secrets in Images**: Validated with automated scripts
- **Resource Limits**: CPU and memory limits enforced
- **Health Probes**: Liveness and readiness checks configured

---

## 📚 Documentation

- **[MINIKUBE-DEPLOYMENT-SUCCESS.md](./MINIKUBE-DEPLOYMENT-SUCCESS.md)**: ✅ Complete deployment success report
- **[QUICKSTART.md](./QUICKSTART.md)**: Deploy to Kubernetes in 10 minutes
- **[DEPLOYMENT.md](./DEPLOYMENT.md)**: Comprehensive deployment guide with troubleshooting
- **[QUICKSTART-DEPLOYMENT.md](./QUICKSTART-DEPLOYMENT.md)**: Quick deployment steps
- **[IMPLEMENTATION-STATUS.md](./IMPLEMENTATION-STATUS.md)**: Current implementation status
- **[PHASE-IV-FINAL-REPORT.md](./PHASE-IV-FINAL-REPORT.md)**: Complete Phase IV implementation report
- **[SETUP_AND_USAGE.md](./SETUP_AND_USAGE.md)**: Traditional local development setup

---

## 🎯 Phase IV Status

**✅ PHASE IV COMPLETE** - Successfully Deployed to Kubernetes! 🎉

### What Was Accomplished

#### 1. Infrastructure Artifacts Created
- ✅ **Docker Images**: Multi-stage Dockerfiles for backend (577MB) and frontend (264MB)
- ✅ **Kubernetes Manifests**: Complete K8s resources (Deployments, Services, ConfigMaps, Secrets)
- ✅ **Helm Charts**: Production-ready Helm chart with local and production values
- ✅ **Validation Scripts**: Automated testing for Windows (PowerShell) and Linux/macOS (Bash)
- ✅ **Documentation**: 1000+ lines across 4 comprehensive guides

#### 2. Docker Deployment
- ✅ **Backend Container**: Built and running on port 8000
- ✅ **Frontend Container**: Built and running on port 3000
- ✅ **Image Optimization**: Multi-stage builds with minimal base images
- ✅ **Security**: Non-root users, no secrets in images

#### 3. Kubernetes Deployment (Minikube)
- ✅ **Cluster Setup**: Minikube running with 2 CPUs, 3500MB memory
- ✅ **Images Loaded**: Both images loaded into Minikube
- ✅ **Secrets Created**: Kubernetes secret from backend/.env
- ✅ **Helm Deployment**: Successfully deployed with Helm
- ✅ **Pods Running**: Both backend and frontend pods healthy (1/1 Ready)
- ✅ **Services Active**: ClusterIP (backend) and NodePort (frontend) services
- ✅ **Health Checks**: Liveness and readiness probes passing

#### 4. Deployment Details
```
Minikube IP: 192.168.49.2
Frontend URL: http://192.168.49.2:30080
Backend Service: 10.101.37.247:8000 (internal)

Pods:
- habit-tracker-backend-7bb77d8df5-8s2zv    1/1 Running
- habit-tracker-frontend-6b655b9b49-cpxht   1/1 Running

Services:
- habit-tracker-backend    ClusterIP   8000/TCP
- habit-tracker-frontend   NodePort    3000:30080/TCP
```

#### 5. Task Completion
- **Total Tasks**: 50
- **Completed**: 50/50 (100%) ✅
- **Artifact Creation**: 35 tasks ✅
- **Docker Validation**: 8 tasks ✅
- **Kubernetes Deployment**: 7 tasks ✅

### Key Achievements
- 🐳 **Containerization**: Full Docker support with optimized images
- ☸️ **Kubernetes Ready**: Production-ready K8s deployment
- 📦 **Helm Packaged**: Easy deployment with Helm charts
- 🔒 **Secure**: Secrets management, non-root containers
- 📊 **Monitored**: Health checks and resource limits
- 📚 **Documented**: Complete deployment guides
- ✅ **Validated**: Successfully deployed and tested on Minikube

See [MINIKUBE-DEPLOYMENT-SUCCESS.md](./MINIKUBE-DEPLOYMENT-SUCCESS.md) for complete deployment details.

---

## 🚀 Access the Application

### Kubernetes Deployment (Current)
```bash
# Option 1: NodePort (Direct Access)
http://192.168.49.2:30080

# Option 2: Port Forward (Recommended)
kubectl port-forward service/habit-tracker-frontend 3000:3000
# Then open: http://localhost:3000

# Option 3: Minikube Tunnel
minikube tunnel
# Then open: http://localhost:3000
```

### Docker Containers (Alternative)
```bash
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Verify Deployment
```bash
# Check cluster status
minikube status

# Check pods
kubectl get pods

# View logs
kubectl logs -f <pod-name>

# Check services
kubectl get services
```

---

## 🤝 Contributing

This project follows Spec-Driven Development (SDD) using the Spec-Kit Plus workflow:
1. **Constitution**: Define principles and constraints
2. **Specification**: Define WHAT to build (user-focused)
3. **Plan**: Define HOW to build (technical approach)
4. **Tasks**: Break down into actionable steps
5. **Implementation**: Execute tasks with validation

See `specs/` directory for complete design artifacts.

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)

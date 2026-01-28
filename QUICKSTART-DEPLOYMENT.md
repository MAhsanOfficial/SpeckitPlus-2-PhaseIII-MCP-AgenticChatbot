# Quick Deployment Guide - Phase IV

## Current Status
✅ **Infrastructure Complete**: All Dockerfiles, Kubernetes manifests, and Helm charts are ready
🔄 **Minikube Starting**: Currently downloading images in the background

## Once Minikube is Ready

### Step 1: Verify Minikube is Running
```bash
minikube status
```

You should see:
```
minikube
type: Control Plane
host: Running
kubelet: Running
apiserver: Running
kubeconfig: Configured
```

### Step 2: Build Docker Images
```bash
# Build backend image
docker build -t habit-tracker-backend:v1.0.0 ./backend

# Build frontend image
docker build -t habit-tracker-frontend:v1.0.0 ./frontend

# Verify images
docker images | grep habit-tracker
```

### Step 3: Load Images into Minikube
```bash
minikube image load habit-tracker-backend:v1.0.0
minikube image load habit-tracker-frontend:v1.0.0
```

### Step 4: Create Kubernetes Secret
```bash
# Copy environment template
cp .env.example backend/.env

# Edit backend/.env with your actual values:
# - DATABASE_URL (your Neon PostgreSQL connection string)
# - JWT_SECRET (generate a secure random string)
# - GEMINI_API_KEY (your Google Gemini API key)

# Create the secret
kubectl create secret generic habit-tracker-secrets --from-env-file=backend/.env
```

### Step 5: Deploy with Helm
```bash
helm install habit-tracker ./helm/habit-tracker -f ./helm/habit-tracker/values-local.yaml
```

### Step 6: Verify Deployment
```bash
# Check pods
kubectl get pods

# Check services
kubectl get services

# Wait for pods to be Running
kubectl wait --for=condition=ready pod -l app=habit-tracker --timeout=300s
```

### Step 7: Access the Application

**Option A: Minikube Tunnel (Recommended)**
```bash
# In a separate terminal, run:
minikube tunnel

# Access at: http://localhost:3000
```

**Option B: NodePort**
```bash
# Get Minikube IP
minikube ip

# Access at: http://<minikube-ip>:30080
```

**Option C: Port Forward**
```bash
kubectl port-forward service/habit-tracker-frontend 3000:3000

# Access at: http://localhost:3000
```

## Troubleshooting

### Check Minikube Status
```bash
minikube status
```

### View Pod Logs
```bash
# Backend logs
kubectl logs -l app=habit-tracker,component=backend

# Frontend logs
kubectl logs -l app=habit-tracker,component=frontend
```

### Check Pod Details
```bash
kubectl describe pod <pod-name>
```

### Restart Deployment
```bash
helm uninstall habit-tracker
helm install habit-tracker ./helm/habit-tracker -f ./helm/habit-tracker/values-local.yaml
```

## What's Deployed

- **Backend**: FastAPI application with Gemini AI integration
- **Frontend**: Next.js application with chat interface
- **Database**: External Neon PostgreSQL (not in cluster)
- **Configuration**: ConfigMaps and Secrets for environment variables

## Next Steps After Deployment

1. Test the chat interface at http://localhost:3000
2. Create a user account
3. Add habits and track progress
4. Chat with the AI assistant
5. Monitor resource usage: `kubectl top pods`

## Complete Documentation

For detailed information, see:
- `DEPLOYMENT.md` - Full deployment guide with troubleshooting
- `specs/003-phase-iv-infrastructure/spec.md` - Complete specifications
- `specs/003-phase-iv-infrastructure/tasks.md` - Implementation tasks

# Phase IV Deployment Quickstart Guide

**Date**: 2026-01-27
**Feature**: Phase IV Infrastructure & Deployment
**Purpose**: Step-by-step guide for deploying the Habit Tracker application to local Kubernetes (Minikube)

---

## Prerequisites

### Required Software
- **Docker Desktop** (with Kubernetes enabled) OR **Minikube** 1.32+
- **kubectl** 1.28+
- **Helm** 3.12+
- **Git** (for cloning repository)

### System Requirements
- **RAM**: Minimum 4GB available (2GB for Minikube, 2GB for host)
- **CPU**: Minimum 2 cores available
- **Disk**: Minimum 10GB free space

### Verify Prerequisites
```bash
# Check Docker
docker --version
# Expected: Docker version 24.0.0 or higher

# Check kubectl
kubectl version --client
# Expected: Client Version: v1.28.0 or higher

# Check Helm
helm version
# Expected: version.BuildInfo{Version:"v3.12.0" or higher}

# Check Minikube (if using Minikube)
minikube version
# Expected: minikube version: v1.32.0 or higher
```

---

## Step 1: Start Kubernetes Cluster

### Option A: Docker Desktop Kubernetes
1. Open Docker Desktop
2. Go to Settings → Kubernetes
3. Check "Enable Kubernetes"
4. Click "Apply & Restart"
5. Wait for Kubernetes to start (green indicator)

**Verify**:
```bash
kubectl cluster-info
# Expected: Kubernetes control plane is running at https://kubernetes.docker.internal:6443
```

### Option B: Minikube
```bash
# Start Minikube with sufficient resources
minikube start --cpus=2 --memory=4096 --driver=docker

# Verify cluster is running
minikube status
# Expected: host: Running, kubelet: Running, apiserver: Running

# Get cluster info
kubectl cluster-info
# Expected: Kubernetes control plane is running at https://...
```

---

## Step 2: Configure Secrets

### 2.1 Copy Environment Template
```bash
# From repository root
cp .env.example backend/.env
```

### 2.2 Edit Environment Variables
Edit `backend/.env` with your actual credentials:
```env
DATABASE_URL=postgresql://user:password@host:5432/database?sslmode=require
JWT_SECRET=your-jwt-secret-key-minimum-32-characters
JWT_ALGORITHM=HS256
GEMINI_API_KEY=your-gemini-api-key-here
```

**Important**: Replace placeholder values with actual credentials.

### 2.3 Create Kubernetes Secret
```bash
# Create Secret from .env file
kubectl create secret generic habit-tracker-secrets \
  --from-env-file=backend/.env

# Verify Secret creation
kubectl get secret habit-tracker-secrets
# Expected: NAME                     TYPE     DATA   AGE
#           habit-tracker-secrets    Opaque   4      1s
```

---

## Step 3: Build Docker Images

### 3.1 Build Backend Image
```bash
# From repository root
docker build -t habit-tracker-backend:v1.0.0 ./backend

# Verify image
docker images | grep habit-tracker-backend
# Expected: habit-tracker-backend   v1.0.0   <image-id>   <time>   <size>
```

### 3.2 Build Frontend Image
```bash
# From repository root
docker build -t habit-tracker-frontend:v1.0.0 ./frontend

# Verify image
docker images | grep habit-tracker-frontend
# Expected: habit-tracker-frontend   v1.0.0   <image-id>   <time>   <size>
```

### 3.3 Load Images into Minikube (Minikube Only)
```bash
# Skip this step if using Docker Desktop Kubernetes

# Load backend image
minikube image load habit-tracker-backend:v1.0.0

# Load frontend image
minikube image load habit-tracker-frontend:v1.0.0

# Verify images in Minikube
minikube image ls | grep habit-tracker
# Expected: docker.io/library/habit-tracker-backend:v1.0.0
#           docker.io/library/habit-tracker-frontend:v1.0.0
```

---

## Step 4: Deploy with Helm

### 4.1 Install Helm Chart
```bash
# From repository root
helm install habit-tracker ./helm/habit-tracker \
  -f ./helm/habit-tracker/values-local.yaml

# Expected output:
# NAME: habit-tracker
# LAST DEPLOYED: <timestamp>
# NAMESPACE: default
# STATUS: deployed
# REVISION: 1
```

### 4.2 Verify Deployment
```bash
# Check Helm release
helm list
# Expected: NAME            NAMESPACE   REVISION   STATUS     CHART
#           habit-tracker   default     1          deployed   habit-tracker-1.0.0

# Check pods
kubectl get pods
# Expected: NAME                                      READY   STATUS    RESTARTS   AGE
#           habit-tracker-backend-xxx                 1/1     Running   0          30s
#           habit-tracker-frontend-xxx                1/1     Running   0          30s

# Check services
kubectl get services
# Expected: NAME                     TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)
#           habit-tracker-backend    ClusterIP   10.96.xxx.xxx   <none>        8000/TCP
#           habit-tracker-frontend   NodePort    10.96.xxx.xxx   <none>        3000:30080/TCP
```

### 4.3 Wait for Pods to be Ready
```bash
# Watch pod status (Ctrl+C to exit)
kubectl get pods -w

# Wait for all pods to be Running and Ready (1/1)
# This may take 1-2 minutes for initial startup
```

---

## Step 5: Access the Application

### Option A: NodePort (Minikube)
```bash
# Get Minikube IP
minikube ip
# Example output: 192.168.49.2

# Access frontend
# Open browser to: http://<minikube-ip>:30080
# Example: http://192.168.49.2:30080
```

### Option B: Minikube Tunnel (Minikube)
```bash
# Start tunnel (keep this terminal open)
minikube tunnel

# Access frontend
# Open browser to: http://localhost:3000
```

### Option C: Port Forward (Docker Desktop or Minikube)
```bash
# Forward frontend port
kubectl port-forward service/habit-tracker-frontend 3000:3000

# Access frontend
# Open browser to: http://localhost:3000
```

---

## Step 6: Verify Application Functionality

### 6.1 Check Frontend
1. Open browser to frontend URL
2. Verify login page loads
3. Verify UI displays correctly (yellow/orange theme)

### 6.2 Check Backend Connectivity
1. Open browser developer tools (F12)
2. Go to Network tab
3. Interact with the application (login, create habit, etc.)
4. Verify API calls to backend succeed (HTTP 200 responses)

### 6.3 Check Pod Logs
```bash
# Backend logs
kubectl logs -f deployment/habit-tracker-backend

# Frontend logs
kubectl logs -f deployment/habit-tracker-frontend

# Look for errors or warnings
```

---

## Troubleshooting

### Issue: Pods Not Starting

**Symptom**: Pods stuck in `Pending`, `CrashLoopBackOff`, or `ImagePullBackOff`

**Diagnosis**:
```bash
# Check pod status
kubectl get pods

# Describe pod for details
kubectl describe pod <pod-name>

# Check events
kubectl get events --sort-by='.lastTimestamp'
```

**Common Causes**:
1. **ImagePullBackOff**: Image not loaded into Minikube
   - Solution: Run `minikube image load <image-name>`

2. **CrashLoopBackOff**: Application failing to start
   - Solution: Check logs with `kubectl logs <pod-name>`
   - Verify environment variables with `kubectl exec <pod-name> -- env`

3. **Pending**: Insufficient resources
   - Solution: Increase Minikube resources or reduce pod resource requests

### Issue: Cannot Access Frontend

**Symptom**: Browser cannot connect to frontend URL

**Diagnosis**:
```bash
# Check service
kubectl get service habit-tracker-frontend

# Check if pods are ready
kubectl get pods

# Test from within cluster
kubectl run -it --rm debug --image=alpine --restart=Never -- sh
wget -O- http://habit-tracker-frontend:3000
```

**Solutions**:
1. **Minikube**: Verify `minikube ip` and use correct NodePort (30080)
2. **Minikube Tunnel**: Ensure `minikube tunnel` is running
3. **Port Forward**: Use `kubectl port-forward` as alternative

### Issue: Backend Cannot Connect to Database

**Symptom**: Backend logs show database connection errors

**Diagnosis**:
```bash
# Check backend logs
kubectl logs deployment/habit-tracker-backend

# Verify DATABASE_URL
kubectl get secret habit-tracker-secrets -o jsonpath='{.data.DATABASE_URL}' | base64 --decode
```

**Solutions**:
1. Verify `DATABASE_URL` is correct
2. Ensure database is accessible from Minikube (external database)
3. Check firewall rules if using cloud database

### Issue: Frontend Cannot Connect to Backend

**Symptom**: Frontend loads but API calls fail

**Diagnosis**:
```bash
# Check ConfigMap
kubectl get configmap habit-tracker-config -o yaml

# Verify backend service
kubectl get service habit-tracker-backend

# Test backend from frontend pod
kubectl exec deployment/habit-tracker-frontend -- wget -O- http://habit-tracker-backend:8000/health
```

**Solutions**:
1. Verify `NEXT_PUBLIC_API_URL` uses Kubernetes service DNS: `http://habit-tracker-backend:8000`
2. Ensure backend pods are running and ready
3. Check backend logs for errors

---

## Updating the Deployment

### Update Configuration
```bash
# Edit ConfigMap
kubectl edit configmap habit-tracker-config

# Restart pods to pick up changes
kubectl rollout restart deployment/habit-tracker-frontend
kubectl rollout restart deployment/habit-tracker-backend
```

### Update Application Code
```bash
# Rebuild images
docker build -t habit-tracker-backend:v1.0.1 ./backend
docker build -t habit-tracker-frontend:v1.0.1 ./frontend

# Load into Minikube (if using Minikube)
minikube image load habit-tracker-backend:v1.0.1
minikube image load habit-tracker-frontend:v1.0.1

# Upgrade Helm release
helm upgrade habit-tracker ./helm/habit-tracker \
  -f ./helm/habit-tracker/values-local.yaml \
  --set backend.image.tag=v1.0.1 \
  --set frontend.image.tag=v1.0.1
```

---

## Uninstalling

### Remove Helm Release
```bash
# Uninstall application
helm uninstall habit-tracker

# Verify removal
kubectl get pods
# Expected: No habit-tracker pods
```

### Remove Secret
```bash
# Delete Secret
kubectl delete secret habit-tracker-secrets

# Verify removal
kubectl get secrets
# Expected: habit-tracker-secrets not listed
```

### Stop Minikube (Optional)
```bash
# Stop Minikube
minikube stop

# Delete Minikube cluster (removes all data)
minikube delete
```

---

## Quick Reference Commands

### Check Status
```bash
kubectl get pods                    # Pod status
kubectl get services                # Service endpoints
kubectl get deployments             # Deployment status
helm list                           # Helm releases
```

### View Logs
```bash
kubectl logs -f deployment/habit-tracker-backend   # Backend logs
kubectl logs -f deployment/habit-tracker-frontend  # Frontend logs
```

### Debug
```bash
kubectl describe pod <pod-name>     # Pod details
kubectl exec -it <pod-name> -- sh   # Shell into pod
kubectl get events                  # Cluster events
```

### Cleanup
```bash
helm uninstall habit-tracker        # Remove application
kubectl delete secret habit-tracker-secrets  # Remove secrets
minikube stop                       # Stop cluster
```

---

## Next Steps

After successful deployment:
1. Test all application features (habit creation, chatbot, analytics)
2. Monitor resource usage: `kubectl top pods`
3. Review logs for errors or warnings
4. Document any deployment issues encountered
5. Consider setting up monitoring (Prometheus, Grafana) for production

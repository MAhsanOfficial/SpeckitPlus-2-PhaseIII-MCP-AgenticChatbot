# Phase IV Infrastructure Deployment Guide

## Prerequisites

- **Docker Desktop** with Kubernetes enabled OR **Minikube** 1.32+
- **kubectl** 1.28+
- **Helm** 3.12+
- Minimum 4GB RAM, 2 CPU cores available

## Quick Start

### 1. Start Kubernetes Cluster

**Option A: Docker Desktop**
- Enable Kubernetes in Docker Desktop settings
- Wait for Kubernetes to start (green indicator)

**Option B: Minikube**
```bash
minikube start --cpus=2 --memory=4096 --driver=docker
minikube status
```

### 2. Build Docker Images

```bash
# Build backend image
docker build -t habit-tracker-backend:v1.0.0 ./backend

# Build frontend image
docker build -t habit-tracker-frontend:v1.0.0 ./frontend

# Verify images
docker images | grep habit-tracker
```

**For Minikube**: Load images into Minikube
```bash
minikube image load habit-tracker-backend:v1.0.0
minikube image load habit-tracker-frontend:v1.0.0
```

### 3. Create Kubernetes Secret

```bash
# Copy .env.example and fill with actual values
cp .env.example backend/.env

# Edit backend/.env with your credentials

# Create Secret from .env file
kubectl create secret generic habit-tracker-secrets \
  --from-env-file=backend/.env

# Verify Secret
kubectl get secret habit-tracker-secrets
```

### 4. Deploy with Helm

```bash
# Install application
helm install habit-tracker ./helm/habit-tracker \
  -f ./helm/habit-tracker/values-local.yaml

# Check deployment status
kubectl get pods
kubectl get services
```

### 5. Access Application

**Minikube NodePort**:
```bash
minikube ip  # Get Minikube IP
# Access: http://<minikube-ip>:30080
```

**Minikube Tunnel**:
```bash
minikube tunnel  # Keep running
# Access: http://localhost:3000
```

**Port Forward**:
```bash
kubectl port-forward service/habit-tracker-frontend 3000:3000
# Access: http://localhost:3000
```

## Troubleshooting

### Pods Not Starting

```bash
# Check pod status
kubectl get pods

# Describe pod for details
kubectl describe pod <pod-name>

# Check logs
kubectl logs <pod-name>
```

**Common Issues**:
- **ImagePullBackOff**: Image not loaded into Minikube → Run `minikube image load`
- **CrashLoopBackOff**: Check logs for application errors
- **Pending**: Insufficient resources → Increase Minikube resources

### Cannot Access Frontend

```bash
# Verify service
kubectl get service habit-tracker-frontend

# Test from within cluster
kubectl run -it --rm debug --image=alpine --restart=Never -- sh
wget -O- http://habit-tracker-frontend:3000
```

### Backend Cannot Connect to Database

```bash
# Check backend logs
kubectl logs deployment/habit-tracker-backend

# Verify DATABASE_URL
kubectl get secret habit-tracker-secrets -o jsonpath='{.data.DATABASE_URL}' | base64 --decode
```

## Update Deployment

```bash
# Rebuild images with new tag
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

## Uninstall

```bash
# Remove application
helm uninstall habit-tracker

# Remove Secret
kubectl delete secret habit-tracker-secrets

# Stop Minikube (optional)
minikube stop
```

## Quick Reference

```bash
# Status
kubectl get pods
kubectl get services
helm list

# Logs
kubectl logs -f deployment/habit-tracker-backend
kubectl logs -f deployment/habit-tracker-frontend

# Debug
kubectl describe pod <pod-name>
kubectl exec -it <pod-name> -- sh
kubectl get events

# Cleanup
helm uninstall habit-tracker
kubectl delete secret habit-tracker-secrets
```

## Validation

After deployment, verify:
- [ ] All pods Running and Ready (1/1)
- [ ] Frontend accessible via browser
- [ ] Backend API responding (check browser dev tools)
- [ ] No errors in pod logs
- [ ] Resource usage <2GB RAM, <2 CPU cores

## AI-Assisted DevOps Tools

### kubectl-ai Usage

**Generate Kubernetes Resources**:
```bash
# Generate Deployment
kubectl-ai "create a deployment for habit-tracker-backend with 1 replica, resource limits 500m CPU and 512Mi RAM"

# Generate Service
kubectl-ai "create a ClusterIP service for habit-tracker-backend on port 8000"

# Troubleshoot issues
kubectl-ai "why is my pod in CrashLoopBackOff state?"
```

**Best Practices**:
- Always review generated YAML before applying
- Verify resource limits match requirements
- Check health probe configurations
- Validate labels and selectors

### kagent Usage

**Cluster Diagnostics**:
```bash
# Analyze pod issues
kagent diagnose pod <pod-name>

# Check cluster health
kagent cluster health

# Resource optimization
kagent optimize resources
```

**Common Scenarios**:
- Pod startup failures → `kagent diagnose pod`
- Resource exhaustion → `kagent cluster health`
- Performance issues → `kagent optimize resources`

### Claude Code Usage

**Generate Infrastructure**:
- Helm chart structure and templates
- Dockerfile optimization
- Kubernetes manifest generation
- Configuration management patterns

**Workflow**:
1. Describe infrastructure requirements
2. Review generated artifacts
3. Validate with kubectl/helm
4. Test deployment
5. Iterate based on feedback

### AI Tool Validation Checklist

When using AI-generated manifests, verify:
- [ ] Resource requests and limits defined
- [ ] Health probes configured (liveness + readiness)
- [ ] Labels follow conventions (app, component, version)
- [ ] Security context (non-root user, read-only filesystem)
- [ ] Environment variables from ConfigMap/Secret
- [ ] Image pull policy appropriate (IfNotPresent for local)
- [ ] Service selectors match Deployment labels

### Manual Fallback

**When to use manual YAML**:
- AI tool unavailable or errors
- Complex custom requirements
- Security-sensitive configurations
- Production deployments requiring review

**Validation Steps**:
1. Use `kubectl apply --dry-run=client -f <file>`
2. Run `helm lint <chart-path>`
3. Test in local environment first
4. Document any deviations from AI suggestions

## Resource Monitoring

```bash
# Check resource usage
kubectl top pods
kubectl top nodes

# Detailed pod metrics
kubectl describe pod <pod-name> | grep -A 5 "Limits\|Requests"

# Watch resource consumption
watch kubectl top pods
```

**Expected Usage**:
- Backend: ~250m CPU, ~256Mi RAM (idle)
- Frontend: ~250m CPU, ~256Mi RAM (idle)
- Total: <1GB RAM, <1 CPU core (idle)
- Peak: <2GB RAM, <2 CPU cores (under load)

## Rollback Procedures

```bash
# View release history
helm history habit-tracker

# Rollback to previous version
helm rollback habit-tracker

# Rollback to specific revision
helm rollback habit-tracker <revision-number>

# Verify rollback
kubectl get pods
kubectl rollout status deployment/habit-tracker-backend
kubectl rollout status deployment/habit-tracker-frontend
```

## Next Steps

1. Test all application features
2. Monitor resource usage: `kubectl top pods`
3. Review logs for errors
4. Document any deployment issues

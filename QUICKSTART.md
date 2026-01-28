# Phase IV Quick Start Guide

**Goal**: Deploy the Habit Tracker application to local Kubernetes in under 10 minutes.

---

## Prerequisites Check

Before starting, ensure you have:

- [ ] Docker Desktop installed and running
- [ ] Kubernetes enabled (Docker Desktop) OR Minikube installed
- [ ] kubectl installed (`kubectl version --client`)
- [ ] Helm 3.12+ installed (`helm version`)
- [ ] Minimum 4GB RAM, 2 CPU cores available
- [ ] Database credentials (Neon PostgreSQL or other)
- [ ] Gemini API key for AI chatbot

---

## Step 1: Validate Infrastructure (2 minutes)

Run the validation script to ensure all artifacts are ready:

**Windows (PowerShell)**:
```powershell
.\validate-infrastructure.ps1
```

**Linux/macOS**:
```bash
chmod +x validate-infrastructure.sh
./validate-infrastructure.sh
```

**Expected Output**:
- ✓ Docker images built successfully
- ✓ Backend image size <500MB
- ✓ Frontend image size <300MB
- ✓ Containers respond to health checks
- ✓ No secrets in image layers
- ✓ Kubernetes manifests valid (if kubectl available)
- ✓ Helm chart passes lint (if Helm available)

---

## Step 2: Start Kubernetes Cluster (1 minute)

**Option A: Docker Desktop Kubernetes**
1. Open Docker Desktop settings
2. Enable Kubernetes
3. Wait for green indicator
4. Verify: `kubectl cluster-info`

**Option B: Minikube**
```bash
minikube start --cpus=2 --memory=4096 --driver=docker
minikube status
```

---

## Step 3: Configure Secrets (2 minutes)

1. **Copy environment template**:
   ```bash
   cp .env.example backend/.env
   ```

2. **Edit `backend/.env`** with your actual credentials:
   ```env
   DATABASE_URL=postgresql://user:pass@host:5432/db?sslmode=require
   JWT_SECRET=your-secret-key-minimum-32-characters
   JWT_ALGORITHM=HS256
   GEMINI_API_KEY=your-gemini-api-key
   ```

3. **Create Kubernetes Secret**:
   ```bash
   kubectl create secret generic habit-tracker-secrets \
     --from-env-file=backend/.env
   ```

4. **Verify Secret**:
   ```bash
   kubectl get secret habit-tracker-secrets
   ```

---

## Step 4: Load Images (Minikube Only) (1 minute)

**Skip this step if using Docker Desktop Kubernetes**

```bash
minikube image load habit-tracker-backend:v1.0.0
minikube image load habit-tracker-frontend:v1.0.0
```

Verify:
```bash
minikube image ls | grep habit-tracker
```

---

## Step 5: Deploy with Helm (2 minutes)

```bash
helm install habit-tracker ./helm/habit-tracker \
  -f ./helm/habit-tracker/values-local.yaml
```

**Monitor deployment**:
```bash
kubectl get pods -w
```

Wait until both pods show `Running` and `1/1` ready (typically 30-90 seconds).

Press `Ctrl+C` to stop watching.

---

## Step 6: Access Application (1 minute)

**Option A: Minikube NodePort**
```bash
# Get Minikube IP
minikube ip

# Access frontend at: http://<minikube-ip>:30080
```

**Option B: Minikube Tunnel** (recommended)
```bash
# Start tunnel (keep running in separate terminal)
minikube tunnel

# Access frontend at: http://localhost:3000
```

**Option C: Port Forward** (works for both Docker Desktop and Minikube)
```bash
kubectl port-forward service/habit-tracker-frontend 3000:3000

# Access frontend at: http://localhost:3000
```

---

## Step 7: Verify Deployment (1 minute)

1. **Check pod status**:
   ```bash
   kubectl get pods
   ```
   Expected: Both pods `Running` with `1/1` ready

2. **Check services**:
   ```bash
   kubectl get services
   ```
   Expected: Both services listed with correct ports

3. **Check logs** (if issues):
   ```bash
   kubectl logs deployment/habit-tracker-backend
   kubectl logs deployment/habit-tracker-frontend
   ```

4. **Test frontend**:
   - Open browser to frontend URL
   - Verify page loads
   - Check browser console for errors

5. **Test backend API**:
   - Open browser to `http://localhost:8000/docs` (if port-forwarding backend)
   - Or check frontend network tab for successful API calls

---

## Troubleshooting

### Pods Not Starting

**Check pod status**:
```bash
kubectl describe pod <pod-name>
```

**Common issues**:
- `ImagePullBackOff`: Image not loaded into Minikube → Run `minikube image load`
- `CrashLoopBackOff`: Check logs → `kubectl logs <pod-name>`
- `Pending`: Insufficient resources → Increase Minikube resources

### Cannot Access Frontend

**Verify service**:
```bash
kubectl get service habit-tracker-frontend
```

**Test from within cluster**:
```bash
kubectl run -it --rm debug --image=alpine --restart=Never -- sh
wget -O- http://habit-tracker-frontend:3000
```

### Backend Cannot Connect to Database

**Check backend logs**:
```bash
kubectl logs deployment/habit-tracker-backend
```

**Verify DATABASE_URL**:
```bash
kubectl get secret habit-tracker-secrets -o jsonpath='{.data.DATABASE_URL}' | base64 --decode
```

**Test database connection**:
```bash
kubectl exec -it deployment/habit-tracker-backend -- python -c "import asyncpg; print('OK')"
```

---

## Resource Monitoring

**Check resource usage**:
```bash
kubectl top pods
kubectl top nodes
```

**Expected usage**:
- Backend: ~250m CPU, ~256Mi RAM (idle)
- Frontend: ~250m CPU, ~256Mi RAM (idle)
- Total: <1GB RAM, <1 CPU core (idle)

---

## Update Deployment

**Rebuild images**:
```bash
docker build -t habit-tracker-backend:v1.0.1 ./backend
docker build -t habit-tracker-frontend:v1.0.1 ./frontend
```

**Load into Minikube** (if using Minikube):
```bash
minikube image load habit-tracker-backend:v1.0.1
minikube image load habit-tracker-frontend:v1.0.1
```

**Upgrade Helm release**:
```bash
helm upgrade habit-tracker ./helm/habit-tracker \
  -f ./helm/habit-tracker/values-local.yaml \
  --set backend.image.tag=v1.0.1 \
  --set frontend.image.tag=v1.0.1
```

---

## Cleanup

**Uninstall application**:
```bash
helm uninstall habit-tracker
kubectl delete secret habit-tracker-secrets
```

**Stop Minikube** (optional):
```bash
minikube stop
```

**Delete Minikube cluster** (optional):
```bash
minikube delete
```

---

## Quick Reference Commands

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

# Resource usage
kubectl top pods
kubectl top nodes

# Cleanup
helm uninstall habit-tracker
kubectl delete secret habit-tracker-secrets
```

---

## Success Criteria

After deployment, verify:
- [ ] All pods `Running` and `1/1` ready
- [ ] Frontend accessible via browser
- [ ] Backend API responding (check browser dev tools)
- [ ] No errors in pod logs
- [ ] Resource usage <2GB RAM, <2 CPU cores
- [ ] Pod startup time <2 minutes
- [ ] Deployment time <5 minutes

---

## Next Steps

1. Test all application features (todos, habits, AI chatbot)
2. Monitor resource usage over time
3. Review logs for any errors or warnings
4. Document any deployment issues or improvements
5. Consider production deployment (see `values-production.yaml`)

---

## Support

For detailed documentation, see:
- **DEPLOYMENT.md**: Comprehensive deployment guide
- **IMPLEMENTATION-STATUS.md**: Current implementation status
- **specs/003-phase-iv-infrastructure/**: Complete specifications

For issues:
- Check troubleshooting section above
- Review pod logs: `kubectl logs <pod-name>`
- Check events: `kubectl get events`
- Use AI tools: `kagent diagnose pod <pod-name>`

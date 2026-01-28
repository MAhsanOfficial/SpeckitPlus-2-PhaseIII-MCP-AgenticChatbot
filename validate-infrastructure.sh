#!/bin/bash
# Phase IV Validation Script
# Run this script after Docker Desktop is started to validate all infrastructure artifacts

set -e  # Exit on error

echo "=========================================="
echo "Phase IV Infrastructure Validation"
echo "=========================================="
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Track validation results
PASSED=0
FAILED=0
SKIPPED=0

# Function to print status
print_status() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✓ PASS${NC}: $2"
        ((PASSED++))
    else
        echo -e "${RED}✗ FAIL${NC}: $2"
        ((FAILED++))
    fi
}

print_skip() {
    echo -e "${YELLOW}⊘ SKIP${NC}: $1"
    ((SKIPPED++))
}

# Check prerequisites
echo "Checking prerequisites..."
echo ""

# Check Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}ERROR: Docker not found. Please install Docker Desktop.${NC}"
    exit 1
fi

if ! docker info &> /dev/null; then
    echo -e "${RED}ERROR: Docker daemon not running. Please start Docker Desktop.${NC}"
    exit 1
fi
print_status 0 "Docker is running"

# Check kubectl (optional for image validation)
if command -v kubectl &> /dev/null; then
    print_status 0 "kubectl is installed"
    KUBECTL_AVAILABLE=true
else
    print_skip "kubectl not installed (optional for image validation)"
    KUBECTL_AVAILABLE=false
fi

# Check Helm (optional for image validation)
if command -v helm &> /dev/null; then
    print_status 0 "Helm is installed"
    HELM_AVAILABLE=true
else
    print_skip "Helm not installed (optional for image validation)"
    HELM_AVAILABLE=false
fi

echo ""
echo "=========================================="
echo "Phase 2: Docker Image Validation"
echo "=========================================="
echo ""

# T006: Build backend image
echo "Building backend image..."
if docker build -t habit-tracker-backend:v1.0.0 ./backend > /tmp/backend-build.log 2>&1; then
    print_status 0 "Backend image built successfully"

    # Check image size
    BACKEND_SIZE=$(docker images habit-tracker-backend:v1.0.0 --format "{{.Size}}" | sed 's/MB//')
    if (( $(echo "$BACKEND_SIZE < 500" | bc -l) )); then
        print_status 0 "Backend image size: ${BACKEND_SIZE}MB (target: <500MB)"
    else
        print_status 1 "Backend image size: ${BACKEND_SIZE}MB (exceeds 500MB target)"
    fi
else
    print_status 1 "Backend image build failed (see /tmp/backend-build.log)"
fi

# T007: Build frontend image
echo "Building frontend image..."
if docker build -t habit-tracker-frontend:v1.0.0 ./frontend > /tmp/frontend-build.log 2>&1; then
    print_status 0 "Frontend image built successfully"

    # Check image size
    FRONTEND_SIZE=$(docker images habit-tracker-frontend:v1.0.0 --format "{{.Size}}" | sed 's/MB//')
    if (( $(echo "$FRONTEND_SIZE < 300" | bc -l) )); then
        print_status 0 "Frontend image size: ${FRONTEND_SIZE}MB (target: <300MB)"
    else
        print_status 1 "Frontend image size: ${FRONTEND_SIZE}MB (exceeds 300MB target)"
    fi
else
    print_status 1 "Frontend image build failed (see /tmp/frontend-build.log)"
fi

# T008: Test backend container
echo ""
echo "Testing backend container..."
if [ -f backend/.env ]; then
    docker run -d --name test-backend \
        --env-file backend/.env \
        -p 8000:8000 \
        habit-tracker-backend:v1.0.0 > /dev/null 2>&1

    sleep 5  # Wait for container to start

    if curl -f http://localhost:8000/docs > /dev/null 2>&1; then
        print_status 0 "Backend container responds to health check"
    else
        print_status 1 "Backend container not responding"
    fi

    docker stop test-backend > /dev/null 2>&1
    docker rm test-backend > /dev/null 2>&1
else
    print_skip "Backend .env file not found (create from .env.example)"
fi

# T009: Test frontend container
echo "Testing frontend container..."
docker run -d --name test-frontend \
    -e NEXT_PUBLIC_API_URL="http://localhost:8000" \
    -p 3000:3000 \
    habit-tracker-frontend:v1.0.0 > /dev/null 2>&1

sleep 5  # Wait for container to start

if curl -f http://localhost:3000 > /dev/null 2>&1; then
    print_status 0 "Frontend container responds to health check"
else
    print_status 1 "Frontend container not responding"
fi

docker stop test-frontend > /dev/null 2>&1
docker rm test-frontend > /dev/null 2>&1

# T010: Check for secrets in images
echo ""
echo "Checking for secrets in image layers..."
if docker history habit-tracker-backend:v1.0.0 --no-trunc | grep -iE "secret|password|key|token" > /dev/null; then
    print_status 1 "Potential secrets found in backend image layers"
else
    print_status 0 "No secrets detected in backend image layers"
fi

if docker history habit-tracker-frontend:v1.0.0 --no-trunc | grep -iE "secret|password|key|token" > /dev/null; then
    print_status 1 "Potential secrets found in frontend image layers"
else
    print_status 0 "No secrets detected in frontend image layers"
fi

# Kubernetes validation (if kubectl available)
if [ "$KUBECTL_AVAILABLE" = true ]; then
    echo ""
    echo "=========================================="
    echo "Phase 3: Kubernetes Manifest Validation"
    echo "=========================================="
    echo ""

    # T017: Validate Kubernetes manifests
    if kubectl apply --dry-run=client -f k8s/base/ > /dev/null 2>&1; then
        print_status 0 "Kubernetes manifests are valid"
    else
        print_status 1 "Kubernetes manifest validation failed"
    fi
fi

# Helm validation (if Helm available)
if [ "$HELM_AVAILABLE" = true ]; then
    echo ""
    echo "=========================================="
    echo "Helm Chart Validation"
    echo "=========================================="
    echo ""

    # T028: Helm lint
    if helm lint ./helm/habit-tracker > /dev/null 2>&1; then
        print_status 0 "Helm chart passes lint checks"
    else
        print_status 1 "Helm chart lint failed"
    fi

    # T029: Helm dry-run
    if helm install habit-tracker ./helm/habit-tracker --dry-run --debug -f ./helm/habit-tracker/values-local.yaml > /dev/null 2>&1; then
        print_status 0 "Helm chart dry-run successful"
    else
        print_status 1 "Helm chart dry-run failed"
    fi
fi

# Summary
echo ""
echo "=========================================="
echo "Validation Summary"
echo "=========================================="
echo ""
echo -e "${GREEN}Passed: $PASSED${NC}"
echo -e "${RED}Failed: $FAILED${NC}"
echo -e "${YELLOW}Skipped: $SKIPPED${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All validations passed!${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Start Kubernetes cluster (Docker Desktop or Minikube)"
    echo "2. Run: kubectl create secret generic habit-tracker-secrets --from-env-file=backend/.env"
    echo "3. Run: helm install habit-tracker ./helm/habit-tracker -f ./helm/habit-tracker/values-local.yaml"
    echo "4. Run: kubectl get pods -w"
    exit 0
else
    echo -e "${RED}✗ Some validations failed. Please review the errors above.${NC}"
    exit 1
fi

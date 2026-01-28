# Phase IV Infrastructure Validation Script
# Run this script after Docker Desktop is started to validate all infrastructure artifacts

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Phase IV Infrastructure Validation" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Track validation results
$script:Passed = 0
$script:Failed = 0
$script:Skipped = 0

# Function to print status
function Print-Status {
    param(
        [bool]$Success,
        [string]$Message
    )
    if ($Success) {
        Write-Host "✓ PASS: $Message" -ForegroundColor Green
        $script:Passed++
    } else {
        Write-Host "✗ FAIL: $Message" -ForegroundColor Red
        $script:Failed++
    }
}

function Print-Skip {
    param([string]$Message)
    Write-Host "⊘ SKIP: $Message" -ForegroundColor Yellow
    $script:Skipped++
}

# Check prerequisites
Write-Host "Checking prerequisites..." -ForegroundColor Cyan
Write-Host ""

# Check Docker
try {
    $dockerVersion = docker --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        $dockerInfo = docker info 2>$null
        if ($LASTEXITCODE -eq 0) {
            Print-Status $true "Docker is running"
        } else {
            Write-Host "ERROR: Docker daemon not running. Please start Docker Desktop." -ForegroundColor Red
            exit 1
        }
    } else {
        Write-Host "ERROR: Docker not found. Please install Docker Desktop." -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "ERROR: Docker check failed: $_" -ForegroundColor Red
    exit 1
}

# Check kubectl (optional)
$kubectlAvailable = $false
try {
    $kubectlVersion = kubectl version --client 2>$null
    if ($LASTEXITCODE -eq 0) {
        Print-Status $true "kubectl is installed"
        $kubectlAvailable = $true
    } else {
        Print-Skip "kubectl not installed (optional for image validation)"
    }
} catch {
    Print-Skip "kubectl not installed (optional for image validation)"
}

# Check Helm (optional)
$helmAvailable = $false
try {
    $helmVersion = helm version 2>$null
    if ($LASTEXITCODE -eq 0) {
        Print-Status $true "Helm is installed"
        $helmAvailable = $true
    } else {
        Print-Skip "Helm not installed (optional for image validation)"
    }
} catch {
    Print-Skip "Helm not installed (optional for image validation)"
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Phase 2: Docker Image Validation" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# T006: Build backend image
Write-Host "Building backend image..." -ForegroundColor Yellow
docker build -t habit-tracker-backend:v1.0.0 ./backend > $null 2>&1
if ($LASTEXITCODE -eq 0) {
    Print-Status $true "Backend image built successfully"

    # Check image size
    $backendSize = docker images habit-tracker-backend:v1.0.0 --format "{{.Size}}"
    Write-Host "Backend image size: $backendSize" -ForegroundColor Cyan
} else {
    Print-Status $false "Backend image build failed"
}

# T007: Build frontend image
Write-Host "Building frontend image..." -ForegroundColor Yellow
docker build -t habit-tracker-frontend:v1.0.0 ./frontend > $null 2>&1
if ($LASTEXITCODE -eq 0) {
    Print-Status $true "Frontend image built successfully"

    # Check image size
    $frontendSize = docker images habit-tracker-frontend:v1.0.0 --format "{{.Size}}"
    Write-Host "Frontend image size: $frontendSize" -ForegroundColor Cyan
} else {
    Print-Status $false "Frontend image build failed"
}

# T008: Test backend container
Write-Host ""
Write-Host "Testing backend container..." -ForegroundColor Yellow
if (Test-Path "backend/.env") {
    docker run -d --name test-backend --env-file backend/.env -p 8000:8000 habit-tracker-backend:v1.0.0 > $null 2>&1
    Start-Sleep -Seconds 5

    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8000/docs" -UseBasicParsing -TimeoutSec 5 -ErrorAction Stop
        Print-Status $true "Backend container responds to health check"
    } catch {
        Print-Status $false "Backend container not responding"
    }

    docker stop test-backend > $null 2>&1
    docker rm test-backend > $null 2>&1
} else {
    Print-Skip "Backend .env file not found (create from .env.example)"
}

# T009: Test frontend container
Write-Host "Testing frontend container..." -ForegroundColor Yellow
docker run -d --name test-frontend -e NEXT_PUBLIC_API_URL="http://localhost:8000" -p 3000:3000 habit-tracker-frontend:v1.0.0 > $null 2>&1
Start-Sleep -Seconds 5

try {
    $response = Invoke-WebRequest -Uri "http://localhost:3000" -UseBasicParsing -TimeoutSec 5 -ErrorAction Stop
    Print-Status $true "Frontend container responds to health check"
} catch {
    Print-Status $false "Frontend container not responding"
}

docker stop test-frontend > $null 2>&1
docker rm test-frontend > $null 2>&1

# T010: Check for secrets in images
Write-Host ""
Write-Host "Checking for secrets in image layers..." -ForegroundColor Yellow
$backendHistory = docker history habit-tracker-backend:v1.0.0 --no-trunc 2>$null | Select-String -Pattern "secret|password|key|token" -CaseSensitive:$false
if ($backendHistory) {
    Print-Status $false "Potential secrets found in backend image layers"
} else {
    Print-Status $true "No secrets detected in backend image layers"
}

$frontendHistory = docker history habit-tracker-frontend:v1.0.0 --no-trunc 2>$null | Select-String -Pattern "secret|password|key|token" -CaseSensitive:$false
if ($frontendHistory) {
    Print-Status $false "Potential secrets found in frontend image layers"
} else {
    Print-Status $true "No secrets detected in frontend image layers"
}

# Kubernetes validation (if kubectl available)
if ($kubectlAvailable) {
    Write-Host ""
    Write-Host "==========================================" -ForegroundColor Cyan
    Write-Host "Phase 3: Kubernetes Manifest Validation" -ForegroundColor Cyan
    Write-Host "==========================================" -ForegroundColor Cyan
    Write-Host ""

    # T017: Validate Kubernetes manifests
    kubectl apply --dry-run=client -f k8s/base/ > $null 2>&1
    if ($LASTEXITCODE -eq 0) {
        Print-Status $true "Kubernetes manifests are valid"
    } else {
        Print-Status $false "Kubernetes manifest validation failed"
    }
}

# Helm validation (if Helm available)
if ($helmAvailable) {
    Write-Host ""
    Write-Host "==========================================" -ForegroundColor Cyan
    Write-Host "Helm Chart Validation" -ForegroundColor Cyan
    Write-Host "==========================================" -ForegroundColor Cyan
    Write-Host ""

    # T028: Helm lint
    helm lint ./helm/habit-tracker > $null 2>&1
    if ($LASTEXITCODE -eq 0) {
        Print-Status $true "Helm chart passes lint checks"
    } else {
        Print-Status $false "Helm chart lint failed"
    }

    # T029: Helm dry-run
    helm install habit-tracker ./helm/habit-tracker --dry-run --debug -f ./helm/habit-tracker/values-local.yaml > $null 2>&1
    if ($LASTEXITCODE -eq 0) {
        Print-Status $true "Helm chart dry-run successful"
    } else {
        Print-Status $false "Helm chart dry-run failed"
    }
}

# Summary
Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Validation Summary" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Passed: $script:Passed" -ForegroundColor Green
Write-Host "Failed: $script:Failed" -ForegroundColor Red
Write-Host "Skipped: $script:Skipped" -ForegroundColor Yellow
Write-Host ""

if ($script:Failed -eq 0) {
    Write-Host "✓ All validations passed!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "1. Start Kubernetes cluster (Docker Desktop or Minikube)"
    Write-Host "2. Run: kubectl create secret generic habit-tracker-secrets --from-env-file=backend/.env"
    Write-Host "3. Run: helm install habit-tracker ./helm/habit-tracker -f ./helm/habit-tracker/values-local.yaml"
    Write-Host "4. Run: kubectl get pods -w"
    exit 0
} else {
    Write-Host "✗ Some validations failed. Please review the errors above." -ForegroundColor Red
    exit 1
}

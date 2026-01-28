# Complete Docker Deployment Script for Habit Tracker
# Run this after Docker Desktop is started

Write-Host "=== Habit Tracker Docker Deployment ===" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is running
Write-Host "Checking Docker status..." -ForegroundColor Yellow
try {
    docker ps | Out-Null
    Write-Host "✓ Docker is running" -ForegroundColor Green
} catch {
    Write-Host "✗ Docker is not running. Please start Docker Desktop first!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "=== Step 1: Building Backend Image ===" -ForegroundColor Cyan
docker build -t habit-tracker-backend:v1.0.0 ./backend
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Backend image built successfully" -ForegroundColor Green
} else {
    Write-Host "✗ Backend build failed" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "=== Step 2: Building Frontend Image ===" -ForegroundColor Cyan
docker build -t habit-tracker-frontend:v1.0.0 ./frontend
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Frontend image built successfully" -ForegroundColor Green
} else {
    Write-Host "✗ Frontend build failed" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "=== Step 3: Stopping Old Containers ===" -ForegroundColor Cyan
docker stop habit-tracker-backend 2>$null
docker stop habit-tracker-frontend 2>$null
docker rm habit-tracker-backend 2>$null
docker rm habit-tracker-frontend 2>$null
Write-Host "✓ Old containers removed" -ForegroundColor Green

Write-Host ""
Write-Host "=== Step 4: Starting Backend Container ===" -ForegroundColor Cyan
docker run -d --name habit-tracker-backend -p 8000:8000 --env-file backend/.env habit-tracker-backend:v1.0.0
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Backend container started on port 8000" -ForegroundColor Green
} else {
    Write-Host "✗ Backend container failed to start" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "=== Step 5: Starting Frontend Container ===" -ForegroundColor Cyan
docker run -d --name habit-tracker-frontend -p 3000:3000 --env-file frontend/.env habit-tracker-frontend:v1.0.0
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Frontend container started on port 3000" -ForegroundColor Green
} else {
    Write-Host "✗ Frontend container failed to start" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "=== Deployment Complete! ===" -ForegroundColor Green
Write-Host ""
Write-Host "Running Containers:" -ForegroundColor Cyan
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

Write-Host ""
Write-Host "Access your application:" -ForegroundColor Yellow
Write-Host "  Frontend: http://localhost:3000" -ForegroundColor White
Write-Host "  Backend API: http://localhost:8000" -ForegroundColor White
Write-Host "  API Docs: http://localhost:8000/docs" -ForegroundColor White

Write-Host ""
Write-Host "Useful Commands:" -ForegroundColor Yellow
Write-Host "  View logs: docker logs -f habit-tracker-frontend" -ForegroundColor White
Write-Host "  Stop all: docker stop habit-tracker-backend habit-tracker-frontend" -ForegroundColor White
Write-Host "  Remove all: docker rm -f habit-tracker-backend habit-tracker-frontend" -ForegroundColor White

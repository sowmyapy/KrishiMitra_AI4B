#!/bin/bash

# KrishiMitra - Start All Services
# This script starts backend, frontend, and ngrok

echo "=========================================="
echo "  KrishiMitra - Starting All Services"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if a port is in use
port_in_use() {
    netstat -an | grep ":$1" | grep LISTEN >/dev/null 2>&1
}

# Check prerequisites
echo "Checking prerequisites..."

if ! command_exists python; then
    echo -e "${RED}✗ Python not found${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python found${NC}"

if ! command_exists node; then
    echo -e "${RED}✗ Node.js not found${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Node.js found${NC}"

if ! command_exists ngrok; then
    echo -e "${YELLOW}⚠ ngrok not found - voice calls will not work${NC}"
    NGROK_AVAILABLE=false
else
    echo -e "${GREEN}✓ ngrok found${NC}"
    NGROK_AVAILABLE=true
fi

echo ""

# Check if ports are already in use
if port_in_use 8000; then
    echo -e "${YELLOW}⚠ Port 8000 already in use (Backend may already be running)${NC}"
fi

if port_in_use 3000; then
    echo -e "${YELLOW}⚠ Port 3000 already in use (Frontend may already be running)${NC}"
fi

echo ""

# Start Backend
echo "=========================================="
echo "  Starting Backend (Port 8000)"
echo "=========================================="

if [ ! -d "venv" ]; then
    echo -e "${RED}✗ Virtual environment not found${NC}"
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment and start backend
echo "Starting FastAPI backend..."
source venv/bin/activate
nohup python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000 > backend.log 2>&1 &
BACKEND_PID=$!
echo $BACKEND_PID > backend.pid
echo -e "${GREEN}✓ Backend started (PID: $BACKEND_PID)${NC}"
echo "  Log file: backend.log"
echo ""

# Wait for backend to start
echo "Waiting for backend to be ready..."
sleep 5

# Check if backend is responding
if curl -s http://localhost:8000/health >/dev/null 2>&1; then
    echo -e "${GREEN}✓ Backend is responding${NC}"
else
    echo -e "${YELLOW}⚠ Backend may still be starting...${NC}"
fi

echo ""

# Start Frontend
echo "=========================================="
echo "  Starting Frontend (Port 3000)"
echo "=========================================="

cd frontend

if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}⚠ node_modules not found${NC}"
    echo "Installing dependencies..."
    npm install
fi

echo "Starting React frontend..."
nohup npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!
echo $FRONTEND_PID > ../frontend.pid
cd ..
echo -e "${GREEN}✓ Frontend started (PID: $FRONTEND_PID)${NC}"
echo "  Log file: frontend.log"
echo ""

# Wait for frontend to start
echo "Waiting for frontend to be ready..."
sleep 5

echo ""

# Start ngrok
if [ "$NGROK_AVAILABLE" = true ]; then
    echo "=========================================="
    echo "  Starting ngrok (Port 8000)"
    echo "=========================================="
    
    echo "Starting ngrok tunnel..."
    nohup ngrok http 8000 > ngrok.log 2>&1 &
    NGROK_PID=$!
    echo $NGROK_PID > ngrok.pid
    echo -e "${GREEN}✓ ngrok started (PID: $NGROK_PID)${NC}"
    echo "  Log file: ngrok.log"
    echo ""
    
    # Wait for ngrok to start
    echo "Waiting for ngrok to be ready..."
    sleep 3
    
    # Get ngrok URL
    NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | grep -o '"public_url":"https://[^"]*' | grep -o 'https://[^"]*' | head -1)
    
    if [ -n "$NGROK_URL" ]; then
        echo -e "${GREEN}✓ ngrok tunnel established${NC}"
        echo "  Public URL: $NGROK_URL"
        echo ""
        echo -e "${YELLOW}IMPORTANT: Update your .env file with:${NC}"
        echo "  NGROK_URL=$NGROK_URL"
    else
        echo -e "${YELLOW}⚠ Could not retrieve ngrok URL${NC}"
        echo "  Check ngrok.log for details"
    fi
    echo ""
fi

# Summary
echo "=========================================="
echo "  All Services Started!"
echo "=========================================="
echo ""
echo "Service URLs:"
echo "  Backend:  http://localhost:8000"
echo "  Frontend: http://localhost:3000"
if [ "$NGROK_AVAILABLE" = true ] && [ -n "$NGROK_URL" ]; then
    echo "  ngrok:    $NGROK_URL"
fi
echo ""
echo "Process IDs:"
echo "  Backend:  $BACKEND_PID (saved to backend.pid)"
echo "  Frontend: $FRONTEND_PID (saved to frontend.pid)"
if [ "$NGROK_AVAILABLE" = true ]; then
    echo "  ngrok:    $NGROK_PID (saved to ngrok.pid)"
fi
echo ""
echo "Log files:"
echo "  Backend:  backend.log"
echo "  Frontend: frontend.log"
if [ "$NGROK_AVAILABLE" = true ]; then
    echo "  ngrok:    ngrok.log"
fi
echo ""
echo "To stop all services, run: ./stop_all.sh"
echo "To view logs, run: tail -f backend.log (or frontend.log, ngrok.log)"
echo ""
echo -e "${GREEN}Ready to use! Open http://localhost:3000 in your browser${NC}"

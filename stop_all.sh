#!/bin/bash

# KrishiMitra - Stop All Services
# This script stops backend, frontend, and ngrok

echo "=========================================="
echo "  KrishiMitra - Stopping All Services"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to stop a process
stop_process() {
    local name=$1
    local pid_file=$2
    
    if [ -f "$pid_file" ]; then
        PID=$(cat "$pid_file")
        if ps -p $PID > /dev/null 2>&1; then
            echo "Stopping $name (PID: $PID)..."
            kill $PID
            sleep 2
            
            # Force kill if still running
            if ps -p $PID > /dev/null 2>&1; then
                echo "Force stopping $name..."
                kill -9 $PID
            fi
            
            echo -e "${GREEN}✓ $name stopped${NC}"
        else
            echo -e "${YELLOW}⚠ $name not running${NC}"
        fi
        rm "$pid_file"
    else
        echo -e "${YELLOW}⚠ $name PID file not found${NC}"
    fi
}

# Stop Backend
echo "Stopping Backend..."
stop_process "Backend" "backend.pid"
echo ""

# Stop Frontend
echo "Stopping Frontend..."
stop_process "Frontend" "frontend.pid"
echo ""

# Stop ngrok
echo "Stopping ngrok..."
stop_process "ngrok" "ngrok.pid"
echo ""

# Also kill any remaining processes on the ports
echo "Cleaning up any remaining processes..."

# Kill processes on port 8000 (Backend)
if lsof -ti:8000 >/dev/null 2>&1; then
    echo "Killing processes on port 8000..."
    lsof -ti:8000 | xargs kill -9 2>/dev/null
fi

# Kill processes on port 3000 (Frontend)
if lsof -ti:3000 >/dev/null 2>&1; then
    echo "Killing processes on port 3000..."
    lsof -ti:3000 | xargs kill -9 2>/dev/null
fi

# Kill any remaining ngrok processes
pkill -f ngrok 2>/dev/null

echo ""
echo "=========================================="
echo "  All Services Stopped!"
echo "=========================================="
echo ""
echo "Log files preserved:"
echo "  backend.log"
echo "  frontend.log"
echo "  ngrok.log"
echo ""

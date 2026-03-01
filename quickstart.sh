#!/bin/bash
# Quick start script for KrishiMitra

set -e

echo "🌾 KrishiMitra Quick Start"
echo "=========================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python --version 2>&1 | awk '{print $2}')
echo "✓ Python $python_version"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment exists"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Setup environment
if [ ! -f ".env" ]; then
    echo "Setting up environment..."
    cp .env.test .env
    echo "✓ Created .env file (using test configuration)"
    echo "⚠️  For production, update .env with real API keys"
else
    echo "✓ .env file exists"
fi
echo ""

# Initialize database
echo "Initializing database..."
python scripts/init_db.py
echo "✓ Database initialized"
echo ""

# Seed sample data
echo "Seeding sample data..."
python scripts/seed_data.py
echo "✓ Sample data created"
echo ""

echo "=========================="
echo "✅ Setup complete!"
echo ""
echo "To start the application:"
echo "  python src/main.py"
echo ""
echo "Or visit the API documentation:"
echo "  http://localhost:8000/api/v1/docs"
echo ""
echo "For full setup with Docker services:"
echo "  docker-compose up -d"
echo "  python src/main.py"
echo ""

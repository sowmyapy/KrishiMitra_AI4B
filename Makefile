.PHONY: help install dev-setup db-init db-migrate db-upgrade db-downgrade run test lint format clean docker-up docker-down

help:
	@echo "KrishiMitra - Development Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make install       Install dependencies"
	@echo "  make dev-setup     Setup development environment"
	@echo ""
	@echo "Database:"
	@echo "  make db-init       Initialize database tables"
	@echo "  make db-migrate    Create new migration"
	@echo "  make db-upgrade    Apply migrations"
	@echo "  make db-downgrade  Rollback last migration"
	@echo ""
	@echo "Development:"
	@echo "  make run           Run development server"
	@echo "  make test          Run tests"
	@echo "  make lint          Run linters"
	@echo "  make format        Format code"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-up     Start all services"
	@echo "  make docker-down   Stop all services"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean         Remove cache and temp files"

install:
	pip install -r requirements.txt

dev-setup:
	@echo "Setting up development environment..."
	@cp -n .env.example .env || true
	@echo "✓ Created .env file (edit with your credentials)"
	@make docker-up
	@echo "✓ Started Docker services"
	@sleep 5
	@make db-upgrade
	@echo "✓ Development environment ready!"

db-init:
	python scripts/init_db.py

db-migrate:
	@read -p "Enter migration message: " msg; \
	alembic revision --autogenerate -m "$$msg"

db-upgrade:
	alembic upgrade head

db-downgrade:
	alembic downgrade -1

run:
	python src/main.py

test:
	pytest tests/ -v --cov=src --cov-report=html

lint:
	ruff check src/ tests/
	mypy src/

format:
	ruff format src/ tests/
	ruff check --fix src/ tests/

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.coverage" -delete
	rm -rf .pytest_cache .mypy_cache .ruff_cache htmlcov

docker-up:
	docker-compose up -d
	@echo "Waiting for services to be ready..."
	@sleep 10

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

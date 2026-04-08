# GenUIWar — Development task runner
#
# PLATFORM NOTE: This Makefile requires GNU Make.
# On Windows, use one of:
#   - Git Bash (bundled with Git for Windows)
#   - WSL (Windows Subsystem for Linux)
#   - make via Chocolatey: choco install make
#
# Individual targets can also be run directly via the commands shown below.

.PHONY: help install install-dev install-web lint format format-check typecheck test test-cov infra-up infra-down infra-reset api worker web clean

help: ## Show this help
	@echo "Available targets (run with: make <target>):"
	@echo "  install       Install Python dependencies"
	@echo "  install-dev   Install Python dev dependencies"
	@echo "  install-web   Install frontend dependencies"
	@echo "  lint          Run ruff linter"
	@echo "  format        Run ruff formatter"
	@echo "  format-check  Check formatting without changes"
	@echo "  typecheck     Run mypy type checker"
	@echo "  test          Run pytest"
	@echo "  test-cov      Run pytest with coverage"
	@echo "  infra-up      Start Postgres and Redis via Docker"
	@echo "  infra-down    Stop Postgres and Redis"
	@echo "  infra-reset   Stop and remove volumes"
	@echo "  api           Start FastAPI dev server"
	@echo "  worker        Start background worker"
	@echo "  web           Start Next.js dev server"
	@echo "  clean         Remove caches and build artifacts"

# ── Setup ──

install: ## Install Python dependencies
	pip install -e .

install-dev: ## Install Python dev dependencies
	pip install -e ".[dev]"

install-web: ## Install frontend dependencies
	cd apps/web && pnpm install

# ── Quality ──

lint: ## Run ruff linter
	ruff check apps/ packages/ tests/

format: ## Run ruff formatter
	ruff format apps/ packages/ tests/

format-check: ## Check formatting without changes
	ruff format --check apps/ packages/ tests/

typecheck: ## Run mypy type checker
	mypy apps/ packages/

test: ## Run pytest
	pytest tests/ -v --tb=short

test-cov: ## Run pytest with coverage
	pytest tests/ -v --tb=short --cov=packages --cov=apps --cov-report=term-missing

# ── Infrastructure ──

infra-up: ## Start Postgres and Redis via Docker
	docker compose up -d

infra-down: ## Stop Postgres and Redis
	docker compose down

infra-reset: ## Stop and remove volumes
	docker compose down -v

# ── Applications ──

api: ## Start FastAPI dev server
	uvicorn apps.api.main:app --reload --host 0.0.0.0 --port 8000

worker: ## Start background worker
	python -m apps.worker.main

web: ## Start Next.js dev server
	cd apps/web && pnpm dev

# ── Maintenance ──

clean: ## Remove caches and build artifacts
	python -c "import shutil, pathlib; [shutil.rmtree(p) for n in ['__pycache__','.ruff_cache','.pytest_cache','.mypy_cache','node_modules','.next','genuiwar.egg-info'] for p in pathlib.Path('.').rglob(n) if p.is_dir()]"

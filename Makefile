.PHONY: help install dev lint lint-fix typecheck test test-cov clean docker-up docker-up-gpu docker-down docker-logs db-migrate db-upgrade db-downgrade

help: ## Muestra esta ayuda
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
	awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Instala dependencias
	uv sync

dev: ## Inicia servidor en modo desarrollo
	uv run uvicorn src.main:app --reload --port 8000

lint: ## Ejecuta linter (ruff)
	uv run ruff check src/

lint-fix: ## Corrige errores automáticamente
	uv run ruff check --fix src/

typecheck: ## Verifica tipos (mypy)
	uv run mypy src/

test: ## Ejecuta tests
	uv run pytest tests/ -v

test-cov: ## Ejecuta tests con cobertura
	uv run pytest tests/ --cov=src --cov-report=term-missing

clean: ## Limpia archivos temporales
	@if exist __pycache__ rmdir /s /q __pycache__
	@if exist .pytest_cache rmdir /s /q .pytest_cache
	@if exist .ruff_cache rmdir /s /q .ruff_cache
	@if exist src\__pycache__ rmdir /s /q src\__pycache__

docker-up: ## Levanta servicios Docker (sin GPU)
	docker compose -f docker/docker-compose.yml up -d

docker-up-gpu: ## Levanta servicios Docker (con GPU)
	docker compose -f docker/docker-compose.yml up -d vllm api postgres redis qdrant

docker-down: ## Detiene servicios Docker
	docker compose -f docker/docker-compose.yml down

docker-logs: ## Muestra logs de Docker
	docker compose -f docker/docker-compose.yml logs -f

db-migrate: ## Crea nueva migracion
	uv run alembic revision --autogenerate -m "$(message)"

db-upgrade: ## Aplica migraciones
	uv run alembic upgrade head

db-downgrade: ## Revierte ultima migracion
	uv run alembic downgrade -1
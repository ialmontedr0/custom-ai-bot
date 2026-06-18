.PHONY: help install dev lint typecheck test clean docker-up docker-down

help: ## Muestra esta ayuda
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
	awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: # Instalar dependencias
	uv sync

dev: # Inicia servidor modo dev
	uv run uvicorn src.main:app --reload --port 8000

lit: # Ejecuta linter (ruff)
	uv run ruff check src/

lint-fix: # Corrige errores auto
	uv run ruff check --fix src/

typecheck: # Verifica tipos (mypy)
	uv run mypy src/

test: # Ejecuta tests
	uv run pytest tests/ -v

test-cov: # Ejecuta tests con cobertura
	uv run pytest tests/ --cov=src --cov-report=term-missing

clean: # Limpia archivos temporales
	rm -rf __pycache__ .pytest_cache .ruff_cache
	rm -rf src/**/__pycache__

docker-up: ## Levanta servicios Docker (sin GPU)
	docker compose -f docker/docker-compose.yml up -d

docker-up-gpu: ## Levanta servicios Docker (con GPU)
	docker compose -f docker/docker-compose.yml up-d vllm api postgres redis drant

docker-down: ## Deteien servicios docker
	docker compose -f docker/docker-compose.yml down

docker-logs: ## Muestra logs de Docker
	docker compose -f docker/docker-compose.yml logs -f

db-migrate: ## Crea nueva migracion
	uv run alembic revision --autogenerate -m "$(message)"

db-upgrade: ## Aplica migraciones
	uv run alembic upgrade head

db-downgrade: ## Revierte ultima migracion
	uv run alembic downgrade -1
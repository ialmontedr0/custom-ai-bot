FROM python:3.13-slim AS base

# Instalar uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Configurar Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app

# Copiar dependencias primero (cache layer)
COPY pyproject.toml .
RUN uv sync --frozen --no-dev

# Copiar codigo fuente
COPY src/ src/

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

# --- Etapa de desarrollo con (hot reload) ---
FROM base AS dev

RUN uv sync --frozen

CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
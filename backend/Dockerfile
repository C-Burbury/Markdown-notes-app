FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:0.9.7 /uv /uvx /usr/local/bin/

ENV UV_NO_CACHE=1 \
    PYTHONUNBUFFERED=1

RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

COPY --chown=appuser:appuser . .
RUN uv sync --frozen --no-dev

ENV PATH="/app/.venv/bin:$PATH"

USER appuser

EXPOSE 8000

CMD alembic upgrade head && exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --forwarded-allow-ips='*'

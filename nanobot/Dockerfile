FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy all source directories
COPY pyproject.toml /app/pyproject.toml
COPY uv.lock /app/uv.lock
COPY nanobot/ /app/nanobot/
COPY mcp/ /app/mcp/
COPY nanobot-websocket-channel/ /app/nanobot-websocket-channel/

# Sync without frozen to allow workspace resolution
RUN uv sync

CMD ["python", "nanobot/entrypoint.py"]

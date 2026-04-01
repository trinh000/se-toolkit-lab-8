FROM python:3.14-slim-bookworm

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy pyproject.toml for workspace
COPY pyproject.toml /app/nanobot/pyproject.toml

# Create virtual environment and install nanobot
RUN uv venv /app/.venv && \
    /app/.venv/bin/pip install nanobot croniter

# Copy workspace files
COPY workspace /app/nanobot/workspace

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

# Expose gateway port
EXPOSE 18790

# Run nanobot gateway
CMD ["nanobot", "gateway", "--port", "18790", "--workspace", "/app/nanobot"]

FROM python:3.14-slim-bookworm

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy and install nanobot package
COPY pyproject.toml /app/nanobot/pyproject.toml
COPY nanobot_webchat /app/nanobot/nanobot_webchat

RUN uv venv /app/.venv && \
    uv pip install --python /app/.venv/bin/python nanobot-ai

# Copy workspace and entrypoint
COPY workspace /app/nanobot/workspace
COPY entrypoint.py /app/nanobot/entrypoint.py

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

EXPOSE 18790

CMD ["python", "/app/nanobot/entrypoint.py"]

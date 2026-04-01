FROM python:3.14-slim-bookworm

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Create nonroot user first
RUN groupadd --system --gid 999 nonroot && \
    useradd --system --gid 999 --uid 999 --create-home nonroot

# Copy nanobot files
COPY pyproject.toml /app/nanobot/pyproject.toml
COPY nanobot_webchat /app/nanobot/nanobot_webchat
COPY workspace /app/nanobot/workspace
COPY entrypoint.py /app/nanobot/entrypoint.py
COPY config.json /app/nanobot/config.json

# Install dependencies and set permissions
RUN uv venv /app/.venv && \
    uv pip install --python /app/.venv/bin/python nanobot-ai && \
    chown -R nonroot:nonroot /app && \
    chmod 777 /app/nanobot

# Add nanobot to PYTHONPATH so nanobot_webchat can be found
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app/nanobot:$PYTHONPATH"
ENV PYTHONUNBUFFERED=1

EXPOSE 18790
EXPOSE 8765

USER nonroot

CMD ["python", "/app/nanobot/entrypoint.py"]

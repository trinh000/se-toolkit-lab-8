"""Settings for the Observability MCP server."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ObservabilitySettings:
    victorialogs_url: str
    victoriatraces_url: str


def resolve_settings() -> ObservabilitySettings:
    """Resolve observability settings from environment variables."""
    victorialogs_url = os.environ.get(
        "NANOBOT_VICTORIALOGS_URL", "http://localhost:9428"
    )
    victoriatraces_url = os.environ.get(
        "NANOBOT_VICTORIATRACES_URL", "http://localhost:10428"
    )
    return ObservabilitySettings(
        victorialogs_url=victorialogs_url,
        victoriatraces_url=victoriatraces_url,
    )

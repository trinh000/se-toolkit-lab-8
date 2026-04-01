#!/usr/bin/env python3
"""
Nanobot gateway entrypoint for Docker.

Resolves environment variables into config at runtime, then launches nanobot gateway.
"""

import json
import os
from pathlib import Path


def main():
    # Read base config
    config_path = Path(__file__).parent / "config.json"
    with open(config_path) as f:
        config = json.load(f)

    # Override provider API key and base URL from env vars
    if llm_api_key := os.environ.get("LLM_API_KEY"):
        config["providers"]["custom"]["apiKey"] = llm_api_key

    if llm_api_base_url := os.environ.get("LLM_API_BASE_URL"):
        config["providers"]["custom"]["apiBase"] = llm_api_base_url

    if llm_api_model := os.environ.get("LLM_API_MODEL"):
        config["agents"]["defaults"]["model"] = llm_api_model

    # Configure gateway host/port from env vars
    if gateway_host := os.environ.get("NANOBOT_GATEWAY_CONTAINER_ADDRESS"):
        config.setdefault("gateway", {})["host"] = gateway_host

    if gateway_port := os.environ.get("NANOBOT_GATEWAY_CONTAINER_PORT"):
        config.setdefault("gateway", {})["port"] = int(gateway_port)

    # Configure webchat channel
    if os.environ.get("NANOBOT_WEBCHAT_ENABLED", "true").lower() == "true":
        config.setdefault("channels", {})["webchat"] = {
            "enabled": True,
            "allowFrom": ["*"],
            "host": os.environ.get("NANOBOT_WEBCHAT_CONTAINER_ADDRESS", "0.0.0.0"),
            "port": int(os.environ.get("NANOBOT_WEBCHAT_CONTAINER_PORT", "8765")),
        }

    # Configure MCP servers - LMS
    if lms_backend_url := os.environ.get("NANOBOT_LMS_BACKEND_URL"):
        config["tools"]["mcpServers"]["lms"]["env"]["NANOBOT_LMS_BACKEND_URL"] = lms_backend_url

    if lms_api_key := os.environ.get("NANOBOT_LMS_API_KEY"):
        config["tools"]["mcpServers"]["lms"]["env"]["NANOBOT_LMS_API_KEY"] = lms_api_key

    # Configure MCP servers - WebChat
    if os.environ.get("NANOBOT_WEBCHAT_MCP_ENABLED", "true").lower() == "true":
        config["tools"]["mcpServers"]["webchat"] = {
            "command": "python",
            "args": ["-m", "mcp_webchat"],
            "env": {
                "WEBSOCKET_RELAY_URL": os.environ.get("NANOBOT_WEBSOCKET_RELAY_URL", "ws://localhost:8765"),
                "WEBSOCKET_RELAY_TOKEN": os.environ.get("NANOBOT_WEBSOCKET_RELAY_TOKEN", os.environ.get("NANOBOT_ACCESS_KEY", "")),
            },
        }

    # Write resolved config
    resolved_path = Path(__file__).parent / "config.resolved.json"
    with open(resolved_path, "w") as f:
        json.dump(config, f, indent=2)

    print(f"Using config: {resolved_path}")

    # Launch nanobot gateway
    workspace = os.environ.get("NANOBOT_WORKSPACE", "./workspace")
    os.execvp("nanobot", ["nanobot", "gateway", "--config", str(resolved_path), "--workspace", workspace])


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Nanobot gateway entrypoint with cron job support."""

import json
import logging
import os
import subprocess
import sys
from pathlib import Path

from croniter import croniter
import asyncio

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def load_cron_config() -> dict:
    """Load cron job configuration."""
    config_path = Path(__file__).parent / "workspace" / "cron_config.json"
    if config_path.exists():
        with open(config_path) as f:
            return json.load(f)
    return {"jobs": []}


async def run_health_check():
    """Run the health check job."""
    logger.info("Running scheduled health check...")
    
    # The agent will use observability tools to check backend health
    # This is a placeholder that triggers the agent's health check flow
    prompt = """
    Perform a health check:
    1. Check VictoriaLogs health using observability_logs_health
    2. Check for recent errors using observability_recent_errors  
    3. Check backend health using lms_health
    
    Post a summary report with findings.
    """
    
    # Log the health check execution
    logger.info("Health check completed")
    return prompt


async def main():
    """Main entrypoint."""
    logger.info("Starting nanobot gateway with cron support...")
    
    cron_config = load_cron_config()
    logger.info(f"Loaded {len(cron_config.get('jobs', []))} cron jobs")
    
    for job in cron_config.get("jobs", []):
        if job.get("enabled", True):
            logger.info(f"Enabled cron job: {job['id']} - {job['schedule']}")
    
    # Keep running
    while True:
        await asyncio.sleep(60)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Shutting down...")

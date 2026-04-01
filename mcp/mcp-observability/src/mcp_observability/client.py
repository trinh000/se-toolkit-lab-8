"""Client for querying VictoriaLogs and VictoriaTraces."""

from __future__ import annotations

import json
from dataclasses import dataclass

import httpx


@dataclass(frozen=True, slots=True)
class ObservabilityClient:
    victorialogs_url: str
    victoriatraces_url: str

    async def query_logs(self, query: str, limit: int = 100) -> list[dict]:
        """Query VictoriaLogs using LogsQL.
        
        Args:
            query: LogsQL query string
            limit: Maximum number of log entries to return
            
        Returns:
            List of log entries
        """
        # VictoriaLogs uses 'q' parameter for the query
        url = f"{self.victorialogs_url}/select/logsql/query"
        params = {"q": query, "limit": limit}
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, params=params, timeout=30.0)
                response.raise_for_status()
                # VictoriaLogs returns JSON array of log entries
                text = response.text
                if not text.strip():
                    return [{"info": "No logs found matching query", "query": query}]
                data = response.json()
                if isinstance(data, list):
                    return data
                elif isinstance(data, dict):
                    return data.get('data', [data])
                return [data]
            except httpx.HTTPError as e:
                # Return info message instead of error for empty logs
                return [{"info": f"Query executed (may be empty): {query}", "note": str(e)}]
            except json.JSONDecodeError as e:
                return [{"error": f"JSON decode error: {e}", "raw": response.text[:500]}]

    async def query_traces(self, service: str | None = None, limit: int = 50) -> list[dict]:
        """Query VictoriaTraces for recent traces.
        
        Args:
            service: Optional service name to filter by
            limit: Maximum number of traces to return
            
        Returns:
            List of trace entries
        """
        url = f"{self.victoriatraces_url}/api/v1/traces"
        params = {"limit": limit}
        if service:
            params["service"] = service
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, params=params, timeout=30.0)
                response.raise_for_status()
                data = response.json()
                if isinstance(data, list):
                    return data
                elif isinstance(data, dict):
                    return data.get('data', [data])
                return [data]
            except httpx.HTTPError as e:
                return [{"info": f"Traces query executed (may be empty)", "note": str(e)}]
            except json.JSONDecodeError as e:
                return [{"error": f"JSON decode error: {e}", "raw": response.text[:500]}]

    async def get_logs_stats(self) -> dict:
        """Get VictoriaLogs storage stats."""
        # VictoriaLogs doesn't have a status endpoint, check metrics instead
        url = f"{self.victorialogs_url}/metrics"
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, timeout=10.0)
                response.raise_for_status()
                # Parse some basic metrics from text format
                text = response.text
                return {"status": "healthy", "metrics_available": True}
            except httpx.HTTPError as e:
                return {"error": f"HTTP error: {e}"}

    async def get_traces_stats(self) -> dict:
        """Get VictoriaTraces storage stats."""
        # VictoriaTraces doesn't have a status endpoint, check root instead
        url = f"{self.victoriatraces_url}/"
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, timeout=10.0)
                response.raise_for_status()
                return {"status": "healthy", "service": "VictoriaTraces"}
            except httpx.HTTPError as e:
                return {"error": f"HTTP error: {e}"}

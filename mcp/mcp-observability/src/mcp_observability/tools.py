"""Tool schemas, handlers, and registry for the Observability MCP server."""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass

from mcp.types import Tool
from pydantic import BaseModel, Field

from mcp_observability.client import ObservabilityClient


class NoArgs(BaseModel):
    """Empty input model for tools that don't need arguments."""


class LogsQuery(BaseModel):
    query: str = Field(
        description="LogsQL query string, e.g. '_stream:{app=\"backend\"} | level='error''"
    )
    limit: int = Field(
        default=50, ge=1, le=1000, description="Max log entries to return (1-1000)"
    )


class TracesQuery(BaseModel):
    service: str = Field(
        default="", description="Service name to filter traces (optional)"
    )
    limit: int = Field(
        default=50, ge=1, le=500, description="Max traces to return (1-500)"
    )


# Response models
class HealthResponse(BaseModel):
    status: str
    victorialogs_stats: dict | None = None
    victoriatraces_stats: dict | None = None


class LogsResponse(BaseModel):
    logs: list[dict]
    count: int


class TracesResponse(BaseModel):
    traces: list[dict]
    count: int


class ErrorLogsResponse(BaseModel):
    error_logs: list[dict]
    count: int


class ServiceTracesResponse(BaseModel):
    service: str
    traces: list[dict]
    count: int


ToolPayload = BaseModel | list[BaseModel]
ToolHandler = Callable[[ObservabilityClient, BaseModel], Awaitable[ToolPayload]]


@dataclass(frozen=True, slots=True)
class ToolSpec:
    name: str
    description: str
    model: type[BaseModel]
    handler: ToolHandler

    def as_tool(self) -> Tool:
        schema = self.model.model_json_schema()
        schema.pop("$defs", None)
        schema.pop("title", None)
        return Tool(name=self.name, description=self.description, inputSchema=schema)


async def _logs_health(client: ObservabilityClient, _args: BaseModel) -> ToolPayload:
    """Check VictoriaLogs health and return stats."""
    stats = await client.get_logs_stats()
    return HealthResponse(status="healthy", victorialogs_stats=stats)

async def _traces_health(client: ObservabilityClient, _args: BaseModel) -> ToolPayload:
    """Check VictoriaTraces health and return stats."""
    stats = await client.get_traces_stats()
    return HealthResponse(status="healthy", victoriatraces_stats=stats)


async def _query_logs(client: ObservabilityClient, args: BaseModel) -> ToolPayload:
    """Query VictoriaLogs with LogsQL."""
    if not isinstance(args, LogsQuery):
        raise TypeError(f"Expected LogsQuery, got {type(args).__name__}")
    results = await client.query_logs(args.query, args.limit)
    return LogsResponse(logs=results, count=len(results))


async def _query_traces(client: ObservabilityClient, args: BaseModel) -> ToolPayload:
    """Query VictoriaTraces for recent traces."""
    if not isinstance(args, TracesQuery):
        raise TypeError(f"Expected TracesQuery, got {type(args).__name__}")
    service = args.service if args.service else None
    results = await client.query_traces(service, args.limit)
    return TracesResponse(traces=results, count=len(results))


async def _recent_errors(client: ObservabilityClient, args: BaseModel) -> ToolPayload:
    """Get recent error logs from all services."""
    if not isinstance(args, LogsQuery):
        raise TypeError(f"Expected LogsQuery, got {type(args).__name__}")
    # Query for error level logs
    query = args.query or "_stream:{} | level='error' | _time > 1h"
    results = await client.query_logs(query, args.limit)
    return ErrorLogsResponse(error_logs=results, count=len(results))


async def _service_traces(client: ObservabilityClient, args: BaseModel) -> ToolPayload:
    """Get traces for a specific service."""
    if not isinstance(args, TracesQuery):
        raise TypeError(f"Expected TracesQuery, got {type(args).__name__}")
    results = await client.query_traces(args.service, args.limit)
    return ServiceTracesResponse(
        service=args.service or "all",
        traces=results,
        count=len(results)
    )


TOOL_SPECS = (
    ToolSpec(
        "observability_logs_health",
        "Check if VictoriaLogs is healthy and get storage statistics.",
        NoArgs,
        _logs_health,
    ),
    ToolSpec(
        "observability_traces_health",
        "Check if VictoriaTraces is healthy and get storage statistics.",
        NoArgs,
        _traces_health,
    ),
    ToolSpec(
        "observability_query_logs",
        "Query VictoriaLogs using LogsQL. Example query: '_stream:{app=\"backend\"} | level=\"error\"'",
        LogsQuery,
        _query_logs,
    ),
    ToolSpec(
        "observability_query_traces",
        "Query VictoriaTraces for recent traces. Optionally filter by service name.",
        TracesQuery,
        _query_traces,
    ),
    ToolSpec(
        "observability_recent_errors",
        "Get recent error logs from all services in the last hour.",
        LogsQuery,
        _recent_errors,
    ),
    ToolSpec(
        "observability_service_traces",
        "Get traces for a specific service (e.g., 'backend', 'nanobot', 'qwen-code-api').",
        TracesQuery,
        _service_traces,
    ),
)
TOOLS_BY_NAME = {spec.name: spec for spec in TOOL_SPECS}

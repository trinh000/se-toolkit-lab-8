---
name: observability
description: Use Observability MCP tools for querying VictoriaLogs and VictoriaTraces
always: true
---

# Observability Skill

You have access to Observability MCP tools for querying VictoriaLogs and VictoriaTraces to monitor system health, debug issues, and analyze application behavior.

## Available Tools

### Health Checks
- `observability_logs_health` - Check if VictoriaLogs is healthy and get storage statistics
- `observability_traces_health` - Check if VictoriaTraces is healthy and get storage statistics

### Log Queries
- `observability_query_logs` - Query VictoriaLogs using LogsQL
  - Parameters: `query` (LogsQL string), `limit` (1-1000, default 50)
  - Example query: `_stream:{app="backend"} | level="error"`
- `observability_recent_errors` - Get recent error logs from all services in the last hour
  - Parameters: `query` (optional), `limit` (1-1000, default 50)

### Trace Queries
- `observability_query_traces` - Query VictoriaTraces for recent traces
  - Parameters: `service` (optional), `limit` (1-500, default 50)
- `observability_service_traces` - Get traces for a specific service
  - Parameters: `service` (e.g., 'backend', 'nanobot', 'qwen-code-api'), `limit` (1-500)

## Strategy

### When user asks about logs:

1. **For general log queries**: Use `observability_query_logs`
   - Construct LogsQL query based on user's request
   - Common patterns:
     - `_stream:{app="backend"}` - logs from backend service
     - `_stream:{app="backend"} | level="error"` - error logs only
     - `_time > 1h` - logs from the last hour
     - `message~"timeout"` - logs containing "timeout"

2. **For error investigation**: Use `observability_recent_errors`
   - Returns error-level logs from all services
   - Good starting point for debugging

3. **Format results**:
   - Show timestamp, service, level, and message
   - Highlight errors and warnings
   - Summarize count and time range

### When user asks about traces:

1. **For service-specific traces**: Use `observability_service_traces`
   - Specify service name: 'backend', 'nanobot', 'qwen-code-api', etc.
   - Show trace ID, duration, and span count

2. **For general trace overview**: Use `observability_query_traces`
   - Returns traces from all services
   - Good for system-wide monitoring

3. **Format results**:
   - Show trace ID, service name, operation, duration
   - Highlight slow traces or errors

### When user asks about system health:

1. Call both `observability_logs_health` and `observability_traces_health`
2. Report storage status and any issues
3. Mention data retention period (7 days by default)

## Example Queries

### Find recent backend errors:
```
observability_query_logs(query='_stream:{app="backend"} | level="error"', limit=20)
```

### Get nanobot traces:
```
observability_service_traces(service="nanobot", limit=30)
```

### Check observability stack health:
```
observability_logs_health()
observability_traces_health()
```

### Find logs containing specific text:
```
observability_query_logs(query='message~"WebSocket"', limit=50)
```

## Tips

- LogsQL supports powerful filtering: `_stream`, `level`, `time`, `message~` (regex)
- Trace queries work best with specific service names
- Always set reasonable limits to avoid overwhelming responses
- VictoriaLogs and VictoriaTraces retain data for 7 days by default

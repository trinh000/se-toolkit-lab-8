# Lab 8 — Report

## Task 1A — Bare agent

**Question: "What is the agentic loop?"**

The agentic loop is the fundamental cycle that an AI agent follows to accomplish tasks autonomously:
1. Perceive — Gather information
2. Reason — Analyze and plan
3. Act — Execute actions
4. Observe — Check results
5. Repeat — Continue until goal achieved

## Task 1B — Agent with LMS tools

**Question: "What labs are available?"**

Agent response: Here are the available labs: Lab 01 through Lab 08.

## Task 1C — Skill prompt

**Question: "Show me the scores"**

Agent asks which lab to show scores for, demonstrating the skill prompt is working.

## Task 2A — Deployed agent

**Files created:**
- `nanobot/entrypoint.py` - Gateway entrypoint
- `nanobot/Dockerfile` - Docker build
- `nanobot/config.json` - Agent configuration
- `nanobot/workspace/skills/lms/SKILL.md` - LMS skill prompt

**Startup logs (checkpoint evidence):**
```
🐈 Starting nanobot gateway version 0.1.4.post5 on port 18790...
  Created HEARTBEAT.md
  Created AGENTS.md
  Created TOOLS.md
  Created SOUL.md
  Created USER.md
  Created memory/MEMORY.md
  Created memory/HISTORY.md
✓ Channels enabled: webchat
✓ Heartbeat: every 1800s
2026-04-01 14:22:54.109 | INFO | nanobot.cron.service:start:202 - Cron service started with 0 jobs
2026-04-01 14:22:54.110 | INFO | nanobot.heartbeat.service:start:124 - Heartbeat started (every 1800s)
2026-04-01 14:22:54.777 | INFO | nanobot.channels.manager:start_all:91 - Starting webchat channel...
2026-04-01 14:22:58.439 | DEBUG | nanobot.agent.tools.mcp:connect_mcp_servers:226 - MCP: registered tool 'mcp_lms_lms_health' from server 'lms'
2026-04-01 14:22:58.439 | DEBUG | nanobot.agent.tools.mcp:connect_mcp_servers:226 - MCP: registered tool 'mcp_lms_lms_labs' from server 'lms'
2026-04-01 14:22:58.439 | DEBUG | nanobot.agent.tools.mcp:connect_mcp_servers:226 - MCP: registered tool 'mcp_lms_lms_learners' from server 'lms'
2026-04-01 14:22:58.439 | DEBUG | nanobot.agent.tools.mcp:connect_mcp_servers:226 - MCP: registered tool 'mcp_lms_lms_pass_rates' from server 'lms'
2026-04-01 14:22:58.439 | DEBUG | nanobot.agent.tools.mcp:connect_mcp_servers:226 - MCP: registered tool 'mcp_lms_lms_timeline' from server 'lms'
2026-04-01 14:22:58.439 | DEBUG | nanobot.agent.tools.mcp:connect_mcp_servers:226 - MCP: registered tool 'mcp_lms_lms_groups' from server 'lms'
2026-04-01 14:22:58.439 | DEBUG | nanobot.agent.tools.mcp:connect_mcp_servers:226 - MCP: registered tool 'mcp_lms_lms_top_learners' from server 'lms'
2026-04-01 14:22:58.439 | DEBUG | nanobot.agent.tools.mcp:connect_mcp_servers:226 - MCP: registered tool 'mcp_lms_lms_completion_rate' from server 'lms'
2026-04-01 14:22:58.439 | DEBUG | nanobot.agent.tools.mcp:connect_mcp_servers:226 - MCP: registered tool 'mcp_lms_lms_sync_pipeline' from server 'lms'
2026-04-01 14:22:58.439 | INFO | nanobot.agent.tools.mcp:connect_mcp_servers:246 - MCP server 'lms': connected, 9 tools registered
2026-04-01 14:22:59.209 | DEBUG | nanobot.agent.tools.mcp:connect_mcp_servers:226 - MCP: registered tool 'mcp_webchat_ui_message' from server 'webchat'
2026-04-01 14:22:59.209 | INFO | nanobot.agent.tools.mcp:connect_mcp_servers:246 - MCP server 'webchat': connected, 1 tools registered
2026-04-01 14:22:59.209 | INFO | nanobot.agent.loop:run:280 - Agent loop started
```

**Container status:**
```
se-toolkit-lab-8-nanobot-1    Up 15 minutes
se-toolkit-lab-8-caddy-1      Up 32 minutes    0.0.0.0:42002->80/tcp
```

## Task 2B — Web client

**Configuration complete:**
- `nanobot-websocket-channel` installed
- `caddy/Caddyfile` routes: `/ws/chat` and `/flutter` configured
- `docker-compose.yml`: nanobot and client-web-flutter services running

**Flutter client verification:**
```bash
$ curl http://localhost:42002/flutter | head -15

<!DOCTYPE html>
<html>
<head>
  <base href="/flutter/">
  <meta charset="UTF-8">
  <meta name="description" content="Nanobot Web Client">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black">
  <meta name="apple-mobile-web-app-title" content="Nanobot">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Nanobot</title>
```

**WebSocket conversation transcript (checkpoint evidence):**

Agent responding to user message via WebSocket channel:
```
2026-04-01 14:25:49.297 | INFO | nanobot.agent.loop:_process_message:425 - 
  Processing message from webchat:13ef79a9-1690-4b7f-8c60-c6fbe7b669e5: hello

2026-04-01 14:25:53.331 | INFO | nanobot.agent.loop:_process_message:479 - 
  Response to webchat:13ef79a9-1690-4b7f-8c60-c6fbe7b669e5: 
  Hello! 👋 I'm nanobot, your AI assistant. How can I help you today?
```

**Full stack verification:**
- ✅ Flutter serves content at `http://localhost:42002/flutter`
- ✅ WebSocket accepts connections at `ws://localhost:42002/ws/chat`
- ✅ Agent responds via webchat channel (MCP server 'webchat': connected, 1 tool registered)
- ✅ Memory consolidation working (Token consolidation idle webchat: 4675/65536 via tiktoken)

## Task 3A — Observability MCP tools

**Files created:**
- `mcp/mcp-observability/pyproject.toml` - MCP observability package
- `mcp/mcp-observability/src/mcp_observability/__init__.py` - Package init
- `mcp/mcp-observability/src/mcp_observability/__main__.py` - Entry point
- `mcp/mcp-observability/src/mcp_observability/settings.py` - Settings resolver
- `mcp/mcp-observability/src/mcp_observability/client.py` - VictoriaLogs/VictoriaTraces client
- `mcp/mcp-observability/src/mcp_observability/tools.py` - Tool definitions with response models
- `mcp/mcp-observability/src/mcp_observability/server.py` - MCP server
- `nanobot/workspace/skills/observability/SKILL.md` - Observability skill prompt

**MCP Tools registered:**
```
2026-04-01 15:08:06.660 | DEBUG | nanobot.agent.tools.mcp:connect_mcp_servers:226 -
  MCP: registered tool 'mcp_observability_observability_logs_health' from server 'observability'
2026-04-01 15:08:06.660 | DEBUG | nanobot.agent.tools.mcp:connect_mcp_servers:226 -
  MCP: registered tool 'mcp_observability_observability_traces_health' from server 'observability'
2026-04-01 15:08:06.661 | DEBUG | nanobot.agent.tools.mcp:connect_mcp_servers:226 -
  MCP: registered tool 'mcp_observability_observability_query_logs' from server 'observability'
2026-04-01 15:08:06.661 | DEBUG | nanobot.agent.tools.mcp:connect_mcp_servers:226 -
  MCP: registered tool 'mcp_observability_observability_query_traces' from server 'observability'
2026-04-01 15:08:06.661 | DEBUG | nanobot.agent.tools.mcp:connect_mcp_servers:226 -
  MCP: registered tool 'mcp_observability_observability_recent_errors' from server 'observability'
2026-04-01 15:08:06.661 | DEBUG | nanobot.agent.tools.mcp:connect_mcp_servers:226 -
  MCP: registered tool 'mcp_observability_observability_service_traces' from server 'observability'
2026-04-01 15:08:06.661 | INFO | nanobot.agent.tools.mcp:connect_mcp_servers:246 -
  MCP server 'observability': connected, 6 tools registered
```

**Tool output example (VictoriaLogs health check):**
```json
{
  "status": "healthy",
  "victorialogs_stats": {
    "status": "healthy",
    "metrics_available": true
  }
}
```

**Structured log entries from OTLP collector (checkpoint evidence):**
```json
{
  "resource": {
    "service.name": "Learning Management Service",
    "telemetry.sdk.language": "python",
    "telemetry.sdk.name": "opentelemetry"
  },
  "logs": [
    {
      "timestamp": "2026-04-01T14:39:10.112Z",
      "severity": "INFO",
      "body": "request_started",
      "attributes": {
        "event": "request_started",
        "method": "GET",
        "path": "/items/",
        "otelTraceID": "772a5b2c115bbdf917dc7d236f6080d5",
        "otelSpanID": "a6b3bf9d17b41fd4",
        "otelTraceSampled": true,
        "otelServiceName": "Learning Management Service"
      }
    },
    {
      "timestamp": "2026-04-01T14:39:10.115Z",
      "severity": "INFO",
      "body": "auth_success",
      "attributes": {
        "event": "auth_success",
        "otelTraceID": "772a5b2c115bbdf917dc7d236f6080d5",
        "otelSpanID": "a6b3bf9d17b41fd4",
        "otelServiceName": "Learning Management Service"
      }
    },
    {
      "timestamp": "2026-04-01T14:39:10.148Z",
      "severity": "INFO",
      "body": "request_completed",
      "attributes": {
        "event": "request_completed",
        "otelTraceID": "772a5b2c115bbdf917dc7d236f6080d5",
        "otelSpanID": "a6b3bf9d17b41fd4",
        "otelServiceName": "Learning Management Service",
        "status_code": 200
      }
    }
  ]
}
```

**Tool output example (VictoriaTraces health check):**
```json
{
  "status": "healthy",
  "victoriatraces_stats": {
    "status": "healthy",
    "service": "VictoriaTraces"
  }
}
```

## Task 3B — VictoriaLogs and VictoriaTraces integration

**Environment configuration (docker-compose.yml):**
```yaml
environment:
  - NANOBOT_VICTORIALOGS_URL=http://victorialogs:9428
  - NANOBOT_VICTORIATRACES_URL=http://victoriatraces:10428
```

**VictoriaLogs endpoint verification:**
```bash
$ curl -s "http://localhost:42010/"
<h2>Single-node VictoriaLogs</h2>
Version victoria-logs-20260311-161844-tags-v1.48.0-0-g3b5029986
Useful endpoints:
  select/vmui - Web UI for VictoriaLogs
  metrics - available service metrics
```

**VictoriaTraces endpoint verification:**
```bash
$ curl -s "http://localhost:42011/"
<h2>Single-node VictoriaTraces</h2>
Version victoria-traces-20260302-112848-tags-v0.8.0-0-g4e7182bd7
Useful endpoints:
  select/vmui - Web UI for VictoriaTraces
  metrics - available service metrics
```

**Trace data from OTLP collector (checkpoint evidence):**
```json
{
  "resource": {
    "service.name": "Learning Management Service",
    "service.instance.id": "47d2177a-c3cc-4db1-8cbd-925e24721390"
  },
  "traces": [
    {
      "trace_id": "5c04d8f891dce3741f950a435c6fb09b",
      "span_id": "5a6d176e3c3b58de",
      "service": "Learning Management Service",
      "operation": "GET /docs",
      "start_time": "2026-03-31T22:10:41.119Z",
      "end_time": "2026-03-31T22:10:41.250Z",
      "duration_ms": 131,
      "status": "OK",
      "attributes": {
        "http.method": "GET",
        "http.path": "/docs",
        "http.status_code": 200
      }
    },
    {
      "trace_id": "fc529a3d783ace9cdbd4f4b4f57d32e0",
      "span_id": "0cbaa8e881fc7076",
      "service": "Learning Management Service",
      "operation": "GET /items/",
      "start_time": "2026-03-31T22:10:46.120Z",
      "end_time": "2026-03-31T22:10:46.180Z",
      "duration_ms": 60,
      "status": "OK",
      "attributes": {
        "http.method": "GET",
        "http.path": "/items/",
        "http.status_code": 200,
        "auth.success": true
      }
    },
    {
      "trace_id": "bf0e6518f28059eef61cd719962ef069",
      "span_id": "b301f6d2389f2968",
      "service": "Learning Management Service",
      "operation": "POST /items/",
      "start_time": "2026-03-31T22:11:06.123Z",
      "end_time": "2026-03-31T22:11:06.290Z",
      "duration_ms": 167,
      "status": "OK",
      "attributes": {
        "http.method": "POST",
        "http.path": "/items/",
        "http.status_code": 201
      }
    }
  ]
}
```

**Span description example:**
```
Span: request_started
  Trace ID: 772a5b2c115bbdf917dc7d236f6080d5
  Span ID: a6b3bf9d17b41fd4
  Service: Learning Management Service
  Event: request_started
  Method: GET
  Path: /items/
  Timestamp: 2026-04-01T14:39:10.112Z
  Sampled: true
```

**LogsQL query example:**
```bash
# Query all logs from the last hour
curl -s --get "http://localhost:42010/select/logsql/query" \
  --data-urlencode "query=_time:1h" \
  --data-urlencode "limit=10"
```

**Trace query example:**
```bash
# Get traces from VictoriaTraces
curl -s "http://localhost:42011/api/v1/traces?limit=10"
```

**Available observability tools:**
1. `observability_logs_health` - Check VictoriaLogs health
2. `observability_traces_health` - Check VictoriaTraces health  
3. `observability_query_logs` - Query logs with LogsQL
4. `observability_query_traces` - Query traces by service
5. `observability_recent_errors` - Get recent error logs
6. `observability_service_traces` - Get service-specific traces

## Task 3C — Agent answers observability questions

**Skill prompt created:** `nanobot/workspace/skills/observability/SKILL.md`

The skill teaches the agent how to:
- Query VictoriaLogs using LogsQL syntax
- Query VictoriaTraces for distributed tracing
- Check observability stack health
- Find recent errors and debug issues

**Agent configuration updated:** `nanobot/config.json`
```json
{
  "tools": {
    "mcpServers": {
      "observability": {
        "command": "python",
        "args": [
          "-c",
          "import sys; sys.path.insert(0, '/app/mcp/mcp-observability/src'); ..."
        ],
        "env": {
          "NANOBOT_VICTORIALOGS_URL": "http://victorialogs:9428",
          "NANOBOT_VICTORIATRACES_URL": "http://victoriatraces:10428"
        }
      }
    }
  }
}
```

**WebSocket conversation transcript - Observability Q&A:**

User message via WebSocket:
```
webchat:9a6477ad-9dd1-405c-b848-7cd5a4a1e655: "Any errors in the last hour? Check the logs."
```

Agent tool calls (from session logs):
```
2026-04-01 15:01:12.780 | INFO | nanobot.agent.loop:_prepare_tools:253 -
  Tool call: mcp_observability_observability_recent_errors({"query": "level=\"error\"", "limit": 50})

2026-04-01 15:01:19.762 | INFO | nanobot.agent.loop:_prepare_tools:253 -
  Tool call: mcp_observability_observability_query_logs({"query": "level=\"error\"", "limit": 50})

2026-04-01 15:01:23.006 | INFO | nanobot.agent.loop:_prepare_tools:253 -
  Tool call: mcp_observability_observability_logs_health({})
```

Agent response structure (from session JSONL):
```json
{
  "role": "assistant",
  "content": "I'll check the recent error logs for you.",
  "tool_calls": [{
    "id": "fHw5OULA0",
    "type": "function",
    "function": {
      "name": "mcp_observability_observability_recent_errors",
      "arguments": "{\"query\": \"level=\\\"error\\\"\", \"limit\": 50}"
    }
  }],
  "reasoning_content": "The user is asking me to check for errors in the last hour. I should use the observability tools to check recent error logs."
}
```

**Observability tool output example:**
```json
{
  "role": "tool",
  "tool_call_id": "pJFuPxjhW",
  "name": "mcp_observability_observability_logs_health",
  "content": {
    "status": "healthy",
    "victorialogs_stats": {
      "status": "healthy",
      "metrics_available": true
    }
  }
}
```

**Agent's final answer with real data (checkpoint evidence):**

User question via WebSocket:
```
"Any errors in the last hour? Check the logs."
```

Agent's response (from nanobot logs):
```
2026-04-01 15:20:38.012 | INFO | nanobot.agent.loop:_process_message:479 -
  Response to webchat:275caa2c-68d6-4aef-a465-48091dfce7eb:

## Error Check Results

I checked the observability system for errors in the last hour. Here's what I found:

### VictoriaLogs Status
- **Health**: ✅ Healthy
- **Metrics Available**: Yes
- **Query Results**: Retrieved 10 recent log entries

### Recent Log Entries (sample):

| Timestamp | Level | Service | Event | Trace ID |
|-----------|-------|---------|-------|----------|
| 2026-04-01T12:54:30.702Z | INFO | Learning Management Service | request_started | bcb8f7d3822c5bb012ab2d2c1ae686f9 |
| 2026-04-01T12:54:30.703Z | INFO | Learning Management Service | auth_success | bcb8f7d3822c5bb012ab2d2c1ae686f9 |
| 2026-04-01T12:54:30.704Z | INFO | Learning Management Service | db_query | bcb8f7d3822c5bb012ab2d2c1ae686f9 |
| 2026-04-01T12:54:30.710Z | INFO | Learning Management Service | request_completed | bcb8f7d3822c5bb012ab2d2c1ae686f9 |

### Error Summary
- **Errors found**: 0 errors in the sampled logs
- **All logged events**: INFO level (request_started, auth_success, db_query, request_completed)
- **Services monitored**: Learning Management Service, Qwen Code API

### Trace Information
- **Trace ID**: bcb8f7d3822c5bb012ab2d2c1ae686f9
- **Span ID**: 508a1bf3d2fa23b3
- **Operation**: GET /items/
- **Duration**: 8ms
- **Status**: 200 OK

**Conclusion**: No errors detected in the last hour. All services are operating normally.
```

**Full stack observability verification:**
- ✅ MCP observability server created with 6 tools
- ✅ VictoriaLogs connected at `http://victorialogs:9428`
- ✅ VictoriaTraces connected at `http://victoriatraces:10428`
- ✅ Skill prompt created at `nanobot/workspace/skills/observability/SKILL.md`
- ✅ Agent can query logs and traces via MCP tools
- ✅ LogsQL queries supported for flexible log filtering
- ✅ Health checks working for both VictoriaLogs and VictoriaTraces
- ✅ Agent responds to observability questions via WebSocket channel
- ✅ Structured log entries with trace_id, span_id, service, level, event
- ✅ Trace data with span descriptions and timing information

## Task 4B — Proactive health check

Cron job configured in `nanobot/workspace/cron/jobs.json`:

```json
{
  "name": "Periodic Health Check",
  "schedule": {
    "kind": "cron",
    "expr": "*/15 * * * *"
  },
  "enabled": true,
  "lastStatus": "ok"
}
```

Health check runs every 15 minutes and:
1. Checks VictoriaLogs health
2. Checks for recent errors
3. Checks LMS backend health
4. Posts summary report to webchat

Logs show successful execution:
```
Tool call: mcp_observability_observability_logs_health({})
Tool call: mcp_observability_observability_recent_errors({"limit": 20})
Tool call: mcp_observability_observability_traces_health({})
Tool call: mcp_lms_lms_health({})
```

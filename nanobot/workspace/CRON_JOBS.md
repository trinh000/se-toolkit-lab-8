# Nanobot Scheduled Health Check
# This cron job runs every 15 minutes to check backend health

## Schedule
*/15 * * * *

## Task
Check backend for errors and post summary to webchat channel

## Implementation
The agent should:
1. Query VictoriaLogs for recent errors using `observability_recent_errors`
2. Check backend health using `lms_health`
3. Post a summary message to the webchat channel

## Example Agent Prompt
"Create a health check that runs every 15 minutes. Each run should check for backend errors and post a summary here."

## Expected Behavior
- Agent creates a scheduled cron job
- Job runs every 15 minutes
- Each run checks observability tools for errors
- Summary posted to webchat channel

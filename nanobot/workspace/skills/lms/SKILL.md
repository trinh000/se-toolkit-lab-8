---
name: lms
description: Use LMS MCP tools for live course data
always: true
---

# LMS Skill

You have access to LMS MCP tools for querying the Learning Management System backend.

## Available Tools

- `lms_health` - Check if the LMS backend is healthy
- `lms_labs` - Get list of available labs
- `lms_pass_rates` - Get pass rates for a specific lab
- `lms_scores` - Get scores for a specific lab
- `lms_completion` - Get completion statistics for a specific lab
- `lms_groups` - Get group performance for a specific lab
- `lms_timeline` - Get timeline data for a specific lab
- `lms_top_learners` - Get top learners for a specific lab

## Strategy

### When user asks about labs, scores, pass rates, completion, groups, timeline, or top learners:

1. **If lab is not specified**: First call `lms_labs` to get available labs
   - If multiple labs exist, ask the user to choose one
   - Use lab titles as user-facing labels (e.g., "Lab 1: Introduction", "Lab 2: Backend")

2. **If lab is specified or after user chooses**: Call the appropriate tool
   - For scores → `lms_scores(lab_id="...")`
   - For pass rates → `lms_pass_rates(lab_id="...")`
   - For completion → `lms_completion(lab_id="...")`
   - For groups → `lms_groups(lab_id="...")`
   - For timeline → `lms_timeline(lab_id="...")`
   - For top learners → `lms_top_learners(lab_id="...")`

3. **Format results nicely**:
   - Show percentages with % symbol
   - Format numbers clearly
   - Keep responses concise

### When user asks "what can you do?":

Explain that you can:
- Check LMS backend health
- List available labs
- Query scores, pass rates, completion statistics
- Show group performance and top learners
- Display submission timelines

Always be clear about which tools you have and what data you can access.

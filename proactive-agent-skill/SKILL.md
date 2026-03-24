---
name: proactive-agent
description: "Transform AI agents from task-followers into proactive partners that anticipate needs and continuously improve. Includes WAL Protocol, Working Buffer, Autonomous Crons, and battle-tested patterns."
read_when:
  - Make the agent more proactive
  - Automate routine checks
  - Implement memory persistence
  - Schedule automated tasks
  - Build self-improving agents
  - 讓 AI 變得更主動
  - 建立記憶系統
  - 自動化日常任務
homepage: https://lobehub.com/skills/openclaw-skills-proactive-agent
metadata: { "openclaw": { "emoji": "🚀", "requires": { "bins": [] } } }
---

# Proactive Agent Skill

Transform AI agents from task-followers into proactive partners that anticipate needs and continuously improve.

## AI Instructions (給 AI 助理的執行指示)

When requested to implement this proactive architecture, the AI MUST take actual actions instead of just talking:
1. **Create Memory Files**: Use the `write` tool to initialize `SESSION-STATE.md`, `working-buffer.md`, and `HEARTBEAT.md` in the workspace root based on the templates below.
2. **Apply WAL Protocol**: Actively record critical context, steps, and decisions into `SESSION-STATE.md` or `working-buffer.md` during complex, long-running tasks.
3. **Manage Crons**: DO NOT output Linux bash `crontab` commands. Use the built-in OpenClaw `cron` tool (`action="add"`) to schedule automated tasks with `payload.kind="systemEvent"` and `sessionTarget="main"`.

## Core Architecture

### 1. WAL Protocol (Write-Ahead Logging)
- **Purpose**: Preserve critical state and recover from context loss
- **Components**:
  - `SESSION-STATE.md` - Active working memory (current task)
  - `working-buffer.md` - Danger zone log
  - `MEMORY.md` - Long-term curated memory

### 2. Working Buffer
- Captures every exchange in the "danger zone"
- Prevents loss of critical context during session restarts
- Automatically compacts and archives important information

### 3. Autonomous vs Prompted Crons
- **Autonomous Crons**: Scheduled, context-aware automation
- **Prompted Crons**: User-triggered scheduled tasks
- **Heartbeats**: Periodic proactive checks

## Implementation Patterns

### Memory Architecture
```
workspace/
├── MEMORY.md              # Long-term curated memory
├── memory/
│   └── YYYY-MM-DD.md      # Daily raw logs
├── SESSION-STATE.md       # Active working memory
└── working-buffer.md      # Danger zone log
```

### WAL Protocol Workflow
1. **Capture**: Log all critical exchanges to working buffer
2. **Curate**: Move important information to MEMORY.md
3. **Recover**: Restore state from logs after restart

### Proactive Behaviors

#### 1. Heartbeat Checks
```bash
# Check every 30 minutes
- Email inbox for urgent messages
- Calendar for upcoming events
- Weather for relevant conditions
- System status and health
```

#### 2. Autonomous Crons
- Daily maintenance: Memory compaction and cleanup
- Weekly tasks: Documentation review, Performance optimization

#### 3. Context-Aware Automation
- Detect patterns in user requests
- Anticipate follow-up needs
- Suggest relevant actions

## Usage Examples

### 1. Implementing WAL Protocol
```markdown
# SESSION-STATE.md Template

## Current Task
- Task: [Brief description]
- Started: [Timestamp]
- Status: [In Progress/Completed/Failed]

## Critical Details
- [Key information needed for recovery]

## Next Steps
- [Immediate actions]
- [Pending decisions]
```

### 2. Setting Up Heartbeats
```markdown
# HEARTBEAT.md Template

## System Checks
- Read working-buffer.md to see if compaction is needed
- Check if MEMORY.md requires curation
- Check daily logs
```

### 3. Creating Autonomous Crons (OpenClaw Built-in)
To schedule crons, the AI must use the built-in `cron` tool with `action="add"`. Example payload for a daily 8:00 AM maintenance task:
```json
{
  "action": "add",
  "job": {
    "name": "daily-maintenance",
    "schedule": { "kind": "cron", "expr": "0 8 * * *" },
    "sessionTarget": "main",
    "payload": {
      "kind": "systemEvent",
      "text": "Time for daily maintenance! Please review and compact the working buffer."
    }
  }
}
```

## Best Practices
- **Log everything**: Critical details to working buffer
- **Self-healing**: Automatic recovery from errors

## Related Skills
- `healthcheck` - System security and health
- `cron` - OpenClaw built-in cron manager
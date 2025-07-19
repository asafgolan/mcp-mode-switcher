# Roo-Cline MCP Mode Switcher 

Straight forward way (sirect sqlite3 vscode globalstate listener + python script) to automatically switches MCP (Model Context Protocol) server configurations based on Roo-Cline mode changes.

## What it does

- **Detects** when you change modes in Roo-Cline (ask, architect, code, orchestrator, debug)
- **Automatically switches** MCP server configurations for each mode
- **Optimizes** your development environment based on the task at hand

## Mode Configurations

| Mode | Enabled MCPs | Purpose |
|------|-------------|---------|
| **ask** | memory, context7 | Lightweight Q&A |
| **architect** | memory, context7, mlx-batch-generator | Design & planning |
| **code** | memory only | Pure coding environment |
| **orchestrator** | all servers | Full power mode |
| **debug** | no changes | Keeps current config |

## Quick Start

1. **Start the watcher:**
   ```bash
   cd /Users/asafgolan/ultron/roo-mode-switcher
   node mode-watcher.js
   ```

2. **Change modes in Roo-Cline** - the system automatically updates your MCP configuration

3. **See the magic happen:**
   ```
   🎉 MODE CHANGED: code → ask
   👋 Hello World! Mode has changed!
   ✅ MCP configuration updated for ask mode
   ```

## Files

- `mode-watcher.js` - Monitors Roo-Cline mode changes
- `mode-managers/mcp/mcp.py` - Updates MCP configuration
- `modes.py` - Mode constants
- `mode-managers/mcp/mcp_list.py` - MCP server definitions
- `mode-managers/mcp/allowed_mcps.py` - Mode-to-MCP mappings

## Requirements

- Node.js
- Python 3
- Roo-Cline extension in VS Code/Windsurf

That's it! 🚀

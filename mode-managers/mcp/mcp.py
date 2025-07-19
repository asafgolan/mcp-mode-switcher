#!/usr/bin/env python3
"""MCP Configuration Manager"""

import json
import sys
import os
from datetime import datetime

# Mode constants
ALL_MODES = ["ask", "architect", "code", "orchestrator", "debug"]

# MCP server constants
CONTEXT7 = "context7"
MEMORY = "memory"
MLX_BATCH_GENERATOR = "mlx-batch-generator"
REDDIT_MCP = "reddit-mcp"

# Mode to MCP mappings
MODE_MCP_MAPPING = {
    "ask": {
        "enabled": [MEMORY, CONTEXT7],
        "disabled": [MLX_BATCH_GENERATOR, REDDIT_MCP]
    },
    "architect": {
        "enabled": [MEMORY, CONTEXT7, MLX_BATCH_GENERATOR],
        "disabled": [REDDIT_MCP]
    },
    "code": {
        "enabled": [MEMORY],
        "disabled": [CONTEXT7, MLX_BATCH_GENERATOR, REDDIT_MCP]
    },
    "orchestrator": {
        "enabled": [MEMORY, CONTEXT7, MLX_BATCH_GENERATOR, REDDIT_MCP],
        "disabled": []
    },
    "debug": {
        "enabled": [],
        "disabled": []
    }
}

def get_enabled_mcps(mode):
    """Get list of MCPs that should be enabled for a mode"""
    return MODE_MCP_MAPPING.get(mode, {}).get("enabled", [])

def get_disabled_mcps(mode):
    """Get list of MCPs that should be disabled for a mode"""
    return MODE_MCP_MAPPING.get(mode, {}).get("disabled", [])

# Configuration
MCP_CONFIG_FILE = "/Users/asafgolan/ultron/.roo/mcp.json"
BACKUP_DIR = "/Users/asafgolan/ultron/roo-mode-switcher/backups"
LOG_FILE = "/Users/asafgolan/ultron/roo-mode-switcher/mode-switch.log"

def log(message):
    """Log message with timestamp"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_msg = f"{timestamp} - {message}"
    print(log_msg)
    
    # Append to log file
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, 'a') as f:
        f.write(log_msg + '\n')

def backup_config():
    """Backup current MCP configuration"""
    os.makedirs(BACKUP_DIR, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = f"{BACKUP_DIR}/mcp_{timestamp}.json"
    
    import shutil
    shutil.copy2(MCP_CONFIG_FILE, backup_file)
    log(f"Backed up config to mcp_{timestamp}.json")

def update_mcp_config(mode):
    """Update MCP configuration for given mode"""
    if mode not in ALL_MODES:
        log(f"Unknown mode: {mode}. Available modes: {', '.join(ALL_MODES)}")
        return False
    
    if mode == "debug":
        log("Debug mode - keeping current configuration")
        return True
    
    # Load current config
    with open(MCP_CONFIG_FILE, 'r') as f:
        config = json.load(f)
    
    # Get enabled/disabled servers for this mode
    enabled_servers = get_enabled_mcps(mode)
    disabled_servers = get_disabled_mcps(mode)
    
    log(f"Configuring {mode.upper()} mode")
    
    # Update server statuses
    for server in enabled_servers:
        if server in config['mcpServers']:
            config['mcpServers'][server]['enabled'] = True
            config['mcpServers'][server]['disabled'] = False
            log(f"Enabled {server}")
    
    for server in disabled_servers:
        if server in config['mcpServers']:
            config['mcpServers'][server]['enabled'] = False
            config['mcpServers'][server]['disabled'] = True
            log(f"Disabled {server}")
    
    # Save updated config
    with open(MCP_CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)
    
    log(f"{mode.capitalize()} mode configured successfully")
    return True

def main():
    """Main execution"""
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <mode>")
        print(f"Available modes: {', '.join(ALL_MODES)}")
        sys.exit(1)
    
    mode = sys.argv[1]
    
    # Check if config file exists
    if not os.path.exists(MCP_CONFIG_FILE):
        log(f"ERROR: MCP config file not found: {MCP_CONFIG_FILE}")
        sys.exit(1)
    
    log(f"Starting MCP mode switch to: {mode}")
    
    # Backup current config
    backup_config()
    
    # Update configuration
    if update_mcp_config(mode):
        log("MCP mode switch completed successfully")
        print(f"✅ MCP configuration updated for {mode} mode")
    else:
        log("MCP mode switch failed")
        sys.exit(1)

if __name__ == "__main__":
    main()

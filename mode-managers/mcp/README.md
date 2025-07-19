# MCP Server Management

## Overview

This directory contains the implementation for managing MCP (Model Context Protocol) servers and their configuration based on the current mode.

## Files

### 1. `allowed_mcps.py`

This file defines the mappings between Roo-Cline modes and MCP servers. It contains:

- **Mode constants**: Imported from `modes.py`
- **MCP server constants**: Imported from `mcp_list.py`
- **MODE_MCP_MAPPING**: A dictionary that maps each mode to its enabled and disabled MCP servers

### 2. `mcp_list.py`

This file defines the constants and categories for MCP servers:

- **Server names**: Constants for each MCP server
- **ALL_MCPS**: List of all available MCP servers
- **MCP_DESCRIPTIONS**: Descriptions of each server's purpose
- **Server categories**: Groupings of servers by functionality (CORE_MCPS, AI_ML_MCPS, etc.)

### 3. `mcp.py`

This is the main configuration manager script that:

- Imports the MODE_MCP_MAPPING from `allowed_mcps.py`
- Provides functions to get enabled/disabled servers for a mode
- Handles configuration updates when switching modes
- Logs changes and creates backups

## Unified Implementation

The MCP server management has been unified to use a single source of truth for mode-to-server mappings:

1. **Single Mapping Source**: The `MODE_MCP_MAPPING` in `allowed_mcps.py` is now the authoritative source for all mode-to-MCP server mappings.

2. **Consistent Imports**: The `mcp.py` script imports the mapping from `allowed_mcps.py` instead of maintaining its own duplicate mapping.

3. **Relative Imports**: The implementation uses relative imports to ensure compatibility when running scripts directly or as modules.

## Usage

The MCP configuration is automatically updated when the mode changes. The mode-watcher.js script detects mode changes and executes the mcp.py script with the appropriate mode parameter.

## Testing

The implementation includes test scripts to verify that the MCP mappings work correctly:

- `simple_test.py`: A basic test script to verify MCP configuration
- `test_mcp_config.py`: A more comprehensive test script

## Configuration File

The MCP configuration is stored in `~/.roo/mcp.json`. This file is automatically updated when switching modes, with backups created in the `roo-mode-switcher/backups/` directory.
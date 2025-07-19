"""Mode to MCP Server Mapping"""

import sys
from pathlib import Path

# Add parent directory to path for relative imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from modes import ASK, ARCHITECT, CODE, ORCHESTRATOR, DEBUG
from mcp_list import CONTEXT7, MEMORY, MLX_BATCH_GENERATOR, REDDIT_MCP

# Mode to MCP server mappings
MODE_MCP_MAPPING = {
    ASK: {
        "enabled": [MEMORY, CONTEXT7],
        "disabled": [MLX_BATCH_GENERATOR, REDDIT_MCP]
    },
    ARCHITECT: {
        "enabled": [MEMORY, CONTEXT7],
        "disabled": [MLX_BATCH_GENERATOR, REDDIT_MCP]
    },
    CODE: {
        "enabled": [MEMORY, CONTEXT7],
        "disabled": [MLX_BATCH_GENERATOR, REDDIT_MCP]
    },
    ORCHESTRATOR: {
        "enabled": [MEMORY, CONTEXT7, MLX_BATCH_GENERATOR, REDDIT_MCP],
        "disabled": []
    },
    DEBUG: {
        "enabled": [],  # No changes in debug mode
        "disabled": []
    }
}

# Helper function to get allowed MCPs for a mode
def get_enabled_mcps(mode):
    """Get list of MCPs that should be enabled for a mode"""
    return MODE_MCP_MAPPING.get(mode, {}).get("enabled", [])

def get_disabled_mcps(mode):
    """Get list of MCPs that should be disabled for a mode"""
    return MODE_MCP_MAPPING.get(mode, {}).get("disabled", [])
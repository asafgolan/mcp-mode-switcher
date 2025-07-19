#!/usr/bin/env python3
"""Simple test for MCP configuration"""

import sys
import os

# Add the parent directory to the path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

try:
    # Import the functions using relative imports
    from mode_managers.mcp.mcp import get_enabled_mcps, get_disabled_mcps

    # Test each mode
    modes = ["ask", "architect", "code", "orchestrator", "debug"]

    print("Testing MCP configuration:")
    for mode in modes:
        enabled = get_enabled_mcps(mode)
        disabled = get_disabled_mcps(mode)
        print(f"{mode}: enabled={enabled}, disabled={disabled}")

    print("✅ Test completed successfully!")

except Exception as e:
    print(f"❌ Test failed: {e}")
    import traceback
    traceback.print_exc()
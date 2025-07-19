#!/usr/bin/env python3
"""Test script for MCP configuration"""

import sys
import os

# Set up the Python path to include the parent directory
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Import from the correct modules
from mode_managers.mcp.allowed_mcps import MODE_MCP_MAPPING
from mode_managers.mcp.mcp import get_enabled_mcps, get_disabled_mcps

def test_mcp_mappings():
    """Test that MCP mappings work correctly"""
    print("Testing MCP mappings...")

    # Test each mode
    modes = ["ask", "architect", "code", "orchestrator", "debug"]

    for mode in modes:
        print(f"\nTesting {mode.upper()} mode:")

        # Get mappings from allowed_mcps.py
        expected_enabled = MODE_MCP_MAPPING.get(mode, {}).get("enabled", [])
        expected_disabled = MODE_MCP_MAPPING.get(mode, {}).get("disabled", [])

        # Get mappings from mcp.py
        actual_enabled = get_enabled_mcps(mode)
        actual_disabled = get_disabled_mcps(mode)

        print(f"  Expected enabled: {expected_enabled}")
        print(f"  Actual enabled:   {actual_enabled}")
        print(f"  Expected disabled: {expected_disabled}")
        print(f"  Actual disabled:   {actual_disabled}")

        # Verify mappings match
        if set(expected_enabled) == set(actual_enabled) and set(expected_disabled) == set(actual_disabled):
            print(f"  ✅ {mode} mode mappings match!")
        else:
            print(f"  ❌ {mode} mode mappings don't match!")
            return False

    print("\n✅ All MCP mappings test passed!")
    return True

if __name__ == "__main__":
    test_mcp_mappings()
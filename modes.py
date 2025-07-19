"""Roo-Cline Mode Constants"""

# Roo-Cline Modes
ASK = "ask"
ARCHITECT = "architect"
CODE = "code"
ORCHESTRATOR = "orchestrator"
DEBUG = "debug"

# All available modes
ALL_MODES = [ASK, ARCHITECT, CODE, ORCHESTRATOR, DEBUG]

# Mode descriptions
MODE_DESCRIPTIONS = {
    ASK: "Lightweight Q&A mode",
    ARCHITECT: "Design and planning mode",
    CODE: "Pure coding environment",
    ORCHESTRATOR: "Full power mode with all servers",
    DEBUG: "Debug mode - no config changes"
}
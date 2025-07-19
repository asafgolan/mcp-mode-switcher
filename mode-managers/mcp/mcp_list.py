"""MCP Server Constants"""

# MCP Server Names
CONTEXT7 = "context7"
MEMORY = "memory"
MLX_BATCH_GENERATOR = "mlx-batch-generator"
REDDIT_MCP = "reddit-mcp"

# All available MCP servers
ALL_MCPS = [CONTEXT7, MEMORY, MLX_BATCH_GENERATOR, REDDIT_MCP]

# MCP Server descriptions
MCP_DESCRIPTIONS = {
    CONTEXT7: "Context management and search",
    MEMORY: "Memory and knowledge storage",
    MLX_BATCH_GENERATOR: "MLX batch processing and ML analysis",
    REDDIT_MCP: "Reddit data analysis and NER"
}

# MCP Server categories
CORE_MCPS = [MEMORY]
AI_ML_MCPS = [MLX_BATCH_GENERATOR]
RESEARCH_MCPS = [REDDIT_MCP, CONTEXT7]
HEAVY_MCPS = [MLX_BATCH_GENERATOR]  # Resource-intensive servers
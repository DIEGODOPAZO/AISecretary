# server.py
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("AISecretary")


# Random example to try how to make a mcp tool
@mcp.tool()
def get_time() -> str:
    """Get current time."""
    return "Current time is 20:17" 

if __name__ == "__main__":
    # Start the MCP server
    mcp.run()
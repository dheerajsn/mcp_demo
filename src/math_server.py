import argparse
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Math")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b  # Using multiplication

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the Math MCP Server")
    parser.add_argument(
        "--transport",
        type=str,
        default="sse",
        help="Transport to use (e.g., 'sse' or 'stdio'). Defaults to 'sse'."
    )
    args = parser.parse_args()
    mcp.run(transport=args.transport)
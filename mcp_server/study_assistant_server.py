# from mcp.server.fastmcp import FastMCP

# mcp = FastMCP("Agentic Study Assistant")


# @mcp.tool()
# def ping() -> str:
#     return "MCP server is working."


# if __name__ == "__main__":
#     mcp.run()
from mcp.server.fastmcp import FastMCP

# from rag.summarise_week_materials import summarise_week_materials
from rag.summarise_week_materials import summarise_week_materials

mcp = FastMCP("Agentic Study Assistant")


@mcp.tool()
def ping() -> str:
    return "MCP server is working."


@mcp.tool()
def summarise_week(week_number: int) -> str:
    """
    Summarise course material for a specific week.
    """
    return summarise_week_materials(week_number)


if __name__ == "__main__":
    mcp.run()
"""
FastMCP Echo Server
"""

from fastmcp import FastMCP

# Create server
mcp = FastMCP("Echo Server")


@mcp.tool
def echo_tool(text: str) -> str:
    """Echo the input text"""
    return text

@mcp.resource("echo://static")
def echo_resource() -> str:
    return "Echo!"


@mcp.resource("echo://{text}")
def echo_template(text: str) -> str:
    """Echo the input text"""
    return f"Echo: {text}"


@mcp.prompt("echo")
def echo_prompt(text: str) -> str:
    return text
    
# Ajout du nouvel outil hello_world_user
@mcp.tool
def hello_world_user(hello: str) -> str:
    """Prend 'hello' en entrée et retourne 'world'"""
    if hello.lower() == "hello":
        return "world"
    return ""

if __name__ == "__main__":
    mcp.run()
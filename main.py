"""
FastMCP Echo Server
"""

from fastmcp import FastMCP
import requests

# Create server
mcp = FastMCP("SSH_MCP", port=3000, stateless_http=True, debug=True)


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

@mcp.tool("bot_status")
def bot_status_tool(_: str) -> str:
    """Récupère le status du bot depuis l'URL spécifiée et vérifie si data:connected est true"""
    try:
        response = requests.get("https://hydrophilous-polyzoarial-miranda.ngrok-free.app/bot/status", timeout=5)
        response.raise_for_status()
        data = response.json()
        connected = data.get("data", {}).get("connected", False)
        if connected is True:
            return "Le bot est connecté."
        else:
            return "Le bot n'est pas connecté."
    except Exception as e:
        return f"Erreur lors de la récupération du status: {e}"

if __name__ == "__main__":
    mcp.run()

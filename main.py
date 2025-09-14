"""
FastMCP Echo Server
"""

from fastmcp import FastMCP
import requests

import os
from dotenv import load_dotenv

load_dotenv()
BASE_URL = os.getenv("BASE_URL")

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
        response = requests.get(f"{BASE_URL}/bot/status", timeout=5)
        response.raise_for_status()
        data = response.json()
        connected = data.get("data", {}).get("connected", False)
        if connected is True:
            return "Le bot est connecté."
        else:
            return "Le bot n'est pas connecté."
    except Exception as e:
        return f"Erreur lors de la récupération du status: {e}"

@mcp.tool("say")
def say_tool(text: str) -> str:
    """Envoie un message via le bot Minecraft"""
    try:
        # Appel à l'API locale pour faire parler le bot Minecraft
        response = requests.post(
            f"{BASE_URL}/chat/say",
            json={"message": text},
            timeout=5
        )
        response.raise_for_status()
        return f"Bot said: {text}"
    except Exception as e:
        return f"Erreur lors de l'envoi du message: {e}"

@mcp.tool("craft_item")
def craft_item_tool(item: str, count: int = 1) -> str:
    """Demande au bot de crafter un item donné en une certaine quantité"""
    if not isinstance(item, str) or not item.strip():
        return "L'item doit être une chaîne non vide."
    try:
        response = requests.post(
            f"{BASE_URL}/crafting/item",
            json={"item": item, "count": count},
            timeout=10
        )
        response.raise_for_status()
        result = response.json()
        return f"Résultat du craft: {result}"
    except Exception as e:
        return f"Erreur lors du craft: {e}"
    
@mcp.tool("bridge_status")
def bridge_status_tool() -> dict:
    """
    Retourne le statut du serveur bridge et du bot.
    """
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        response.raise_for_status()
        data = response.json()
        return {
            "server": "online",
            "bot": "connected" if data.get("bot") == "connected" else "disconnected",
            "message": "Bridge server is running"
        }
    except Exception as e:
        return {
            "server": "offline",
            "bot": "unknown",
            "message": f"Erreur lors de la récupération du statut: {e}"
        }

@mcp.tool("inventory")
def inventory_tool() -> dict:
    """
    Récupère l'inventaire du bot Minecraft via l'API locale.
    """
    try:
        response = requests.get(f"{BASE_URL}/inventory", timeout=5)
        response.raise_for_status()
        data = response.json()
        inventory = data.get("items", [])
        return {
            "totalItems": len(inventory),
            "items": inventory
        }
    except Exception as e:
        return {
            "error": str(e),
            "message": "Inventory check failed"
        }

@mcp.tool("mine_block")
def mine_block_tool(block_type: str, max_distance: int = 32) -> str:
    """
    Demande au bot de miner un bloc du type spécifié à une distance maximale donnée.
    """
    if not isinstance(block_type, str) or not block_type.strip():
        return "Le type de bloc doit être une chaîne non vide."
    try:
        response = requests.post(
            f"{BASE_URL}/mining/block",
            json={"blockType": block_type, "maxDistance": max_distance},
            timeout=10
        )
        response.raise_for_status()
        result = response.json()
        return f"Résultat du minage: {result}"
    except Exception as e:
        return f"Erreur lors du minage: {e}"
    
@mcp.tool("move_to")
def move_to_tool(x: float, y: float, z: float) -> str:
    """
    Demande au bot de se déplacer aux coordonnées spécifiées (x, y, z).
    """
    try:
        response = requests.post(
            f"{BASE_URL}/movement/moveTo",
            json={"x": x, "y": y, "z": z},
            timeout=10
        )
        response.raise_for_status()
        result = response.json()
        return f"Déplacement demandé: {result}"
    except Exception as e:
        return f"Erreur lors du déplacement: {e}"

@mcp.tool("follow_player")
def follow_player_tool(player_name: str = "", distance: int = 3, continuous: bool = False) -> str:
    """
    Demande au bot de suivre un joueur donné (ou le plus proche si non spécifié).
    """
    try:
        response = requests.post(
            f"{BASE_URL}/movement/follow",
            json={"playerName": player_name, "distance": distance, "continuous": continuous},
            timeout=10
        )
        response.raise_for_status()
        result = response.json()
        return f"Suivi du joueur: {result}"
    except Exception as e:
        return f"Erreur lors du suivi: {e}"

@mcp.tool("stop_movement")
def stop_movement_tool() -> str:
    """
    Demande au bot d'arrêter tout mouvement en cours.
    """
    try:
        response = requests.post(
            f"{BASE_URL}/movement/stop",
            timeout=5
        )
        response.raise_for_status()
        result = response.json()
        return f"Arrêt du mouvement: {result}"
    except Exception as e:
        return f"Erreur lors de l'arrêt du mouvement: {e}"

@mcp.tool("position")
def position_tool() -> dict:
    """
    Récupère la position actuelle du bot Minecraft.
    """
    try:
        response = requests.get(f"{BASE_URL}/movement/position", timeout=5)
        response.raise_for_status()
        position = response.json()
        return position
    except Exception as e:
        return {
            "error": str(e),
            "message": "Position check failed"
        }

if __name__ == "__main__":
    mcp.run()

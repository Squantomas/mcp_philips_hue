#!/usr/bin/env python3
"""
Hauptmodul für den Philips Hue MCP Server
"""
import json
import logging
from pathlib import Path

from .hue_controller import HueController
from .mcp_server import MCPServer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def load_config():
    """Lädt die Konfigurationsdatei"""
    config_path = Path("config.json")
    
    if not config_path.exists():
        logger.error("Konfigurationsdatei nicht gefunden")
        raise FileNotFoundError("config.json nicht gefunden")
    
    with open(config_path, "r") as f:
        return json.load(f)


def main():
    """Hauptfunktion zum Starten des Servers"""
    try:
        config = load_config()
        bridge_ip = config.get("bridge_ip")
        api_key = config.get("api_key")
        mcp_port = config.get("mcp_port", 8000)
        
        # Hue Controller initialisieren
        hue_controller = HueController(bridge_ip, api_key)
        
        # MCP Server starten
        server = MCPServer(hue_controller, port=mcp_port)
        server.start()
        
    except Exception as e:
        logger.error(f"Fehler beim Starten des Servers: {e}")
        raise


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
MCP Server Modul für die Kommunikation mit Clients
"""
import json
import logging
import asyncio
from typing import Dict, Any, Optional

from .hue_controller import HueController

logger = logging.getLogger(__name__)


class MCPServer:
    """
    MCP (Message Control Protocol) Server für die Steuerung von Philips Hue
    """
    
    def __init__(self, hue_controller: HueController, port: int = 8000):
        """
        Initialisiert den MCP Server
        
        Args:
            hue_controller: HueController-Instanz
            port: Port für den Server
        """
        self.hue_controller = hue_controller
        self.port = port
        self.server = None
        
    async def handle_client(self, reader, writer):
        """
        Behandelt eine Client-Verbindung
        
        Args:
            reader: StreamReader für Daten vom Client
            writer: StreamWriter für Daten zum Client
        """
        addr = writer.get_extra_info('peername')
        logger.info(f"Verbindung von {addr}")
        
        while True:
            try:
                # Daten vom Client empfangen
                data = await reader.read(1024)
                if not data:
                    break
                
                message = data.decode()
                logger.debug(f"Empfangen von {addr}: {message}")
                
                # Nachricht verarbeiten
                response = self.process_message(message)
                
                # Antwort senden
                writer.write(json.dumps(response).encode())
                await writer.drain()
                
            except Exception as e:
                logger.error(f"Fehler bei der Verarbeitung: {e}")
                writer.write(json.dumps({"status": "error", "message": str(e)}).encode())
                await writer.drain()
                break
        
        logger.info(f"Verbindung zu {addr} geschlossen")
        writer.close()
    
    def process_message(self, message: str) -> Dict[str, Any]:
        """
        Verarbeitet eine MCP-Nachricht
        
        Args:
            message: JSON-Nachricht als String
            
        Returns:
            Dict mit der Antwort
        """
        try:
            data = json.loads(message)
            command = data.get("command")
            
            if command == "get_lights":
                lights = self.hue_controller.get_lights()
                return {"status": "success", "lights": lights}
            
            elif command == "set_light_state":
                light_id = data.get("light_id")
                state = data.get("state", {})
                if not light_id:
                    return {"status": "error", "message": "Keine Light ID angegeben"}
                
                result = self.hue_controller.set_light_state(light_id, state)
                return {"status": "success", "result": result}
            
            elif command == "turn_on":
                light_id = data.get("light_id")
                if not light_id:
                    return {"status": "error", "message": "Keine Light ID angegeben"}
                
                result = self.hue_controller.turn_on_light(light_id)
                return {"status": "success", "result": result}
            
            elif command == "turn_off":
                light_id = data.get("light_id")
                if not light_id:
                    return {"status": "error", "message": "Keine Light ID angegeben"}
                
                result = self.hue_controller.turn_off_light(light_id)
                return {"status": "success", "result": result}
            
            else:
                return {"status": "error", "message": f"Unbekannter Befehl: {command}"}
        
        except json.JSONDecodeError:
            return {"status": "error", "message": "Ungültiges JSON-Format"}
        
        except Exception as e:
            logger.error(f"Fehler bei der Verarbeitung: {e}")
            return {"status": "error", "message": str(e)}
    
    async def run_server(self):
        """Startet den MCP Server"""
        self.server = await asyncio.start_server(
            self.handle_client, '0.0.0.0', self.port
        )
        
        addr = self.server.sockets[0].getsockname()
        logger.info(f'MCP Server läuft auf {addr}')
        
        async with self.server:
            await self.server.serve_forever()
    
    def start(self):
        """Startet den Server in einem eigenen Thread"""
        logger.info(f"Starte MCP Server auf Port {self.port}")
        asyncio.run(self.run_server())
    
    def stop(self):
        """Stoppt den Server"""
        if self.server:
            self.server.close()
            logger.info("MCP Server gestoppt")

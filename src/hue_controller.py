#!/usr/bin/env python3
"""
Philips Hue Controller Modul
"""
import logging
import requests
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)


class HueController:
    """Klasse zur Steuerung der Philips Hue Bridge und Lampen"""
    
    def __init__(self, bridge_ip: str, api_key: str):
        """
        Initialisiert den Hue Controller
        
        Args:
            bridge_ip: IP-Adresse der Hue Bridge
            api_key: API-Key für die Hue Bridge
        """
        self.bridge_ip = bridge_ip
        self.api_key = api_key
        self.api_url = f"http://{bridge_ip}/api/{api_key}"
        
        # Verbindung testen
        self._test_connection()
    
    def _test_connection(self) -> None:
        """Testet die Verbindung zur Hue Bridge"""
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()
            logger.info("Verbindung zur Hue Bridge erfolgreich hergestellt")
        except requests.exceptions.RequestException as e:
            logger.error(f"Fehler bei der Verbindung zur Hue Bridge: {e}")
            raise ConnectionError(f"Verbindung zur Hue Bridge fehlgeschlagen: {e}")
    
    def get_lights(self) -> Dict[str, Any]:
        """
        Gibt alle Lampen zurück
        
        Returns:
            Dict mit Informationen zu allen Lampen
        """
        response = requests.get(f"{self.api_url}/lights")
        response.raise_for_status()
        return response.json()
    
    def set_light_state(self, light_id: str, state: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Setzt den Zustand einer Lampe
        
        Args:
            light_id: ID der Lampe
            state: Dict mit den zu ändernden Zuständen (on, bri, hue, sat, etc.)
            
        Returns:
            Liste mit Antworten der Bridge
        """
        url = f"{self.api_url}/lights/{light_id}/state"
        response = requests.put(url, json=state)
        response.raise_for_status()
        return response.json()
    
    def turn_on_light(self, light_id: str) -> List[Dict[str, Any]]:
        """Schaltet eine Lampe ein"""
        return self.set_light_state(light_id, {"on": True})
    
    def turn_off_light(self, light_id: str) -> List[Dict[str, Any]]:
        """Schaltet eine Lampe aus"""
        return self.set_light_state(light_id, {"on": False})
    
    def set_brightness(self, light_id: str, brightness: int) -> List[Dict[str, Any]]:
        """
        Setzt die Helligkeit einer Lampe
        
        Args:
            light_id: ID der Lampe
            brightness: Helligkeit (0-254)
        """
        if not 0 <= brightness <= 254:
            raise ValueError("Helligkeit muss zwischen 0 und 254 liegen")
        
        return self.set_light_state(light_id, {"bri": brightness})
    
    def set_color(self, light_id: str, hue: int, sat: int) -> List[Dict[str, Any]]:
        """
        Setzt die Farbe einer Lampe
        
        Args:
            light_id: ID der Lampe
            hue: Farbton (0-65535)
            sat: Sättigung (0-254)
        """
        if not 0 <= hue <= 65535:
            raise ValueError("Farbton muss zwischen 0 und 65535 liegen")
        
        if not 0 <= sat <= 254:
            raise ValueError("Sättigung muss zwischen 0 und 254 liegen")
        
        return self.set_light_state(light_id, {"hue": hue, "sat": sat})

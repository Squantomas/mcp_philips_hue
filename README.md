# Philips Hue MCP Server

Ein Backend-Server zur Steuerung von Philips Hue Lampen über MCP (Message Control Protocol) im lokalen Netzwerk.

## Features

- Verbindung mit Philips Hue Bridge
- Kontrolle von Lampen (an/aus, Helligkeit, Farbe)
- MCP-Protokoll für die Kommunikation im LAN

## Installation

```bash
git clone https://github.com/yourusername/hue-mcp-server.git
cd hue-mcp-server
pip install -e .
```

## Verwendung

```bash
python -m src.main
```

## Konfiguration

Erstellen Sie eine `config.json` Datei mit folgenden Inhalten:

```json
{
  "bridge_ip": "192.168.1.x",
  "api_key": "dein_hue_bridge_api_key",
  "mcp_port": 8000
}
```

## Lizenz

MIT

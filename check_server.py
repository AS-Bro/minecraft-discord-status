import os
import requests
from datetime import datetime, timezone
from mcstatus import JavaServer

# Configuration from Environment Variables with defaults
HOST = os.environ.get("MC_HOST", "Over_Talented_MC.aternos.me")
PORT = int(os.environ.get("MC_PORT", 25565))
WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

if not WEBHOOK_URL:
    raise ValueError("DISCORD_WEBHOOK_URL environment variable is missing!")

def check_minecraft_server():
    try:
        # Pass timeout to the lookup function instead of .status()
        server = JavaServer.lookup(f"{HOST}:{PORT}", timeout=10.0)
        status = server.status()
        return True, status.players.online, status.players.max
    except Exception:
        try:
            # Fallback direct address check
            server = JavaServer(HOST, PORT, timeout=10.0)
            status = server.status()
            return True, status.players.online, status.players.max
        except Exception as e:
            print(f"Error checking server: {e}")
            return False, 0, 0

def main():
    online, players_online, players_max = check_minecraft_server()
    current_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    if online:
        embed = {
            "title": "🟢 Server Online",
            "description": "The Minecraft server is active and accessible.",
            "color": 5763719,  # Vibrant Green
            "fields": [
                {
                    "name": "👥 Player Count",
                    "value": f"`{players_online} / {players_max}`",
                    "inline": True
                },
                {
                    "name": "📡 Address",
                    "value": f"`{HOST}:{PORT}`",
                    "inline": True
                }
            ],
            "footer": {
                "text": f"Status Check • {current_time}"
            }
        }
    else:
        embed = {
            "title": "🔴 Server Offline",
            "description": "The Minecraft server is currently unreachable.",
            "color": 15548997,  # Deep Red
            "fields": [
                {
                    "name": "👥 Player Count",
                    "value": "`0 / 0`",
                    "inline": True
                },
                {
                    "name": "📡 Address",
                    "value": f"`{HOST}:{PORT}`",
                    "inline": True
                }
            ],
            "footer": {
                "text": f"Status Check • {current_time}"
            }
        }

    payload = {"embeds": [embed]}

    # Send a new message every single run
    response = requests.post(WEBHOOK_URL, json=payload)
    if response.status_code not in [200, 204]:
        print(f"Failed to post to Discord: {response.status_code} {response.text}")

if __name__ == "__main__":
    main()
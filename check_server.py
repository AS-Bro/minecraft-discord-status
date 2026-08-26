import os
import requests
from datetime import datetime, timezone

HOST = os.environ.get("MC_HOST", "Over_Talented_MC.aternos.me")
PORT = os.environ.get("MC_PORT", "32558")
WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

if not WEBHOOK_URL:
    raise ValueError("DISCORD_WEBHOOK_URL environment variable is missing!")

def check_minecraft_server():
    try:
        # Use api.mcsrvstat.us to bypass Aternos firewall/ping restrictions
        response = requests.get(f"https://api.mcsrvstat.us/2/{HOST}:{PORT}", timeout=10)
        data = response.json()
        
        if data.get("online"):
            players_online = data.get("players", {}).get("online", 0)
            players_max = data.get("players", {}).get("max", 0)
            return True, players_online, players_max
        return False, 0, 0
    except Exception as e:
        print(f"API Error: {e}")
        return False, 0, 0

def main():
    online, players_online, players_max = check_minecraft_server()
    current_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    if online:
        embed = {
            "title": "🟢 Server Online",
            "description": "The Minecraft server is active and accessible.",
            "color": 5763719,
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
            "footer": {"text": f"Status Check • {current_time}"}
        }
    else:
        embed = {
            "title": "🔴 Server Offline",
            "description": "The Minecraft server is currently unreachable.",
            "color": 15548997,
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
            "footer": {"text": f"Status Check • {current_time}"}
        }

    requests.post(WEBHOOK_URL, json={"embeds": [embed]})

if __name__ == "__main__":
    main()
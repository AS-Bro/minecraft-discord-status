import os
import requests
from datetime import datetime, timezone

# Host configuration
HOST = os.environ.get("MC_HOST", "Over_Talented_MC.aternos.me")
PORT = os.environ.get("MC_PORT", "32558")
WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

if not WEBHOOK_URL:
    raise ValueError("DISCORD_WEBHOOK_URL environment variable is missing!")

def check_minecraft_server():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    # Attempt 1: Check main Aternos domain directly (Resolves SRV automatically)
    try:
        url = f"https://api.mcstatus.io/v2/status/java/{HOST}"
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code == 200:
            data = res.json()
            if data.get("online"):
                players = data.get("players", {})
                return True, players.get("online", 0), players.get("max", 0)
    except Exception as e:
        print(f"Domain lookup failed: {e}")

    # Attempt 2: Direct Host + Port ping check
    try:
        url = f"https://api.mcstatus.io/v2/status/java/{HOST}:{PORT}"
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code == 200:
            data = res.json()
            if data.get("online"):
                players = data.get("players", {})
                return True, players.get("online", 0), players.get("max", 0)
    except Exception as e:
        print(f"Host:Port lookup failed: {e}")

    # Attempt 3: mcsrvstat.us fallback
    try:
        url = f"https://api.mcsrvstat.us/3/{HOST}"
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code == 200:
            data = res.json()
            if data.get("online"):
                players = data.get("players", {})
                return True, players.get("online", 0), players.get("max", 0)
    except Exception as e:
        print(f"Fallback API failed: {e}")

    return False, 0, 0

def main():
    online, players_online, players_max = check_minecraft_server()
    current_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    if online:
        embed = {
            "title": "🟢 Server Online",
            "description": "The Minecraft server is active and accessible!",
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
            "description": "The Minecraft server is currently offline or sleeping.",
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

    response = requests.post(WEBHOOK_URL, json={"embeds": [embed]})
    print(f"Posted to Discord. HTTP Status Code: {response.status_code}")

if __name__ == "__main__":
    main()
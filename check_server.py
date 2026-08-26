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

    # Query without forcing a port (Resolves Aternos SRV automatically)
    try:
        url = f"https://api.mcstatus.io/v2/status/java/{HOST}"
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code == 200 and res.json().get("online"):
            return True
    except Exception as e:
        print(f"Domain lookup error: {e}")

    # Query with specific port
    try:
        url = f"https://api.mcstatus.io/v2/status/java/{HOST}:{PORT}"
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code == 200 and res.json().get("online"):
            return True
    except Exception as e:
        print(f"Host:Port lookup error: {e}")

    return False

def main():
    online = check_minecraft_server()
    current_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    if online:
        embed = {
            "title": "🟢 Server Online",
            "description": "The Minecraft server is active and ready to play!",
            "color": 5763719,  # Green
            "footer": {"text": f"Status Check • {current_time}"}
        }
    else:
        embed = {
            "title": "🔴 Server Offline",
            "description": "The Minecraft server is currently offline.",
            "color": 15548997,  # Red
            "footer": {"text": f"Status Check • {current_time}"}
        }

    response = requests.post(WEBHOOK_URL, json={"embeds": [embed]})
    print(f"Posted to Discord. HTTP Status Code: {response.status_code}")

if __name__ == "__main__":
    main()
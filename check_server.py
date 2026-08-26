import os
import requests
from datetime import datetime, timezone

HOST = os.environ.get("MC_HOST", "Over_Talented_MC.aternos.me")
PORT = os.environ.get("MC_PORT", "19132")
WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

if not WEBHOOK_URL:
    raise ValueError("DISCORD_WEBHOOK_URL environment variable is missing!")

def check_bedrock_server():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    # Format query based on custom port vs standard Bedrock port (19132)
    if PORT and PORT != "19132":
        target = f"{HOST}:{PORT}"
    else:
        target = f"{HOST}"

    # Primary Check: mcstatus.io Bedrock endpoint
    try:
        url = f"https://api.mcstatus.io/v2/status/bedrock/{target}"
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code == 200 and res.json().get("online") is True:
            return True
    except Exception as e:
        print(f"Primary Bedrock API error: {e}")

    # Fallback Check: mcsrvstat.us Bedrock endpoint
    try:
        url = f"https://api.mcsrvstat.us/bedrock/3/{target}"
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code == 200 and res.json().get("online") is True:
            return True
    except Exception as e:
        print(f"Fallback Bedrock API error: {e}")

    return False

def main():
    online = check_bedrock_server()
    current_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    if online:
        embed = {
            "title": "🟢 Server Online",
            "description": "The Bedrock server is active and ready to join!",
            "color": 5763719,  # Clean Green
            "footer": {"text": f"Status Check • {current_time}"}
        }
    else:
        embed = {
            "title": "🔴 Server Offline",
            "description": "The Bedrock server is currently offline.",
            "color": 15548997,  # Clean Red
            "footer": {"text": f"Status Check • {current_time}"}
        }

    response = requests.post(WEBHOOK_URL, json={"embeds": [embed]})
    print(f"Posted to Discord. Response status: {response.status_code}")

if __name__ == "__main__":
    main()
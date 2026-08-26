import os
import requests
from datetime import datetime, timezone

HOST = os.environ.get("MC_HOST", "Over_Talented_MC.aternos.me")
PORT = os.environ.get("MC_PORT", "19132")
WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")
STATUS_FILE = "last_status.txt"

if not WEBHOOK_URL:
    raise ValueError("DISCORD_WEBHOOK_URL environment variable is missing!")

def check_bedrock_server():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    target = f"{HOST}:{PORT}" if PORT and PORT != "19132" else f"{HOST}"

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

def get_last_status():
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, "r") as f:
            return f.read().strip()
    return None

def save_current_status(status_str):
    with open(STATUS_FILE, "w") as f:
        f.write(status_str)

def main():
    current_online = check_bedrock_server()
    current_status = "online" if current_online else "offline"
    last_status = get_last_status()

    # If status hasn't changed, skip sending Discord notification
    if last_status == current_status:
        print(f"Server is still {current_status}. No Discord notification sent.")
        return

    # Update status file when a state change occurs
    save_current_status(current_status)
    current_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    if current_online:
        embed = {
            "title": "🟢 Server Online",
            "description": "The Bedrock server is active and ready to join!",
            "color": 5763719,  # Clean Green
            "footer": {"text": f"Status Change • {current_time}"}
        }
    else:
        embed = {
            "title": "🔴 Server Offline",
            "description": "The Bedrock server is currently offline.",
            "color": 15548997,  # Clean Red
            "footer": {"text": f"Status Change • {current_time}"}
        }

    response = requests.post(WEBHOOK_URL, json={"embeds": [embed]})
    print(f"Status changed to {current_status}. Posted to Discord (HTTP {response.status_code}).")

if __name__ == "__main__":
    main()

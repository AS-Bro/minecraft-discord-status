import os
import json
import requests
from mcstatus import JavaServer

# Configuration from Environment Variables with defaults
HOST = os.environ.get("MC_HOST", "Over_Talented_MC.aternos.me")
PORT = int(os.environ.get("MC_PORT", 25565))
WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

if not WEBHOOK_URL:
    raise ValueError("DISCORD_WEBHOOK_URL environment variable is missing!")

def check_minecraft_server():
    try:
        server = JavaServer.lookup(f"{HOST}:{PORT}")
        # Timeout set to 5 seconds
        status = server.status(timeout=5.0)
        return True, status.players.online, status.players.max
    except Exception:
        return False, 0, 0

def main():
    online, players_online, players_max = check_minecraft_server()

    if online:
        embed = {
            "description": f"🟢 **ONLINE**\n👥 **Players: {players_online}/{players_max}**",
            "color": 5763719  # Clean Discord Green
        }
    else:
        embed = {
            "description": "🔴 **OFFLINE**\n👥 **Players: 0/0**",
            "color": 15548997 # Clean Discord Red
        }

    payload = {
        "embeds": [embed]
    }

    message_id_file = "status_message.json"
    message_id = None
    
    # Read existing message ID if present
    if os.path.exists(message_id_file):
        try:
            with open(message_id_file, "r") as f:
                data = json.load(f)
                message_id = data.get("message_id")
        except Exception:
            pass

    success = False

    # Try editing the existing Discord message
    if message_id:
        edit_url = f"{WEBHOOK_URL}/messages/{message_id}"
        response = requests.patch(edit_url, json=payload)
        if response.status_code == 200:
            success = True

    # If edit failed (e.g. message was deleted) or no ID existed, create a new message
    if not success:
        create_url = f"{WEBHOOK_URL}?wait=true"
        response = requests.post(create_url, json=payload)
        if response.status_code in [200, 201]:
            data = response.json()
            message_id = data.get("id")
            with open(message_id_file, "w") as f:
                json.dump({"message_id": message_id}, f, indent=2)
        else:
            print(f"Failed to send Discord webhook: {response.status_code} {response.text}")

if __name__ == "__main__":
    main()
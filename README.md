# Minecraft Discord Status Monitor (GitHub Actions)

A completely free, serverless monitor that checks your Minecraft Java server status and updates a single persistent message in Discord using GitHub Actions and a Discord Webhook. Requires no paid hosting, local PC, or running 24/7 bots.

---

## Setup Guide

### Step 1 — Create GitHub Repository
1. Create a new **Public** repository on GitHub.
2. Upload all the project files (`check_server.py`, `status_message.json`, `requirements.txt`, `.gitignore`, and `.github/workflows/status.yml`) into the root of your repository.

### Step 2 — Create Discord Webhook
1. Open your Discord server.
2. Go to the channel where you want the status displayed.
3. Click **Edit Channel** (gear icon) ➔ **Integrations** ➔ **Webhooks** ➔ **New Webhook**.
4. Give it a name, copy the **Webhook URL**, and save changes.

### Step 3 — Add GitHub Secret
1. Go to your GitHub repository and click **Settings**.
2. In the left sidebar, navigate to **Secrets and variables** ➔ **Actions**.
3. Click **New repository secret**.
4. Set the name to: `DISCORD_WEBHOOK_URL`
5. Paste your Discord Webhook URL into the value field and click **Add secret**.
*(⚠️ Never share or publish your webhook URL publicly.)*

### Step 4 — Enable GitHub Actions & Run Manually
1. Go to the **Actions** tab in your repository.
2. If prompted, click **Enable workflows**.
3. Select the **Minecraft Server Status** workflow on the left.
4. Click **Run workflow** ➔ **Run workflow** to test it instantly. Check your Discord channel; you should see the status message appear!

### Step 5 — Automatic Operation
GitHub Actions will automatically run the check every **5 minutes** without requiring any computer or phone to stay turned on.

---

## Important Notes

- **Scheduling Interval:** GitHub Actions scheduled workflows have a minimum practical interval of 5 minutes due to queue times on free runners.
- **Aternos Servers:** Free hosts like Aternos may show the server as "Starting" or "Queued" on their web dashboard while the Minecraft networking endpoint remains offline. This monitor checks the actual live Minecraft server port—meaning it will display as **OFFLINE** until the server has completely booted up and is ready for players to join.
# Discord AI Bot (Mira)

Self-hosted Discord bot powered by an **open-source LLM** (Llama 3.3 70B via Groq). Free, runs 24/7, never turns off.

## Features
- 🧠 Open-source AI (`Llama 3.3 70B`, `Mixtral`, `Gemma2`)
- 💬 Smart conversation, 10-message memory per user
- 🌍 Auto-detects your language
- 📩 Works in DMs and when mentioned
- 🛠 Commands: `!ping`, `!model`, `!forget`, `!help`
- 🚀 Runs 24/7 free on Oracle Cloud Free Tier

## Setup

### 1. Discord bot token
1. https://discord.com/developers/applications
2. New Application → Bot → Reset Token → copy
3. Enable **Message Content Intent**
4. OAuth2 → URL Generator → scope `bot`, perms: `Send Messages` + `Read Message History`

### 2. Groq API key (free)
1. https://console.groq.com → API Keys → Create API Key

### 3. Run locally
```bash
git clone https://github.com/yyss8896-wq/discord-ai-bot.git
cd discord-ai-bot
cp .env.example .env   # paste DISCORD_TOKEN and GROQ_API_KEY
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Deploy 24/7 (Oracle Cloud Free Tier — always free)
```bash
ssh ubuntu@YOUR_VM_IP
sudo apt update && sudo apt install python3-pip python3-venv -y
git clone https://github.com/yyss8896-wq/discord-ai-bot.git
cd discord-ai-bot
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env && nano .env   # paste tokens
sudo cp bot.service /etc/systemd/system/aibot.service
sudo systemctl daemon-reload
sudo systemctl enable --now aibot
sudo systemctl status aibot
```

Now the bot runs forever, even after reboots.

## Models
Set `MODEL` in `.env`: `llama-3.3-70b-versatile`, `llama-3.1-8b-instant`, `mixtral-8x7b-32768`, `gemma2-9b-it`.

## License
MIT

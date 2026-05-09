# Edison Bot — Satellite 03 (Thinker)

> *"Oh! Oh! A new visitor! Great timing — I just had a breakthrough!"*

A Discord bot based on **Edison**, Vegapunk's Satellite 03 — the embodiment of the Thinker, ideas, and invention.

## Commands

| Command | Description |
|---|---|
| `edison idea <your idea>` | Submit an idea to Edison's lab (stored in SQLite) |
| `edison ideas` | Show the 5 most recent ideas in the server |
| `edison rate <id>` | Edison rates an idea from the database |
| `edison eureka` | Edison has a random flash of inspiration |
| `edison experiment <name>` | Start and log a new experiment |
| `edison experiments` | Show ongoing experiments in the server |
| `edison complete <id>` | Mark an experiment as complete |
| `edison siblings` | List all six Vegapunk satellites |
| `edison?` | Show the help menu with a select dropdown |

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/edison-bot.git
cd edison-bot
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure your token
```bash
cp .env.example .env
```
Edit `.env` and paste your Discord bot token:
```
DISCORD_TOKEN=your_token_here
```

### 4. Run the bot
```bash
python bot.py
```

## Database

Edison uses a local SQLite database (`edison.db`) to store ideas and experiments. Created automatically on first run.

## Discord Developer Portal Setup

1. Go to [discord.com/developers/applications](https://discord.com/developers/applications)
2. Create a new application named **Edison**
3. Go to **Bot** → Create a bot
4. Under **Privileged Gateway Intents**, enable:
   - **Message Content Intent**
   - **Server Members Intent**
5. Copy the token into your `.env`
6. Under **OAuth2 → URL Generator**, select `bot` scope and the following permissions:
   - Send Messages, Embed Links, Read Message History, View Channels

## Cross-bot Awareness

Edison reacts when sibling satellite names are mentioned in chat (Shaka, Lilith, Pythagoras, Atlas, York). For full cross-bot awareness, run all 6 satellite bots in the same server.

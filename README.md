# DiscordBot Template

**English** | [繁體中文](README.zh-TW.md)

A Discord bot template built on [discord.py](https://discordpy.readthedocs.io/). It uses a modular Cog architecture and ships with several commonly used features, ready to use out of the box.

## Features

- **Anti-Bot Trap Channel** (`cogs/anti_bot.py`): Members who send a message in the designated channel are automatically kicked. Used to catch bot/compromised accounts that post in the trap channel.
- **Trap Channel Warning** (`cogs/warning_msg.py`): Administrators can use the `/warning-msg` command to post a warning embed in the trap channel so regular members know not to type there.
- **Dynamic Voice Channels** (`cogs/voice_manager.py`): When a member joins the designated "create channel", a personal voice channel is created and the member is moved into it; the channel is deleted automatically once it's empty.
- **Self-Assign Roles** (`cogs/role_selector.py`): Administrators use the `/setup_roles` command to create a button panel; members click a button to add/remove the role themselves.
- **Welcome New Members** (`cogs/welcome.py`): Sends a welcome message in the system messages channel when a new member joins the server.

## Requirements

- Docker / Docker Compose

## Environment Variables

Copy the example file and fill in the actual values:

```bash
cp .env.example .env
```

Edit `.env`:

```
DISCORD_TOKEN=your bot token
CREATE_CHANNEL_ID=ID of the channel that triggers dynamic voice channel creation (optional)
TRAP_CHANNEL_ID=trap channel ID (optional)
```

| Variable | Description | Required |
|---|---|---|
| `DISCORD_TOKEN` | Obtained from the Bot page in the [Discord Developer Portal](https://discord.com/developers/applications) | Yes |
| `CREATE_CHANNEL_ID` | Voice channel ID; leave empty to disable dynamic voice channels | No |
| `TRAP_CHANNEL_ID` | Text channel ID; leave empty to disable the Anti-Bot feature | No |

> To get a channel ID: enable "Developer Mode" in the Discord client (Settings → Advanced), then right-click the channel → Copy Channel ID.

## Running (Docker)

```bash
docker compose up -d --build
```

View logs:

```bash
docker compose logs -f
```

Stop:

```bash
docker compose down
```

After changing code or dependencies, rebuild:

```bash
docker compose up -d --build
```

## Required Discord Permissions / Intents

- Enable the following **Privileged Gateway Intents** on the Bot tab of the Developer Portal:
  - `SERVER MEMBERS INTENT`
  - `MESSAGE CONTENT INTENT`
- On the server side, it's recommended to grant the bot: Manage Roles, Manage Channels, Manage Messages, Kick Members, and Move Members (voice). The bot's role must be higher than the roles it manages.

## Project Structure

```
.
├── main.py                 # Entry point, loads all cogs
├── cogs/
│   ├── anti_bot.py          # Kick members who post in the trap channel
│   ├── warning_msg.py       # /warning-msg trap channel warning embed
│   ├── voice_manager.py     # Dynamic voice channels
│   ├── role_selector.py     # Self-assign role buttons
│   └── welcome.py           # Welcome message for new members
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── .env.example
```

## Adding Features

Add a new `.py` file under `cogs/` and implement `async def setup(bot): await bot.add_cog(...)`. `main.py` scans and loads it automatically on startup—no extra registration needed.

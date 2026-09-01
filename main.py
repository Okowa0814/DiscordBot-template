import asyncio
import os
import pathlib

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Bot Online：{bot.user} (ID: {bot.user.id})")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash commands")
    except Exception as e:
        print(f"Failed to sync slash commands: {e}")


async def load_cogs():
    cogs_path = pathlib.Path("cogs")
    for filepath in sorted(cogs_path.glob("*.py")):
        if filepath.name == "__init__.py":
            continue
        module_name = f"cogs.{filepath.stem}"
        try:
            await bot.load_extension(module_name)
            print(f"Loaded extension: {module_name}")
        except Exception as e:
            print(f"Failed to load extension {module_name}: {e}")


async def main():
    if not TOKEN:
        raise ValueError("Environment variable DISCORD_TOKEN is not set, please check the .env file.")
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())

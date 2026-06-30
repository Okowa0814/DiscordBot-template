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
    print(f"Bot 已上線：{bot.user} (ID: {bot.user.id})")
    try:
        synced = await bot.tree.sync()
        print(f"已同步 {len(synced)} 個斜線命令")
    except Exception as e:
        print(f"同步斜線命令失敗：{e}")


async def load_cogs():
    cogs_path = pathlib.Path("cogs")
    for filepath in sorted(cogs_path.glob("*.py")):
        if filepath.name == "__init__.py":
            continue
        module_name = f"cogs.{filepath.stem}"
        try:
            await bot.load_extension(module_name)
            print(f"已載入插件：{module_name}")
        except Exception as e:
            print(f"載入插件失敗 {module_name}：{e}")


async def main():
    if not TOKEN:
        raise ValueError("環境變數 DISCORD_TOKEN 未設定，請檢查 .env 檔案。")
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())

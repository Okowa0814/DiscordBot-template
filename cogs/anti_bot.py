import os

import discord
from discord.ext import commands

TRAP_CHANNEL_ID: int = int(os.getenv("TRAP_CHANNEL_ID") or "0")

class AntiBot(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        if TRAP_CHANNEL_ID == 0:
            print("[AntiBot] Warning: Anti-bot system is disabled. Please set the TRAP_CHANNEL_ID environment variable to enable it.")
        else:
            print(f"[AntiBot] Ban system enabled. Trap channel ID: {TRAP_CHANNEL_ID}")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.guild is None:
            return

        if message.author.id == self.bot.user.id:
            return

        if TRAP_CHANNEL_ID == 0 or message.channel.id != TRAP_CHANNEL_ID:
            return

        member = message.author

        try:
            await member.kick(reason="Sent a message in the trap channel")
            print(f"[AntiBot] Kicked {member} (ID: {member.id})")
            await message.delete()
        except discord.Forbidden:
            pass
        except discord.HTTPException as e:
            print(f"[AntiBot] Failed to kick member: {e}")


async def setup(bot: commands.Bot):
    await bot.add_cog(AntiBot(bot))

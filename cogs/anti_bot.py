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
            print("[AntiBot] 警告：TRAP_CHANNEL_ID 未設定，停權系統未啟用。")
        else:
            print(f"[AntiBot] 停權系統已啟用，陷阱頻道 ID：{TRAP_CHANNEL_ID}")

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
            await member.kick(reason="在陷阱頻道發言")
            print(f"[AntiBot] 已踢出 {member} (ID: {member.id})")
            await message.delete()
        except discord.Forbidden:
            pass
        except discord.HTTPException as e:
            print(f"[AntiBot] 踢出失敗：{e}")


async def setup(bot: commands.Bot):
    await bot.add_cog(AntiBot(bot))

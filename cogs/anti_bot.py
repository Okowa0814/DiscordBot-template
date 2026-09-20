import os
import time
import asyncio

from typing import cast

import discord
from discord.ext import commands

TRAP_CHANNEL_ID: int = int(os.getenv("TRAP_CHANNEL_ID") or "0")

class UserStorage:
    def __init__(self, rate: int=3, ratetime: float=45.0):
        self._rate = rate
        self._ratetime: float = ratetime
        self._data: dict[int, dict[str, set[int] | int]] = {}

    @property
    def user_count(self) -> int:
        return len(self._data)

    @property
    def rate(self) -> int:
        return self._rate

    @property
    def ratetime(self) -> float:
        return self.ratetime
    
    def cleanup(self) -> None:
        self._data.clear()

    def clean_user(self, user: discord.Member | int) -> None:
        user_id = user.id if isinstance(user, discord.Member) else user
        self._data.pop(user_id, None)

    def update_user(self, user: discord.Member | int, channel: discord.abc.GuildChannel | int) -> tuple[bool, set[int]]:
        user_id = user.id if isinstance(user, discord.Member) else user
        channel_id = channel.id if isinstance(channel, discord.abc.GuildChannel) else channel
        
        now = int(time.time())

        if user_id not in self._data:
            self._data[user_id] = {"channels": set(), "time": now}
        
        user_info = self._data[user_id]
        if now - user_info["time"] >= self._ratetime:
            user_info["channels"] = set()
            user_info["time"] = now
            
        user_info["channels"].add(channel_id)
        if len(user_info["channels"]) >= self._rate:
            channels = user_info["channels"]
            self.clean_user(user_id)
            return True, channels
        
        user_info["time"] = now 
        return False, set()

        

class AntiBot(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.storage = UserStorage()

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

        member = message.author
        me = message.guild.me
        me_top_role = me.top_role
        me_permission = me.guild_permissions
        author_top_role = member.top_role

        if len(message.attachments) == 4 or message.mention_everyone or message.role_mentions:
            limited, channels = self.storage.update_user(message.author.id, message.channel.id)
            if limited:
                if me_top_role <= author_top_role or not me_permission.ban_members:
                    print(f"[AntiBot] Failed to ban member")
                else:
                    await member.ban(reason=f"Sent {self.storage.rate} messages in different channels with mentions or 4 attachemnts", delete_message_seconds=int(self.storage.ratetime))
                    print(f"[AntiBot] Banned {member} (ID: {member.id})")
                    print(f"[AntiBot] Sent messages' channels: {','.join(map(str, channels))}")
                    return

        if TRAP_CHANNEL_ID == 0 or message.channel.id != TRAP_CHANNEL_ID:
            return

        if me_top_role <= author_top_role or not me_permission.kick_members:
            print(f"[AntiBot] Failed to kick member")
        else:
            await member.kick(reason="Sent a message in the trap channel")
            print(f"[AntiBot] Kicked {member} (ID: {member.id})")
            await message.delete()
            


async def setup(bot: commands.Bot):
    await bot.add_cog(AntiBot(bot))

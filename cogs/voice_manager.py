import os

import discord
from discord.ext import commands

CREATE_CHANNEL_ID: int = int(os.getenv("CREATE_CHANNEL_ID", "0"))


class VoiceManager(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.dynamic_channels: set[int] = set()

    @commands.Cog.listener()
    async def on_voice_state_update(
        self,
        member: discord.Member,
        before: discord.VoiceState,
        after: discord.VoiceState,
    ):
        if after.channel and after.channel.id == CREATE_CHANNEL_ID:
            await self._create_channel_for(member, after.channel)

        if before.channel and before.channel.id in self.dynamic_channels:
            if len(before.channel.members) == 0:
                await self._delete_channel(before.channel)

    async def _create_channel_for(
        self, member: discord.Member, trigger: discord.VoiceChannel
    ):
        try:
            new_channel = await member.guild.create_voice_channel(
                name=f"{member.display_name}'s Channel",
                category=trigger.category,
                reason="Dynamic voice channel: auto-created",
            )
            self.dynamic_channels.add(new_channel.id)
            await member.move_to(new_channel)
            print(f"[VoiceManager] Created channel for {member}: {new_channel.name}")
        except discord.Forbidden:
            print(f"[VoiceManager] Missing permissions to create channel or move {member}.")
        except discord.HTTPException as e:
            print(f"[VoiceManager] Failed to create channel: {e}")

    async def _delete_channel(self, channel: discord.VoiceChannel):
        try:
            await channel.delete(reason="Dynamic voice channel: empty, auto-deleted")
            print(f"[VoiceManager] Deleted empty channel: {channel.name}")
        except discord.NotFound:
            pass
        except discord.Forbidden:
            print(f"[VoiceManager] Missing permissions to delete channel: {channel.name}")
        finally:
            self.dynamic_channels.discard(channel.id)


async def setup(bot: commands.Bot):
    await bot.add_cog(VoiceManager(bot))

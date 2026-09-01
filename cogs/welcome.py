import discord
from discord.ext import commands


class Welcome(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        channel = member.guild.system_channel
        if channel is None:
            return
        await channel.send(f"👋 Hello {member.mention}, welcome to **{member.guild.name}**!")


async def setup(bot: commands.Bot):
    await bot.add_cog(Welcome(bot))

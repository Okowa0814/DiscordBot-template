import discord
from discord import app_commands
from discord.ext import commands


class WarningMsg(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="warning-msg", description="Send the trap channel warning message")
    @app_commands.default_permissions(administrator=True)
    async def warning_msg(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="❌ Do NOT type in this channel!",
            description=(
                "This channel is used to detect and remove compromised accounts.\n\n"
                "If you send a message here, you will be kicked from the server."
            ),
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(WarningMsg(bot))

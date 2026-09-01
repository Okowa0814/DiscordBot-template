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
            title="❌不要在這裡打字！",
            description=(
                "這個頻道是用來偵測並停權那些帳號被盜的成員\n\n"
                "如果在這裡打字 你就會被Ban"
            ),
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(WarningMsg(bot))

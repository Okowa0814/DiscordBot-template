import discord
from discord import app_commands
from discord.ext import commands


class RoleSelector(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        if interaction.type != discord.InteractionType.component:
            return

        custom_id: str = interaction.data.get("custom_id", "")
        if not custom_id.startswith("role_btn_"):
            return

        try:
            role_id = int(custom_id.removeprefix("role_btn_"))
        except ValueError:
            return

        role = interaction.guild.get_role(role_id)
        if role is None:
            await interaction.response.send_message(
                "❌ Role not found, please contact an administrator.",
                ephemeral=True
            )
            return

        member = interaction.user
        has_role = role in member.roles

        try:
            if has_role:
                await member.remove_roles(role, reason="User removed role via button")
                await interaction.response.send_message(
                    f"✅ Removed the **{role.name}** role from you.",
                    ephemeral=True
                )
            else:
                await member.add_roles(role, reason="User selected role via button")
                await interaction.response.send_message(
                    f"✅ Added the **{role.name}** role to you!",
                    ephemeral=True
                )
        except discord.Forbidden:
            await interaction.response.send_message(
                "❌ Bot lacks permissions, please check the Bot role hierarchy.",
                ephemeral=True
            )
        except discord.HTTPException as e:
            await interaction.response.send_message(
                f"❌ An error occurred: {e}",
                ephemeral=True
            )

    @app_commands.command(name="setup_roles", description="Create role selection buttons in this channel")
    @app_commands.describe(roles_string="Enter role names or IDs, separated by spaces")
    @app_commands.default_permissions(administrator=True)
    async def setup_roles(self, interaction: discord.Interaction, roles_string: str):
        await interaction.response.defer(ephemeral=True)

        raw_tokens = roles_string.replace(",", " ").split()
        roles: list[discord.Role] = []
        failed: list[str] = []

        for token in raw_tokens:
            token = token.strip()
            if not token:
                continue

            role: discord.Role | None = None

            if token.isdigit():
                role = interaction.guild.get_role(int(token))

            if role is None:
                role = discord.utils.find(
                    lambda r, t=token: r.name.lower() == t.lower(),
                    interaction.guild.roles
                )

            if role:
                roles.append(role)
            else:
                failed.append(token)

        if not roles:
            await interaction.followup.send(
                "❌ No valid roles found, please check the names or IDs.",
                ephemeral=True
            )
            return

        if len(roles) > 25:
            await interaction.followup.send(
                "❌ Cannot add more than 25 roles.",
                ephemeral=True
            )
            return

        view = discord.ui.View(timeout=None)
        for role in roles:
            view.add_item(discord.ui.Button(
                label=role.name,
                style=discord.ButtonStyle.primary,
                custom_id=f"role_btn_{role.id}"
            ))

        await interaction.channel.send(
            content="🎭 **Select Your Role**\nClick a button below to get the corresponding role:",
            view=view
        )

        reply = f"✅ Created **{len(roles)}** role button(s) in this channel."
        if failed:
            failed_str = ", ".join(f"`{f}`" for f in failed)
            reply += f"\n⚠️ The following inputs could not be matched to any role and were skipped: {failed_str}"
        await interaction.followup.send(reply, ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(RoleSelector(bot))

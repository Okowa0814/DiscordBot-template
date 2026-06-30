import discord
from discord import app_commands
from discord.ext import commands


class RoleSelector(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # 透過 on_interaction 攔截所有 role_btn_ 開頭的按鈕點擊
    # 好處：Bot 重啟後按鈕依然有效，無需重新執行指令
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
                "❌ 身分組不存在，請聯絡管理員。",
                ephemeral=True
            )
            return

        member = interaction.user
        has_role = role in member.roles

        try:
            if has_role:
                await member.remove_roles(role, reason="使用者透過按鈕移除身分組")
                await interaction.response.send_message(
                    f"✅ 已移除您的 **{role.name}** 身分組。",
                    ephemeral=True
                )
            else:
                await member.add_roles(role, reason="使用者透過按鈕選擇身分組")
                await interaction.response.send_message(
                    f"✅ 已賦予您 **{role.name}** 身分組！",
                    ephemeral=True
                )
        except discord.Forbidden:
            await interaction.response.send_message(
                "❌ Bot 權限不足，請確認 Bot 身分組順序。",
                ephemeral=True
            )
        except discord.HTTPException as e:
            await interaction.response.send_message(
                f"❌ 發生錯誤：{e}",
                ephemeral=True
            )

    @app_commands.command(name="setup_roles", description="在此頻道建立身分組選擇按鈕")
    @app_commands.describe(roles_string="輸入身分組名稱或 ID，以空格分隔")
    @app_commands.default_permissions(administrator=True)
    async def setup_roles(self, interaction: discord.Interaction, roles_string: str):
        await interaction.response.defer(ephemeral=True)

        # 支援逗號或空格分隔
        raw_tokens = roles_string.replace(",", " ").split()
        roles: list[discord.Role] = []
        failed: list[str] = []

        for token in raw_tokens:
            token = token.strip()
            if not token:
                continue

            role: discord.Role | None = None

            # 優先嘗試 ID 查詢
            if token.isdigit():
                role = interaction.guild.get_role(int(token))

            # 若 ID 查不到，改用名稱（不分大小寫）
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
                "❌ 找不到任何有效的身分組，請確認名稱或 ID 是否正確。",
                ephemeral=True
            )
            return

        # Discord 每個 ActionRow 最多 5 個按鈕，最多 5 行，共 25 個
        if len(roles) > 25:
            await interaction.followup.send(
                "❌ 身分組數量不可超過 25 個。",
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
            content="🎭 **選擇您的身分組**\n點擊下方按鈕來獲取對應身分組：",
            view=view
        )

        reply = f"✅ 已在此頻道建立 **{len(roles)}** 個身分組按鈕。"
        if failed:
            failed_str = "、".join(f"`{f}`" for f in failed)
            reply += f"\n⚠️ 以下輸入找不到對應身分組，已略過：{failed_str}"
        await interaction.followup.send(reply, ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(RoleSelector(bot))

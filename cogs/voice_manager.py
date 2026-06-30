import os

import discord
from discord.ext import commands

# 「點我創頻道」語音頻道的 ID，從環境變數讀取
CREATE_CHANNEL_ID: int = int(os.getenv("CREATE_CHANNEL_ID", "0"))


class VoiceManager(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # 記錄所有動態建立的頻道 ID，Bot 重啟後重置
        self.dynamic_channels: set[int] = set()

    @commands.Cog.listener()
    async def on_voice_state_update(
        self,
        member: discord.Member,
        before: discord.VoiceState,
        after: discord.VoiceState,
    ):
        # 使用者進入觸發頻道 → 建立專屬頻道並移動
        if after.channel and after.channel.id == CREATE_CHANNEL_ID:
            await self._create_channel_for(member, after.channel)

        # 使用者離開某個動態頻道 → 若已空則刪除
        if before.channel and before.channel.id in self.dynamic_channels:
            if len(before.channel.members) == 0:
                await self._delete_channel(before.channel)

    async def _create_channel_for(
        self, member: discord.Member, trigger: discord.VoiceChannel
    ):
        try:
            new_channel = await member.guild.create_voice_channel(
                name=f"{member.display_name} 的頻道",
                category=trigger.category,
                reason="動態語音頻道：自動建立",
            )
            self.dynamic_channels.add(new_channel.id)
            await member.move_to(new_channel)
            print(f"[VoiceManager] 已為 {member} 建立頻道：{new_channel.name}")
        except discord.Forbidden:
            print(f"[VoiceManager] 權限不足，無法建立頻道或移動 {member}。")
        except discord.HTTPException as e:
            print(f"[VoiceManager] 建立頻道失敗：{e}")

    async def _delete_channel(self, channel: discord.VoiceChannel):
        try:
            await channel.delete(reason="動態語音頻道：人數歸零，自動刪除")
            print(f"[VoiceManager] 已刪除空頻道：{channel.name}")
        except discord.NotFound:
            pass  # 頻道已不存在，無需處理
        except discord.Forbidden:
            print(f"[VoiceManager] 權限不足，無法刪除頻道：{channel.name}")
        finally:
            self.dynamic_channels.discard(channel.id)


async def setup(bot: commands.Bot):
    await bot.add_cog(VoiceManager(bot))

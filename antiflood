import time
import discord
from discord.ext import commands
from datetime import timedelta

IGNORED_CHANNEL_ID = 1453379496060125216  # ❌ игнорируемый канал

class AntiFlood(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.user_messages = {}

        # ⚙️ НАСТРОЙКИ
        self.MESSAGE_LIMIT = 5      # сообщений
        self.TIME_LIMIT = 5         # секунд
        self.TIMEOUT_SECONDS = 60   # мут для обычных

    def is_admin(self, member: discord.Member) -> bool:
        return (
            member.guild_permissions.administrator
            or member.guild_permissions.moderate_members
        )

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # ❌ игнор ботов, ЛС и нужного канала
        if (
            message.author.bot
            or not message.guild
            or message.channel.id == IGNORED_CHANNEL_ID
        ):
            return

        now = time.time()
        user_id = message.author.id

        if user_id not in self.user_messages:
            self.user_messages[user_id] = []

        self.user_messages[user_id].append(now)

        # оставляем сообщения только за TIME_LIMIT секунд
        self.user_messages[user_id] = [
            t for t in self.user_messages[user_id]
            if now - t <= self.TIME_LIMIT
        ]

        if len(self.user_messages[user_id]) >= self.MESSAGE_LIMIT:
            member = message.author

            # 🛡 админ → предупреждение
            if self.is_admin(member):
                await message.channel.send(
                    f"⚠️ {member.mention}, не флуди, пожалуйста."
                )

            # 👤 обычный → мут
            else:
                try:
                    await member.timeout(
                        discord.utils.utcnow() + timedelta(seconds=self.TIMEOUT_SECONDS),
                        reason="Флуд"
                    )
                    await message.channel.send(
                        f"⛔ {member.mention}, флуд запрещён! "
                        f"Мут на {self.TIMEOUT_SECONDS} сек."
                    )
                except discord.Forbidden:
                    pass

            # сброс счётчика
            self.user_messages[user_id].clear()

async def setup(bot):
    await bot.add_cog(AntiFlood(bot))

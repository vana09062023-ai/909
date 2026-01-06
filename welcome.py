import discord
from discord.ext import commands

WELCOME_CHANNEL_ID = 1458042246560747645
VERIFY_CHANNEL_ID = 1458042841380028446
GUILD_ID = 1450489316663890085


class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if member.guild.id != GUILD_ID:
            return

        channel = self.bot.get_channel(WELCOME_CHANNEL_ID)
        if not channel:
            return

        message = (
            f"## 👋 {member.mention} Добро пожаловать на сервер **909 Team!**\n"
            "Чтобы получить доступ ко всем каналам, тебе нужно пройти **верификацию** ✅\n"
            f"➡️ Перейди в канал <#{VERIFY_CHANNEL_ID}> и следуй инструкции.\n"
            "Приятного общения и добро пожаловать в команду 💙"
        )

        await channel.send(message)


async def setup(bot):
    await bot.add_cog(Welcome(bot))

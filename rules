from discord.ext import commands

class Rules(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="правила")
    async def rules(self, ctx):
        await ctx.send(
            "Привет! "
            "https://discord.com/channels/1450489316663890085/1450489465566003415 "
            "- Тут можно посмотреть все правила на сервере, не нарушай! ✨"
        )

async def setup(bot):
    await bot.add_cog(Rules(bot))

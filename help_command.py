import discord
from discord.ext import commands

class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="909хелп")
    async def send_help(self, ctx):
        embed = discord.Embed(
            title="🤖 909 Bot — Полный обзор",
            description="Привет! Я 909 Bot, создан для управления сервером, выдачи опыта, варнов и многого другого!",
            color=discord.Color.blurple()
        )

        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/906/906175.png")  # Можно заменить на свой значок
        embed.set_footer(text="909 Bot — Следи за чатом и развивайся!", icon_url=ctx.author.avatar.url)

        # Разделы команд
        embed.add_field(
            name="💬 Чат и антифлуд",
            value="`!варны @user` — посмотреть варны\n"
                  "`!варн @user причина` — выдать варн (только модераторы)\n"
                  "`!снятьварн @user` — снять варн (только модераторы)\n"
                  "`!антифлуд` — работает автоматически",
            inline=False
        )
        
        embed.add_field(
            name="🛡 Модерация",
            value="`!кик @user причина` — кик (только администраторы)\n"
                  "`!бан @user причина` — бан (только администраторы)",
            inline=False
        )

        embed.add_field(
            name="ℹ️ Прочее",
            value="`!909хелп` — открыть это сообщение\n"
                  "`!правила` — показать правила сервера",
            inline=False
        )

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(HelpCommand(bot))

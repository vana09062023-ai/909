import discord
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # проверка: админ или нет
    def is_admin(self, member: discord.Member) -> bool:
        return member.guild_permissions.administrator

    def higher_or_equal_role(self, author: discord.Member, target: discord.Member) -> bool:
        return target.top_role >= author.top_role

    # команда кика
    @commands.command(name="кик")
    async def kick(self, ctx, member: discord.Member = None, *, reason: str = None):
        if not self.is_admin(ctx.author):
            await ctx.send("⛔ Только администраторы могут использовать эту команду.")
            return

        if not member or not reason:
            await ctx.send("❗ Использование: `!кик @пользователь причина`")
            return

        if self.higher_or_equal_role(ctx.author, member):
            await ctx.send("⛔ Нельзя кикнуть пользователя с ролью выше или равной вашей.")
            return

        try:
            await member.kick(reason=reason)
            await ctx.send(f"✅ {member.mention} был кикнут! Причина: {reason}")
        except discord.Forbidden:
            await ctx.send("⚠️ Не удалось кикнуть пользователя. Проверь права бота.")

    # команда бана
    @commands.command(name="бан")
    async def ban(self, ctx, member: discord.Member = None, *, reason: str = None):
        if not self.is_admin(ctx.author):
            await ctx.send("⛔ Только администраторы могут использовать эту команду.")
            return

        if not member or not reason:
            await ctx.send("❗ Использование: `!бан @пользователь причина`")
            return

        if self.higher_or_equal_role(ctx.author, member):
            await ctx.send("⛔ Нельзя забанить пользователя с ролью выше или равной вашей.")
            return

        try:
            await member.ban(reason=reason)
            await ctx.send(f"✅ {member.mention} был забанен! Причина: {reason}")
        except discord.Forbidden:
            await ctx.send("⚠️ Не удалось забанить пользователя. Проверь права бота.")

async def setup(bot):
    await bot.add_cog(Moderation(bot))

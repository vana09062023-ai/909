import discord
from discord.ext import commands
import json
import os

# роли, которым разрешено выдавать или снимать варны
ALLOWED_ROLES = [
    1453980812298027142,
    1451189946193936535,
    1451609067868127365,
    1450489769602846841,
    1452001166475923638
]

MAX_WARNS = 3
WARNS_FILE = "warns.json"

class Warns(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        if os.path.exists(WARNS_FILE):
            with open(WARNS_FILE, "r", encoding="utf-8") as f:
                self.warns = json.load(f)
                self.warns = {int(k): v for k, v in self.warns.items()}
        else:
            self.warns = {}

    def save_warns(self):
        with open(WARNS_FILE, "w", encoding="utf-8") as f:
            json.dump(self.warns, f, ensure_ascii=False, indent=4)

    def can_manage_warns(self, member: discord.Member) -> bool:
        return any(role.id in ALLOWED_ROLES for role in member.roles)

    def higher_or_equal_role(self, author: discord.Member, target: discord.Member) -> bool:
        return target.top_role >= author.top_role

    # Просмотр варнов — все
    @commands.command(name="варны")
    async def show_warns(self, ctx, member: discord.Member = None):
        if not member:
            await ctx.send("❗ Укажи пользователя: `!варны @пользователь`")
            return

        count = self.warns.get(member.id, 0)
        await ctx.send(
            f"⚠️ Варны пользователя {member.mention}: **{count}/{MAX_WARNS}**"
        )

    # Выдача варна — роли ALLOWED_ROLES
    @commands.command(name="варн")
    async def give_warn(self, ctx, member: discord.Member = None, *, reason: str = None):
        if not member or not reason:
            await ctx.send("❗ Использование: `!варн @пользователь причина`")
            return

        if not self.can_manage_warns(ctx.author):
            await ctx.send("⛔ У тебя нет прав выдавать варны.")
            return

        if self.higher_or_equal_role(ctx.author, member):
            await ctx.send("⛔ Ты не можешь выдать варн этому пользователю (роль выше или равна твоей).")
            return

        current = self.warns.get(member.id, 0)
        if current >= MAX_WARNS:
            await ctx.send(f"❗ У {member.mention} уже **{MAX_WARNS}/{MAX_WARNS}** варнов! Больше нельзя.")
            return

        self.warns[member.id] = current + 1
        self.save_warns()

        await ctx.send(
            f"⚠️ {member.mention} получил варн от {ctx.author.mention}. "
            f"Причина: {reason}\n"
            f"Варны: {self.warns[member.id]}/{MAX_WARNS}"
        )

    # Снятие варна — роли ALLOWED_ROLES
    @commands.command(name="снятьварн")
    async def remove_warn(self, ctx, member: discord.Member = None):
        if not member:
            await ctx.send("❗ Использование: `!снятьварн @пользователь`")
            return

        if not self.can_manage_warns(ctx.author):
            await ctx.send("⛔ У тебя нет прав снимать варны.")
            return

        current = self.warns.get(member.id, 0)
        if current == 0:
            await ctx.send(f"❗ У {member.mention} нет варнов для снятия.")
            return

        self.warns[member.id] = current - 1
        self.save_warns()

        await ctx.send(
            f"✅ У {member.mention} снят варн {ctx.author.mention}. "
            f"Варны теперь: {self.warns[member.id]}/{MAX_WARNS}"
        )

async def setup(bot):
    await bot.add_cog(Warns(bot))

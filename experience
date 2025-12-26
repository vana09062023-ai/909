import discord
from discord.ext import commands
import json
import os

# роли, которые могут выдавать и снимать опыт
ALLOWED_ROLES = [
    1453980812298027142,
    1451189946193936535,
    1451609067868127365,
    1450489769602846841,
    1452001166475923638
]

EXP_FILE = "experience.json"
LOG_CHANNEL_ID = 1454177854446244012  # канал для логов опыта

class Experience(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # загрузка опыта
        if os.path.exists(EXP_FILE):
            with open(EXP_FILE, "r", encoding="utf-8") as f:
                self.exp = json.load(f)
                self.exp = {int(k): v for k, v in self.exp.items()}
        else:
            self.exp = {}

    def save_exp(self):
        with open(EXP_FILE, "w", encoding="utf-8") as f:
            json.dump(self.exp, f, ensure_ascii=False, indent=4)

    def can_manage_exp(self, member: discord.Member) -> bool:
        return any(role.id in ALLOWED_ROLES for role in member.roles)

    async def send_log(self, message: str):
        channel = self.bot.get_channel(LOG_CHANNEL_ID)
        if channel:
            await channel.send(message)

    # просмотр опыта — все
    @commands.command(name="опыт")
    async def show_exp(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.author
        current = self.exp.get(member.id, 0)
        await ctx.send(f"💠 Опыт пользователя {member.mention}: **{current}**")

    # выдача опыта — ALLOWED_ROLES
    @commands.command(name="опытгив")
    async def give_exp(self, ctx, member: discord.Member = None, amount: int = None, *, reason: str = None):
        if not member or amount is None or not reason:
            await ctx.send("❗ Использование: `!опытгив @пользователь количество причина`")
            return

        if not self.can_manage_exp(ctx.author):
            await ctx.send("⛔ У тебя нет прав выдавать опыт.")
            return

        current = self.exp.get(member.id, 0)
        self.exp[member.id] = current + amount
        self.save_exp()

        await ctx.send(
            f"💠 {member.mention} получил {amount} опыта от {ctx.author.mention}. "
            f"Причина: {reason}\n"
            f"Опыт теперь: {self.exp[member.id]}"
        )

        # лог
        await self.send_log(
            f"💠 **Лог опыта:** {ctx.author.mention} выдал {amount} опыта {member.mention}. Причина: {reason}. "
            f"Всего опыта: {self.exp[member.id]}"
        )

    # снятие опыта — ALLOWED_ROLES
    @commands.command(name="снятьопыт")
    async def remove_exp(self, ctx, member: discord.Member = None, amount: int = None, *, reason: str = None):
        if not member or amount is None or not reason:
            await ctx.send("❗ Использование: `!снятьопыт @пользователь количество причина`")
            return

        if not self.can_manage_exp(ctx.author):
            await ctx.send("⛔ У тебя нет прав снимать опыт.")
            return

        current = self.exp.get(member.id, 0)
        new_amount = max(0, current - amount)
        self.exp[member.id] = new_amount
        self.save_exp()

        await ctx.send(
            f"💠 У {member.mention} снято {amount} опыта {ctx.author.mention}. "
            f"Причина: {reason}\n"
            f"Опыт теперь: {new_amount}"
        )

        # лог
        await self.send_log(
            f"💠 **Лог опыта:** {ctx.author.mention} снял {amount} опыта у {member.mention}. Причина: {reason}. "
            f"Всего опыта: {new_amount}"
        )

    # выдача опыта всем в голосовом канале — ALLOWED_ROLES
    @commands.command(name="войсгив")
    async def give_voice_exp(self, ctx, channel_id: int = None, amount: int = None, *, reason: str = None):
        if not channel_id or amount is None or not reason:
            await ctx.send("❗ Использование: `!войсгив id_голосового_канала количество причина`")
            return

        if not self.can_manage_exp(ctx.author):
            await ctx.send("⛔ У тебя нет прав выдавать опыт.")
            return

        channel = ctx.guild.get_channel(channel_id)
        if not channel or not isinstance(channel, discord.VoiceChannel):
            await ctx.send("❗ Указан неверный голосовой канал.")
            return

        members = [m for m in channel.members if not m.bot]
        if not members:
            await ctx.send("❗ В голосовом канале нет участников.")
            return

        for member in members:
            current = self.exp.get(member.id, 0)
            self.exp[member.id] = current + amount

        self.save_exp()
        mentions = ", ".join([m.mention for m in members])
        await ctx.send(
            f"💠 Всем участникам голосового канала {channel.name} выдано {amount} опыта от {ctx.author.mention}.\n"
            f"Причина: {reason}\n"
            f"Пользователи: {mentions}"
        )

        # лог
        await self.send_log(
            f"💠 **Лог опыта:** {ctx.author.mention} выдал {amount} опыта всем в голосовом канале {channel.name}.\n"
            f"Причина: {reason}\n"
            f"Пользователи: {mentions}"
        )

async def setup(bot):
    await bot.add_cog(Experience(bot))

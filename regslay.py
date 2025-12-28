import discord
from discord.ext import commands

ALLOWED_ROLE_ID = 1453366478534611112
RESULT_CHANNEL_ID = 1450489465566003418


# ===== MODAL =====
class SlayModal(discord.ui.Modal, title="Регистрация на премию SLAY"):
    discord_ping = discord.ui.TextInput(
        label="Ваш пинг Discord",
        placeholder="@username",
        required=True,
        max_length=100
    )

    nomination = discord.ui.TextInput(
        label="На какую премию хотите",
        placeholder="Название номинации",
        required=True,
        max_length=100
    )

    reason = discord.ui.TextInput(
        label="Почему вы должны быть в номинации",
        style=discord.TextStyle.paragraph,
        required=True,
        max_length=1000
    )

    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot

    async def on_submit(self, interaction: discord.Interaction):
        channel = self.bot.get_channel(RESULT_CHANNEL_ID)

        embed = discord.Embed(
            title="🏆 Новая заявка на премию SLAY",
            color=discord.Color.purple()
        )
        embed.add_field(name="👤 Пользователь", value=interaction.user.mention, inline=False)
        embed.add_field(name="📌 Пинг Discord", value=self.discord_ping.value, inline=False)
        embed.add_field(name="⭐ Номинация", value=self.nomination.value, inline=False)
        embed.add_field(name="📝 Причина", value=self.reason.value, inline=False)

        embed.set_footer(text=f"ID пользователя: {interaction.user.id}")

        await channel.send(embed=embed)
        await interaction.response.send_message(
            "✅ Ваша заявка успешно отправлена!", ephemeral=True
        )


# ===== BUTTON =====
class SlayView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(
        label="🏆 Подать заявку",
        style=discord.ButtonStyle.success
    )
    async def apply(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(SlayModal(self.bot))


# ===== COG =====
class RegSlay(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="regslay")
    async def regslay(self, ctx):
        # проверка роли
        if not any(role.id == ALLOWED_ROLE_ID for role in ctx.author.roles):
            await ctx.send("⛔ У тебя нет прав использовать эту команду.")
            return

        embed = discord.Embed(
            title="🏆 Премия SLAY — Регистрация",
            description=(
                "@everyone\n\n"
                "🌟 **Добрый вечер, друзья!**\n\n"
                "Мы рады объявить о начале регистрации на премию **SLAY** в декабре.\n"
                "Чтобы подать заявку, просто нажмите на кнопку ниже 👇"
            ),
            color=discord.Color.purple()
        )

        embed.set_footer(text="Премия SLAY • Декабрь")

        await ctx.send(embed=embed, view=SlayView(self.bot))


async def setup(bot):
    await bot.add_cog(RegSlay(bot))

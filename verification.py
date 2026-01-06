import discord
from discord.ext import commands
import random

VERIFY_CHANNEL_ID = 1458042841380028446
ROLE_NOT_VERIFIED = 1458041901642022974
ROLE_VERIFIED = 1450492049634627748

# Временное хранилище кода капчи
captcha_storage = {}


# ===== VIEW с кнопкой =====
class VerificationView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="✅ Пройти верификацию", style=discord.ButtonStyle.success)
    async def verify(self, interaction: discord.Interaction, _):
        # Генерируем код
        code = str(random.randint(1000, 9999))
        captcha_storage[interaction.user.id] = code

        # ❗ Первое сообщение в ЛС с кодом
        try:
            await interaction.user.send(
                f"🔐 **Ваш код верификации:** `{code}`\n"
                "Перейдите в следующий шаг и введите его, чтобы получить доступ."
            )
        except discord.Forbidden:
            await interaction.response.send_message(
                "❌ Не могу написать вам в ЛС. Разрешите сообщения от сервера.",
                ephemeral=True
            )
            return

        # Второе сообщение с инструкцией (в ЛС)
        await interaction.response.send_message(
            "✉️ Код отправлен вам в ЛС. Введите его в следующем сообщении, чтобы пройти верификацию.",
            ephemeral=True
        )


# ===== COG =====
class Verification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Отправка кнопки в канал
    @commands.command(name="верификация")
    @commands.has_permissions(administrator=True)
    async def verification(self, ctx):
        if ctx.channel.id != VERIFY_CHANNEL_ID:
            return

        embed = discord.Embed(
            title="🔐 Верификация 909 Team",
            description=(
                "Чтобы получить доступ ко всем каналам сервера,\n"
                "нажмите кнопку ниже, и вы получите личный код в ЛС."
            ),
            color=discord.Color.blurple()
        )

        await ctx.send(embed=embed, view=VerificationView())

    # Пользователь вводит код в ЛС
    @commands.command(name="код")
    async def enter_code(self, ctx, user_code: str):
        user_id = ctx.author.id
        correct_code = captcha_storage.get(user_id)

        if not correct_code:
            await ctx.send("❌ У вас нет активного кода верификации. Нажмите кнопку заново.", delete_after=10)
            return

        if user_code != correct_code:
            await ctx.send("❌ Код неверный. Попробуйте снова.", delete_after=10)
            return

        # Всё верно — выдаём роль
        guild = ctx.guild
        member = ctx.author
        role_remove = guild.get_role(ROLE_NOT_VERIFIED)
        role_add = guild.get_role(ROLE_VERIFIED)

        if role_remove in member.roles:
            await member.remove_roles(role_remove, reason="Прошёл верификацию")

        if role_add:
            await member.add_roles(role_add, reason="Прошёл верификацию")

        captcha_storage.pop(user_id, None)
        await ctx.send("✅ Верификация успешно пройдена! Добро пожаловать 💙", delete_after=15)


async def setup(bot):
    await bot.add_cog(Verification(bot))

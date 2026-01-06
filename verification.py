import discord
from discord.ext import commands
import random

VERIFY_CHANNEL_ID = 1458042841380028446
ROLE_NOT_VERIFIED = 1458041901642022974
ROLE_VERIFIED = 1450492049634627748

# временное хранилище капчи
captcha_storage = {}


# ===== MODAL =====
class CaptchaModal(discord.ui.Modal, title="🔐 Верификация"):
    captcha_input = discord.ui.TextInput(
        label="Введите код с кнопки",
        placeholder="Например: 4821",
        required=True,
        max_length=6
    )

    def __init__(self, user_id: int):
        super().__init__()
        self.user_id = user_id

    async def on_submit(self, interaction: discord.Interaction):
        correct_code = captcha_storage.get(self.user_id)

        if not correct_code:
            await interaction.response.send_message(
                "❌ Капча устарела. Нажмите кнопку ещё раз.",
                ephemeral=True
            )
            return

        if self.captcha_input.value != correct_code:
            await interaction.response.send_message(
                "❌ Неверный код. Попробуйте ещё раз.",
                ephemeral=True
            )
            return

        guild = interaction.guild
        member = interaction.user

        role_remove = guild.get_role(ROLE_NOT_VERIFIED)
        role_add = guild.get_role(ROLE_VERIFIED)

        if role_remove in member.roles:
            await member.remove_roles(role_remove, reason="Прошёл верификацию")

        if role_add:
            await member.add_roles(role_add, reason="Прошёл верификацию")

        captcha_storage.pop(self.user_id, None)

        await interaction.response.send_message(
            "✅ Верификация успешно пройдена! Добро пожаловать 💙",
            ephemeral=True
        )


# ===== VIEW =====
class VerificationView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="✅ Пройти верификацию", style=discord.ButtonStyle.success)
    async def verify(self, interaction: discord.Interaction, _):
        code = str(random.randint(1000, 9999))
        captcha_storage[interaction.user.id] = code

        await interaction.response.send_message(
            f"🔐 **Код верификации:** `{code}`\n"
            "Нажмите кнопку ещё раз и введите его в появившемся окне.",
            ephemeral=True
        )

        await interaction.followup.send_modal(
            CaptchaModal(interaction.user.id)
        )


# ===== COG =====
class Verification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="верификация")
    @commands.has_permissions(administrator=True)
    async def verification(self, ctx):
        if ctx.channel.id != VERIFY_CHANNEL_ID:
            return

        embed = discord.Embed(
            title="🔐 Верификация на сервере 909 Team",
            description=(
                "Чтобы получить доступ ко всем каналам сервера,\n"
                "нажмите кнопку ниже и пройдите простую верификацию.\n\n"
                "🛡 Это защищает сервер от ботов и рейдов."
            ),
            color=discord.Color.blurple()
        )

        await ctx.send(embed=embed, view=VerificationView())


async def setup(bot):
    await bot.add_cog(Verification(bot))

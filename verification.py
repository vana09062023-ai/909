import discord
from discord.ext import commands
import random

VERIFY_CHANNEL_ID = 1458042841380028446
ROLE_NOT_VERIFIED = 1458041901642022974
ROLE_VERIFIED = 1450492049634627748

QUESTION = "Сколько букв в слове «дискорд»?"
CORRECT = "7"
OPTIONS = ["6", "7", "8"]


class VerificationView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        random.shuffle(OPTIONS)

        for option in OPTIONS:
            self.add_item(VerifyButton(option, option == CORRECT))


class VerifyButton(discord.ui.Button):
    def __init__(self, label: str, correct: bool):
        style = discord.ButtonStyle.success if correct else discord.ButtonStyle.secondary
        super().__init__(label=label, style=style)
        self.correct = correct

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        member = interaction.user

        if self.correct:
            remove_role = guild.get_role(ROLE_NOT_VERIFIED)
            add_role = guild.get_role(ROLE_VERIFIED)

            if remove_role in member.roles:
                await member.remove_roles(remove_role)

            if add_role:
                await member.add_roles(add_role)

            await interaction.response.send_message(
                "✅ Вы успешно прошли верификацию! Добро пожаловать 💙",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "❌ Неверный ответ. Попробуйте ещё раз.",
                ephemeral=True
            )


class Verification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="верификация")
    @commands.has_permissions(administrator=True)
    async def verification(self, ctx):
        if ctx.channel.id != VERIFY_CHANNEL_ID:
            return

        embed = discord.Embed(
            title="🔐 Верификация 909 Team",
            description="Докажите, что вы человек, выбрав правильный ответ 👇",
            color=discord.Color.blurple()
        )
        embed.add_field(name="❓ Вопрос", value=QUESTION, inline=False)

        await ctx.send(embed=embed, view=VerificationView())


async def setup(bot):
    await bot.add_cog(Verification(bot))

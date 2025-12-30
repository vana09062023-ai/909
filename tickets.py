import discord
from discord.ext import commands
import random

TICKET_CHANNEL_ID = 1455434894288228496
TICKET_CATEGORY_ID = 1455434772812796076


# ===== MODAL =====
class TicketModal(discord.ui.Modal, title="Открытие тикета"):
    reason = discord.ui.TextInput(
        label="По какой причине открываете тикет?",
        style=discord.TextStyle.paragraph,
        required=True,
        max_length=1000
    )

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    async def on_submit(self, interaction: discord.Interaction):
        guild = interaction.guild
        category = guild.get_channel(TICKET_CATEGORY_ID)

        ticket_number = random.randint(1000, 9999)
        channel_name = f"тикет-{ticket_number}"

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True
            ),
            guild.me: discord.PermissionOverwrite(view_channel=True)
        }

        # доступ всем администраторам
        for member in guild.members:
            if member.guild_permissions.administrator:
                overwrites[member] = discord.PermissionOverwrite(
                    view_channel=True,
                    send_messages=True,
                    read_message_history=True
                )

        channel = await guild.create_text_channel(
            name=channel_name,
            category=category,
            overwrites=overwrites
        )

        embed = discord.Embed(
            title="🎫 Новый тикет",
            color=discord.Color.blurple()
        )
        embed.add_field(name="👤 Автор", value=interaction.user.mention, inline=False)
        embed.add_field(name="📝 Причина", value=self.reason.value, inline=False)

        await channel.send(embed=embed, view=CloseTicketView())
        await interaction.response.send_message(
            f"✅ Тикет создан: {channel.mention}",
            ephemeral=True
        )


# ===== VIEW С КНОПКАМИ =====
class TicketView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(
        label="🎫 Открыть тикет",
        style=discord.ButtonStyle.primary
    )
    async def open_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(TicketModal(self.bot))


class CloseTicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="🔒 Закрыть тикет",
        style=discord.ButtonStyle.danger
    )
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "⛔ Только администратор может закрыть тикет.",
                ephemeral=True
            )
            return

        await interaction.channel.delete(reason="Тикет закрыт администратором")


# ===== COG =====
class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="tiket")
    async def ticket(self, ctx):
        if ctx.channel.id != TICKET_CHANNEL_ID:
            return

        if not ctx.author.guild_permissions.administrator:
            await ctx.send("⛔ Команда доступна только администраторам.")
            return

        embed = discord.Embed(
            title="🎫 Система тикетов",
            description=(
                "Добро пожаловать!\n\n"
                "Нажмите кнопку ниже, чтобы открыть тикет и связаться с администрацией.\n"
                "Опишите проблему максимально подробно."
            ),
            color=discord.Color.blurple()
        )

        embed.set_footer(text="909 • Ticket System")

        await ctx.send(embed=embed, view=TicketView(self.bot))


async def setup(bot):
    await bot.add_cog(Tickets(bot))

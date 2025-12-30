import discord
from discord.ext import commands
import random
import io
from datetime import datetime

TICKET_CHANNEL_ID = 1455434894288228496
TICKET_CATEGORY_ID = 1455434772812796076
LOG_CHANNEL_ID = 1455554988557205575

open_tickets = {}  # user_id: channel_id


# ========= MODALS =========
class TicketModal(discord.ui.Modal, title="Открытие тикета"):
    reason = discord.ui.TextInput(
        label="По какой причине открываете тикет?",
        style=discord.TextStyle.paragraph,
        max_length=1000,
        required=True
    )

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    async def on_submit(self, interaction: discord.Interaction):
        if interaction.user.id in open_tickets:
            await interaction.response.send_message(
                "⛔ У вас уже есть открытый тикет.",
                ephemeral=True
            )
            return

        guild = interaction.guild
        category = guild.get_channel(TICKET_CATEGORY_ID)
        log_channel = self.bot.get_channel(LOG_CHANNEL_ID)

        ticket_id = random.randint(1000, 9999)
        channel_name = f"тикет-{ticket_id}"

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True
            ),
            guild.me: discord.PermissionOverwrite(view_channel=True)
        }

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

        open_tickets[interaction.user.id] = channel.id

        embed = discord.Embed(
            title="🎫 Новый тикет",
            color=discord.Color.blurple(),
            timestamp=datetime.utcnow()
        )
        embed.add_field(name="👤 Автор", value=interaction.user.mention, inline=False)
        embed.add_field(name="📝 Причина", value=self.reason.value, inline=False)

        await channel.send(embed=embed, view=CloseTicketView(self.bot))

        if log_channel:
            log = discord.Embed(
                title="📥 Тикет открыт",
                color=discord.Color.green(),
                timestamp=datetime.utcnow()
            )
            log.add_field(name="Пользователь", value=interaction.user.mention, inline=False)
            log.add_field(name="Канал", value=channel.mention, inline=False)
            log.add_field(name="Причина", value=self.reason.value, inline=False)
            await log_channel.send(embed=log)

        await interaction.response.send_message(
            f"✅ Тикет создан: {channel.mention}",
            ephemeral=True
        )


class CloseReasonModal(discord.ui.Modal, title="Закрытие тикета"):
    reason = discord.ui.TextInput(
        label="Причина закрытия тикета",
        style=discord.TextStyle.paragraph,
        max_length=1000,
        required=True
    )

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    async def on_submit(self, interaction: discord.Interaction):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "⛔ Только администратор может закрыть тикет.",
                ephemeral=True
            )
            return

        log_channel = self.bot.get_channel(LOG_CHANNEL_ID)

        messages = []
        async for msg in interaction.channel.history(limit=None, oldest_first=True):
            messages.append(
                f"[{msg.created_at.strftime('%d.%m.%Y %H:%M')}] "
                f"{msg.author}: {msg.content}"
            )

        transcript = "\n".join(messages)
        file = discord.File(
            fp=io.BytesIO(transcript.encode("utf-8")),
            filename=f"{interaction.channel.name}.txt"
        )

        embed = discord.Embed(
            title="📕 Тикет закрыт",
            color=discord.Color.red(),
            timestamp=datetime.utcnow()
        )
        embed.add_field(name="Закрыл", value=interaction.user.mention, inline=False)
        embed.add_field(name="Причина", value=self.reason.value, inline=False)
        embed.add_field(name="Канал", value=interaction.channel.name, inline=False)

        if log_channel:
            await log_channel.send(embed=embed, file=file)

        for user_id, channel_id in list(open_tickets.items()):
            if channel_id == interaction.channel.id:
                del open_tickets[user_id]

        await interaction.channel.delete(reason="Тикет закрыт")


# ========= VIEWS =========
class TicketView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label="🎫 Открыть тикет", style=discord.ButtonStyle.primary)
    async def open_ticket(self, interaction: discord.Interaction, _):
        await interaction.response.send_modal(TicketModal(self.bot))


class CloseTicketView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label="🔒 Закрыть тикет", style=discord.ButtonStyle.danger)
    async def close_ticket(self, interaction: discord.Interaction, _):
        await interaction.response.send_modal(CloseReasonModal(self.bot))


# ========= COG =========
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
                "Нажмите кнопку ниже, чтобы открыть тикет.\n"
                "Опишите проблему максимально подробно."
            ),
            color=discord.Color.blurple()
        )

        await ctx.send(embed=embed, view=TicketView(self.bot))


async def setup(bot):
    await bot.add_cog(Tickets(bot))

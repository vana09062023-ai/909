import discord
from discord.ext import commands

GUILD_ID = 1450489316663890085

# ====== КОНФИГ РЕАКЦИОННЫХ РОЛЕЙ ======
REACTION_MESSAGES = {
    # ===== СТАРОЕ СООБЩЕНИЕ =====
    1454513503309271236: {  # message_id
        "channel_id": 1450507155659555009,
        "roles": {
            "📵": 1453378595509768310,
            "👦": 1454097720469094472,
            "👱‍♀️": 1450509186520846518
        }
    },

    # ===== НОВОЕ СООБЩЕНИЕ (ФЛАГИ) =====
    1454826252601917451: {
        "channel_id": 1450507155659555009,
        "roles": {
            "flag_russia": 1454826403592929391,   # кастом
            "Greece": 1455112322010972301,           # стандарт
            "Belarus": 1454826699052154953,       # кастом
            "ukraine": 1454826771131404350        # кастом
        }
    }
}


class ReactionRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ===== ДОБАВЛЕНИЕ РЕАКЦИЙ ПРИ СТАРТЕ =====
    @commands.Cog.listener()
    async def on_ready(self):
        guild = self.bot.get_guild(GUILD_ID)

        for message_id, data in REACTION_MESSAGES.items():
            channel = guild.get_channel(data["channel_id"])
            if not channel:
                continue

            try:
                message = await channel.fetch_message(message_id)
            except:
                continue

            for emoji_key in data["roles"].keys():
                try:
                    emoji = discord.utils.get(guild.emojis, name=emoji_key)
                    await message.add_reaction(emoji or emoji_key)
                except:
                    pass

        print("✅ Reaction roles (all messages) загружены")

    # ===== ДОБАВЛЕНИЕ РОЛИ =====
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if payload.guild_id != GUILD_ID:
            return

        config = REACTION_MESSAGES.get(payload.message_id)
        if not config:
            return

        emoji_name = payload.emoji.name if payload.emoji.is_custom_emoji() else str(payload.emoji)
        role_id = config["roles"].get(emoji_name)
        if not role_id:
            return

        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        if not member or member.bot:
            return

        role = guild.get_role(role_id)
        if role:
            await member.add_roles(role, reason="Reaction role add")

    # ===== УДАЛЕНИЕ РОЛИ =====
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        if payload.guild_id != GUILD_ID:
            return

        config = REACTION_MESSAGES.get(payload.message_id)
        if not config:
            return

        emoji_name = payload.emoji.name if payload.emoji.is_custom_emoji() else str(payload.emoji)
        role_id = config["roles"].get(emoji_name)
        if not role_id:
            return

        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        if not member:
            return

        role = guild.get_role(role_id)
        if role:
            await member.remove_roles(role, reason="Reaction role remove")


async def setup(bot):
    await bot.add_cog(ReactionRoles(bot))

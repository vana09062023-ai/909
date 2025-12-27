import discord
from discord.ext import commands

# ID сообщения с реакциями
MESSAGE_ID = 1454513503309271236
CHANNEL_ID = 1450507155659555009
GUILD_ID = 1450489316663890085

# эмодзи -> роль
REACTION_ROLES = {
    "📵": 1453378595509768310,      # mobile_phone_off
    "👦": 1454097720469094472,      # boy
    "👱‍♀️": 1450509186520846518     # blond_haired_woman
}

class ReactionRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        guild = self.bot.get_guild(GUILD_ID)
        channel = guild.get_channel(CHANNEL_ID)
        message = await channel.fetch_message(MESSAGE_ID)

        # ставим реакции при запуске
        for emoji in REACTION_ROLES.keys():
            try:
                await message.add_reaction(emoji)
            except:
                pass

        print("✅ Reaction roles загружены")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if payload.message_id != MESSAGE_ID:
            return

        emoji = str(payload.emoji)
        if emoji not in REACTION_ROLES:
            return

        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)

        if member.bot:
            return

        role = guild.get_role(REACTION_ROLES[emoji])
        if role:
            await member.add_roles(role, reason="Reaction role add")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        if payload.message_id != MESSAGE_ID:
            return

        emoji = str(payload.emoji)
        if emoji not in REACTION_ROLES:
            return

        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)

        if not member:
            return

        role = guild.get_role(REACTION_ROLES[emoji])
        if role:
            await member.remove_roles(role, reason="Reaction role remove")

async def setup(bot):
    await bot.add_cog(ReactionRoles(bot))

import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

@bot.event
async def on_ready():
    await bot.change_presence(
        status=discord.Status.dnd,
        activity=discord.Streaming(
            name="Следит за чатом в скваде!",
            url="https://twitch.tv/example"
        )
    )
    print(f"Бот запущен как {bot.user}")

async def main():
    async with bot:
        await bot.load_extension("rules")
        await bot.load_extension("antiflood")
        await bot.load_extension("warns")
        await bot.load_extension("moderation")
        await bot.load_extension("experience")
        await bot.load_extension("help_command")
        await bot.start("")

asyncio.run(main())

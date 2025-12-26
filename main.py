import discord
from discord.ext import commands
import asyncio

# Токен бота
BOT_TOKEN = 

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

async def main():
    async with bot:
        # загружаем все cogs
        await bot.load_extension("rules")
        await bot.load_extension("antiflood")
        await bot.load_extension("warns")
        await bot.load_extension("moderation")
        await bot.load_extension("experience")
        await bot.load_extension("help_command")
        
        await bot.start(BOT_TOKEN)

asyncio.run(main())

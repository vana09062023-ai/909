import discord
from discord.ext import commands
import asyncio
import os # Добавляем этот модуль

# Бот будет брать токен из "Переменных окружения" на хостинге
BOT_TOKEN = os.getenv('BOT_TOKEN') 

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

async def main():
    async with bot:
        # Загружаем коги
        # Убедись, что названия файлов совпадают (например, rules.py)
        extensions = ["rules", "antiflood", "warns", "moderation", "experience", "help_command"]
        
        for extension in extensions:
            try:
                await bot.load_extension(extension)
                print(f"Модуль {extension} успешно загружен.")
            except Exception as e:
                print(f"Ошибка загрузки {extension}: {e}")
        
        if BOT_TOKEN:
            await bot.start(BOT_TOKEN)
        else:
            print("ОШИБКА: Токен не найден! Проверь переменные окружения на BotHost.")

if __name__ == "__main__":
    asyncio.run(main())

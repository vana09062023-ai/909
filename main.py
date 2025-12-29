import discord
from discord.ext import commands
import asyncio
import os

# Было: BOT_TOKEN = os.getenv('BOT_TOKEN')
# Стало:
BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# Новая задача для обновления статуса
async def set_status_loop():
    await bot.wait_until_ready()
    activity1 = discord.Activity(type=discord.ActivityType.listening, name="Общается в скваде 909")
    # Могут быть и другие варианты статуса
    status_options = [
        discord.Activity(type=discord.ActivityType.listening, name="Общается в скваде 909"),
        discord.Activity(type=discord.ActivityType.watching, name="сквада 909"),
        discord.Activity(type=discord.ActivityType playing, name="в чате"),
    ]
    idx = 0
    while not bot.is_closed():
        try:
            await bot.change_presence(activity=status_options[idx % len(status_options)])
            idx += 1
        except Exception as e:
            print(f"Ошибка смены статуса: {e}")
        await asyncio.sleep(600)  # 10 минут
        

async def main():
    async with bot:
        # Загружаем коги
        # Убедись, что названия файлов совпадают (например, rules.py)
        extensions = ["rules", "antiflood", "warns", "moderation", "regslay", "reaction_roles", "help_command"]
        
        for extension in extensions:
            try:
                await bot.load_extension(extension)
                print(f"Модуль {extension} успешно загружен.")
            except Exception as e:
                print(f"Ошибка загрузки {extension}: {e}")
        
        # Запускаем задачу статуса
        bot.loop.create_task(set_status_loop())
        
        if BOT_TOKEN:
            await bot.start(BOT_TOKEN)
        else:
            print("ОШИБКА: Токен не найден! Проверь переменные окружения на BotHost.")

if __name__ == "__main__":
    asyncio.run(main())

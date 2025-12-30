import discord
from discord.ext import commands
import asyncio
import os

# Токен берётся из переменных окружения хостинга
BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    activity = discord.Streaming(
        name="Общается в скваде 909",
        url="https://twitch.tv/discord"  # ссылка обязательна
    )

    await bot.change_presence(
        status=discord.Status.dnd,  # Не беспокоить
        activity=activity
    )

    print(f"✅ Бот запущен как {bot.user}")


async def main():
    async with bot:
        extensions = [
            "rules",
            "antiflood",
            "warns",
            "moderation",
            "regslay",
            "reaction_roles",
            "help_command"
        ]

        for extension in extensions:
            try:
                await bot.load_extension(extension)
                print(f"Модуль {extension} успешно загружен.")
            except Exception as e:
                print(f"Ошибка загрузки {extension}: {e}")

        if BOT_TOKEN:
            await bot.start(BOT_TOKEN)
        else:
            print("❌ ОШИБКА: Токен не найден! Проверь DISCORD_BOT_TOKEN на хостинге.")


if __name__ == "__main__":
    asyncio.run(main())

import asyncio
import os

from telegram import Bot
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")


def send_telegram_notification(message):
    bot = Bot(token=BOT_TOKEN)

    chat_id = "-1002006402830"
    asyncio.run(bot.send_message(chat_id=chat_id, text=message))

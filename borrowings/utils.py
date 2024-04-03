import asyncio

from telegram import Bot


def send_telegram_notification(message):
    bot_token = "7025192077:AAGy6mPZ0YCcVSCy9z9OfL_KGZCJdx6cscI"
    bot = Bot(token=bot_token)

    chat_id = "-1002006402830"
    asyncio.run(bot.send_message(chat_id=chat_id, text=message))

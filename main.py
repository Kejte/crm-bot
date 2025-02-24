import asyncio
import os
import logging
from core import handlers
from core.settings import settings
from aiogram import Bot, Dispatcher, F 
from aiogram.filters import Command
from utils.commands import set_commands
from aiogram.client.default import DefaultBotProperties
from core.middlewares import RegisterMiddleware

async def start_bot(bot: Bot):
    await set_commands(bot)
    await bot.send_message(settings.bots.admin_id, text='Бот запущен!')

async def stop_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text='Бот выключен!')

async def load_bot():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - [%(levelname)s] - %(name)s -'''
                               '(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s'
                        )
    bot = Bot(token=settings.bots.bot_token, default=DefaultBotProperties(parse_mode='HTML'))
    dp = Dispatcher()

    # STAFF handlers
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    dp.message.middleware.register(RegisterMiddleware())
    dp.callback_query.middleware.register(RegisterMiddleware())

    dp.message.register(handlers.hello_message, Command(commands='start'))
    dp.callback_query.register(handlers.hello_message, F.data=='hello_message')
    dp.callback_query.register(handlers.send_callback_message, F.data.startswith('id_'))
    dp.callback_query.register(handlers.offers_categories, F.data=='offers_categories')
    dp.callback_query.register(handlers.offers,F.data.startswith('offers_category'))
    dp.callback_query.register(handlers.offer, F.data.startswith('offer_'))
    dp.callback_query.register(handlers.apply_offer, F.data.startswith('apply_'))    

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(load_bot())
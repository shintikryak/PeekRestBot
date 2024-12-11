from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
import asyncio
import logging

import config
from handlers import router

async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Начать работу с ботом"),
        BotCommand(command="restaurants", description="Показать список ресторанов"),
        BotCommand(command="tables", description="Показать свободные столики"),
    ]
    await bot.set_my_commands(commands)

async def main():
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)

    # Устанавливаем команды меню
    await set_bot_commands(bot)
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

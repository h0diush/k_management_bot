import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from config_data import ConfigBot, config_bot
from handlers import base_command_router, task_commands_router
from keyboards import set_main_menu
from middlewares import CheckUserMiddleware

logger = logging.getLogger(__name__)


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s "
               "[%(asctime)s] - %(name)s - %(message)s",
    )
    logger.info("starting Bot...")
    config: ConfigBot = config_bot()
    bot = Bot(token=config.tg_bot.token,
              default=DefaultBotProperties(parse_mode="HTML"))
    await set_main_menu(bot)
    dp = Dispatcher()
    dp.include_router(base_command_router)
    dp.include_router(task_commands_router)
    base_command_router.message.middleware(CheckUserMiddleware())
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

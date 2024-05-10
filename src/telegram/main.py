from aiogram import Dispatcher, Bot

from src.telegram import main_router
from src.middlewares.telegram import DBSessionMiddleware
from src.database.create_pool import create_pool
from src.settings import settings


async def webhook_startup(bot: Bot):
    print("set", await bot.set_webhook(settings.webhooks.build_url(), secret_token=settings.webhooks.secret))


async def webhook_shutdown(bot: Bot):
    print("down", await bot.delete_webhook())


dp = Dispatcher()

dp.include_router(main_router)

pool = dp["session_pool"] = create_pool(
    dsn=settings.postgres.build_dsn())

dp.update.outer_middleware(DBSessionMiddleware(session_pool=pool))

from aiogram import Bot

from src.database import create_pool
from src.settings import settings
from src.utils.logger import setup_logger

pool = create_pool(settings.postgres.build_dsn())

bot = Bot(settings.bot_token)

logger = setup_logger()

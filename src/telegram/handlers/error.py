import traceback

from aiogram import Router
from aiogram.types import ErrorEvent

from src.factories import logger

router = Router()


@router.error()
async def error_handler(event: ErrorEvent):
    logger.error(traceback.format_exc())

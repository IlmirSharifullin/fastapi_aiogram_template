from aiogram import Router

from .start import router as start_router
from .error import router as error_router

main_router = Router()
main_router.include_routers(error_router, start_router)
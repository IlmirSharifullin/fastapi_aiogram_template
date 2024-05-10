from fastapi import APIRouter

from src.settings import settings

main_router = APIRouter(prefix=settings.uri_prefix)


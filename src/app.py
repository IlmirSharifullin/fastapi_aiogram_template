import asyncio
import logging
from datetime import timedelta
from typing import Annotated

import uvicorn
from aiogram import types
from fastapi import FastAPI, Request, Header, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.base import BaseHTTPMiddleware

from src.admin_app import main_router
from src.admin_app.config import Token, authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, \
    get_current_admin_user
from src.database import DBUser
from src.factories import bot, pool
from src.middlewares import FastApiDBSessionMiddleware
from src.settings import settings
from src.telegram.main import dp, webhook_startup, webhook_shutdown

app = FastAPI()
db_middleware = FastApiDBSessionMiddleware(session_pool=pool)
app.add_middleware(BaseHTTPMiddleware, dispatch=db_middleware)
app.mount(settings.uri_prefix + "/static", StaticFiles(directory="admin_app/static"), name="static")

app.include_router(main_router)


templates = Jinja2Templates(directory="admin_app/templates")


@app.post("/token")
async def login_for_access_token(r: Request,
                                 form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 ) -> Token:
    user = await authenticate_user(r.state.db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@app.get("/users/me/")
async def read_users_me(
        current_user: Annotated[DBUser, Depends(get_current_admin_user)],
):
    return current_user


@app.post(settings.webhooks.path)
async def bot_webhook(update: dict,
                      x_telegram_bot_api_secret_token: Annotated[str | None, Header()] = None) -> None | dict:
    """ Register webhook endpoint for telegram"""
    if x_telegram_bot_api_secret_token != settings.webhooks.secret:
        return {"status": "error", "message": "Wrong secret token!"}
    telegram_update = types.Update(**update)
    await dp.feed_webhook_update(bot=bot, update=telegram_update)


async def main():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(name)s- %(message)s')

    await webhook_startup(bot)

    config = uvicorn.Config("src.app:app", port=settings.webhooks.port, host=settings.webhooks.host, log_level="info", )
    server = uvicorn.Server(config)
    await server.serve()

    await webhook_shutdown(bot)


if __name__ == '__main__':
    asyncio.run(main())

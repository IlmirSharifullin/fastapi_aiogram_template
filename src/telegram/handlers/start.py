from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from src.database import Repository

router = Router()


@router.message(CommandStart())
async def start_cmd(message: Message, repository: Repository):
    user = await repository.user.get(message.from_user.id)
    print(user)
    raise ValueError
    await message.answer(message.text)

from aiogram import types, Router
from aiogram.filters import CommandStart

start_router = Router()


@start_router.message(CommandStart)
async def cmd_start(message: types.Message):
    await message.answer("Bot successfully run from docker!")

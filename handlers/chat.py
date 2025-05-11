from aiogram import Router
from aiogram.types import Message

from services.yandex_client import ask_yandex_gpt

router = Router()


@router.message()
async def chat(message: Message):
    reply = await ask_yandex_gpt(message.text)
    await message.answer(reply)

from aiogram import Router
from aiogram.types import Message

from services.load_resume import load_stack


router = Router()


@router.message(lambda msg: msg.text == "/start")
async def start_command(message: Message):
    await message.answer("Привет! Я бот-Кирилл."
                         " Ты можешь задать мне любой вопрос по резюме"
                         " — я отвечу как кандидат.")
    stack = load_stack()
    await message.answer(
        f"Вот кратко мой стек:\n\n{stack}", parse_mode="Markdown")
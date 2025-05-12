from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import (Message, InlineKeyboardMarkup,
                           InlineKeyboardButton, CallbackQuery,
                           ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove)
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup

from services.load_resume import load_stack, load_about_me
from services.yandex_client import ask_yandex_gpt
from constants import COMMANDS_WITH_DESCRIPTION

router = Router()


class ChatMode(StatesGroup):
    talking_to_ai = State()


@router.message(Command("start"))
async def start_command(message: Message):
    name = message.from_user.first_name
    ai_button = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="💬 Поговорить с ИИ о резюме",
            callback_data="talk_to_ai")]
    ])
    await message.answer(
        f"*Привет, {name}👋*\nЯ бот Кирилла🤖\n"
        "Ты можешь задать мне любой вопрос по резюме нажав"
        " на 'Поговорить с ИИ о резюме'"
        " — я отвечу как кандидат\n\n"
        f"*Вот что я умею:*\n{COMMANDS_WITH_DESCRIPTION}",
        reply_markup=ai_button,
        parse_mode="MarkdownV2"
    )


@router.message(Command("about_kirill"))
async def start_command(message: Message):
    await message.answer(load_about_me(), parse_mode="MarkdownV2")


@router.message(Command("short_stack"))
async def short_stack_command(message: Message):
    await message.answer(load_stack(), parse_mode="MarkdownV2")


@router.message(Command("help"))
async def help_command(message: Message):
    user_message = f"Все команды:\n\n{COMMANDS_WITH_DESCRIPTION}"
    await message.answer(user_message, parse_mode="MarkdownV2")


@router.callback_query(F.data == "talk_to_ai")
async def talk_to_ai_handler(callback: CallbackQuery, state: FSMContext):
    stop_button = KeyboardButton(text="❌ Остановить разговор с ИИ")
    stop_keyboard = ReplyKeyboardMarkup(
        keyboard=[[stop_button]], resize_keyboard=True
    )
    await callback.message.answer(
        "Напиши свой вопрос, и я постараюсь ответить как кандидат 👨‍💼\n",
        reply_markup=stop_keyboard
    )
    await state.set_state(ChatMode.talking_to_ai)
    await callback.answer()


@router.message(F.text == "❌ Остановить разговор с ИИ")
async def stop_ai_chat(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "AI-режим отключён. Ты можешь снова начать, нажав кнопку на /start.",
        reply_markup=ReplyKeyboardRemove(remove_keyboard=True)
    )


@router.message(ChatMode.talking_to_ai)
async def handle_ai_question(message: Message):
    reply = await ask_yandex_gpt(message.text)
    await message.answer(f"`{reply}`", parse_mode="MarkdownV2")


@router.message()
async def fallback_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == ChatMode.talking_to_ai:
        return

    await message.answer(
        "🤖 Я не понял твоё сообщение."
        " Чтобы начать разговор с ИИ, нажми на кнопку в /start."
    )

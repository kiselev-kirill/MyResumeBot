import asyncio
from aiogram import Bot, Dispatcher
from config import TELEGRAM_BOT_TOKEN
from handlers.start import router as start_router
from handlers.chat import router as chat_router


async def main():
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(start_router)
    dp.include_router(chat_router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
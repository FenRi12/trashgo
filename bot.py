# bot.py
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from config import TOKEN
from handlers import start_handlers, user_handlers, admin_handlers, info_handlers
from database import init_db
init_db()

# ----------------- НАСТРОЙКА ЛОГИРОВАНИЯ -----------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# ----------------- ИНИЦИАЛИЗАЦИЯ -----------------

bot = Bot(token=TOKEN)
dp = Dispatcher()

# ----------------- ПОДКЛЮЧЕНИЕ РОУТЕРОВ -----------------
dp.include_router(start_handlers.router)
dp.include_router(user_handlers.router)
dp.include_router(admin_handlers.router)
dp.include_router(info_handlers.router)

# ----------------- ХЭНДЛЕР ОШИБОК -----------------
async def error_handler(update: types.Update, exception: Exception, *args, **kwargs):
    logging.error(f"❌ Ошибка при обработке апдейта: {exception}")
    return True  # чтобы бот не падал

dp.errors.register(error_handler)


# ----------------- ЗАПУСК -----------------
if __name__ == "__main__":
    logging.info("🚀 Бот запущен!")
    try:
        asyncio.run(dp.start_polling(bot))
    except Exception as e:
        logging.critical(f"❌ Фатальная ошибка: {e}")

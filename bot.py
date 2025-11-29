import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from config import TOKEN
from handlers import start_handlers, user_handlers, admin_handlers, info_handlers
from database import init_db
from database_users import init_users_db
from handlers import start_handlers, user_handlers, admin_handlers, info_handlers, language_handlers

# ----------------- ИНИЦИАЛИЗАЦИЯ БАЗ -----------------
init_db()
init_users_db()

# ----------------- НАСТРОЙКА ЛОГИРОВАНИЯ -----------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# ----------------- СОЗДАНИЕ БОТА И ДИСПЕТЧЕРА -----------------
bot = Bot(token=TOKEN)
dp = Dispatcher()

# ----------------- ПОДКЛЮЧЕНИЕ РОУТЕРОВ -----------------
dp.include_router(start_handlers.router)
dp.include_router(user_handlers.router)
dp.include_router(admin_handlers.router)
dp.include_router(info_handlers.router)  # сюда уже входит menu_router
dp.include_router(language_handlers.router)

# ----------------- ХЭНДЛЕР ОШИБОК -----------------


async def error_handler(update: types.Update, exception: Exception, *args, **kwargs):
    logging.error(f"❌ Ошибка при обработке апдейта: {exception}", exc_info=True)
    # можно добавить уведомление админу, если нужно


dp.errors.register(error_handler)

# ----------------- ЗАПУСК -----------------
if __name__ == "__main__":
    logging.info("🚀 Бот запущен!")
    try:
        asyncio.run(dp.start_polling(bot))
    except Exception as e:
        logging.critical(f"❌ Фатальная ошибка: {e}")

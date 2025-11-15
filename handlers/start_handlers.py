from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from keyboards import main_menu

router = Router()

@router.message(Command("start"))
async def start_command(message: Message):
    await message.answer(
        "Привет! Я бот TrashGo. Выберите действие:", 
        reply_markup=main_menu
    )

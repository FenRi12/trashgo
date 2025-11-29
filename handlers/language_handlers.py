# language_handlers.py

from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from database_users import save_user_data
from localization import L_text
from keyboards import main_menu

router = Router()


# FSM выбора языка
class LangChoose(StatesGroup):
    choosing = State()


# -----------------------------
# Нажатие кнопки "🌐 Выбрать язык"
# -----------------------------
@router.message(lambda msg: msg.text.startswith("🌐"))
async def ask_language(message: types.Message, state: FSMContext):
    await state.set_state(LangChoose.choosing)

    kb = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="🇷🇺 Русский")],
            [types.KeyboardButton(text="🇺🇿 O‘zbekcha")]
        ],
        resize_keyboard=True
    )

    await message.answer("🌐 Выберите язык / Tilni tanlang", reply_markup=kb)


# -----------------------------
# Обработка выбора языка
# -----------------------------
@router.message(LangChoose.choosing)
async def save_language(message: types.Message, state: FSMContext):

    if message.text == "🇷🇺 Русский":
        lang = "ru"
    elif message.text == "🇺🇿 O‘zbekcha":
        lang = "uz"
    else:
        await message.answer("Пожалуйста, выберите язык кнопкой.")
        return

    save_user_data(message.from_user.id, language=lang)

    await state.clear()

    await message.answer(
        L_text("Язык успешно изменён!", message.from_user.id),
        reply_markup=main_menu(message.from_user.id)
    )

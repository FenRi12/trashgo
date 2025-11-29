# start_handlers.py
import logging
from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command

from localization import L_text
from keyboards import main_menu
from database_users import save_user_data, get_user

router = Router()

class LangState(StatesGroup):
    choosing = State()

class RegistrationState(StatesGroup):
    house = State()
    entrance = State()
    apartment = State()
    floor = State()
    door_code = State()
    location = State()
    first_name = State()
    last_name = State()
    phone = State()

@router.message(Command("start"))
async def start_command(message: types.Message, state: FSMContext):
    user = get_user(message.from_user.id)

    # Если язык уже выбран → показываем просто меню
    if user and user.get("language"):
        uid = message.from_user.id
        await message.answer(
            L_text("👋Привет! Я бот TrashGo.", uid),
            reply_markup=main_menu(uid)
        )
        return

    # Иначе — выбор языка
    await state.set_state(LangState.choosing)

    kb = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="🇷🇺 Русский")],
            [types.KeyboardButton(text="🇺🇿 O‘zbekcha")]
        ],
        resize_keyboard=True
    )

    await message.answer("🌐 Выберите язык / Tilni tanlang", reply_markup=kb)

@router.message(LangState.choosing)
async def choose_language(message: types.Message, state: FSMContext):
    if message.text == "🇷🇺 Русский":
        lang = "ru"
    elif message.text == "🇺🇿 O‘zbekcha":
        lang = "uz"
    else:
        await message.answer("Выберите язык кнопкой.")
        return

    save_user_data(message.from_user.id, language=lang)

    await state.clear()

    # После выбора языка — просто меню (без регистрации)
    await message.answer(
        L_text("👋Привет! Я бот TrashGo.", message.from_user.id),
        reply_markup=main_menu(message.from_user.id)
    )

# ------------------------------- РЕГИСТРАЦИЯ -------------------------------

@router.message(RegistrationState.house)
async def reg_house(message: types.Message, state: FSMContext):
    await state.update_data(house=message.text.strip())
    await state.set_state(RegistrationState.entrance)
    await message.answer(L_text("Введите номер подъезда слева направо:", message.from_user.id))

@router.message(RegistrationState.entrance)
async def reg_entrance(message: types.Message, state: FSMContext):
    await state.update_data(entrance=message.text.strip())
    await state.set_state(RegistrationState.apartment)
    await message.answer(L_text("Введите номер квартиры:", message.from_user.id))

@router.message(RegistrationState.apartment)
async def reg_apartment(message: types.Message, state: FSMContext):
    await state.update_data(apartment=message.text.strip())
    await state.set_state(RegistrationState.floor)
    await message.answer(L_text("Введите этаж:", message.from_user.id))

@router.message(RegistrationState.floor)
async def reg_floor(message: types.Message, state: FSMContext):
    await state.update_data(floor=message.text.strip())
    await state.set_state(RegistrationState.door_code)
    await message.answer(L_text("Введите код домофона:", message.from_user.id))

@router.message(RegistrationState.door_code)
async def reg_door_code(message: types.Message, state: FSMContext):
    await state.update_data(door_code=message.text.strip())
    await state.set_state(RegistrationState.location)
    await message.answer(L_text("Отправьте вашу локацию 📍 через 📎", message.from_user.id))

@router.message(RegistrationState.location)
async def reg_location(message: types.Message, state: FSMContext):
    if not message.location:
        await message.answer(L_text("Пожалуйста, отправьте локацию 📍", message.from_user.id))
        return

    await state.update_data(latitude=float(message.location.latitude), longitude=float(message.location.longitude))
    await state.set_state(RegistrationState.first_name)
    await message.answer(L_text("Введите имя:", message.from_user.id))

@router.message(RegistrationState.first_name)
async def reg_first_name(message: types.Message, state: FSMContext):
    await state.update_data(first_name=message.text.strip())
    await state.set_state(RegistrationState.last_name)
    await message.answer(L_text("Введите фамилию:", message.from_user.id))

@router.message(RegistrationState.last_name)
async def reg_last_name(message: types.Message, state: FSMContext):
    await state.update_data(last_name=message.text.strip())
    await state.set_state(RegistrationState.phone)
    await message.answer(L_text("Введите телефон:", message.from_user.id))

@router.message(RegistrationState.phone)
async def reg_phone(message: types.Message, state: FSMContext):
    data = await state.get_data()

    save_user_data(
        user_id=message.from_user.id,
        first_name=data.get("first_name"),
        last_name=data.get("last_name"),
        username=message.from_user.username or "—",
        phone=data.get("phone"),
        house=data.get("house"),
        entrance=data.get("entrance"),
        apartment=data.get("apartment"),
        floor=data.get("floor"),
        door_code=data.get("door_code"),
        latitude=data.get("latitude"),
        longitude=data.get("longitude")
    )

    await message.answer(
        L_text("✅ Регистрация завершена! Ваши данные сохранены.", message.from_user.id),
        reply_markup=main_menu(message.from_user.id)
    )
    await state.clear()

# Ошибки
@router.errors()
async def global_error_handler(update, **kwargs):
    exception = kwargs.get("exception")
    logging.error(f"Произошла ошибка: {exception} \nUpdate: {update}")
    return True

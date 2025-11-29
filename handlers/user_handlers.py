# user_handlers.py
import logging
from datetime import datetime
from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from localization import L_text
from keyboards import (
    main_menu,
    time_slots_kb,
    bags_kb,
    tariff_kb,
    admin_order_buttons
)

from database_users import save_user_data, get_user
from database import add_order
from config import ADMIN_CHAT_ID

router = Router()

class OrderState(StatesGroup):
    choosing_data = State()
    house = State()
    entrance = State()
    apartment = State()
    floor = State()
    door_code = State()
    location = State()
    first_name = State()
    last_name = State()
    phone = State()
    time_slot = State()
    bags = State()
    payment = State()

@router.message(lambda m: m.text == L_text("🚮 Заказать вынос мусора", m.from_user.id))
async def start_order(message: types.Message, state: FSMContext):
    user = get_user(message.from_user.id)

    # Определяем, есть ли РЕАЛЬНАЯ регистрация
    has_real_data = (
        user and (
            user.get("house") or
            user.get("first_name") or
            user.get("phone")
        )
    )

    if has_real_data:
        kb = types.ReplyKeyboardMarkup(
            keyboard=[
                [
                    types.KeyboardButton(text=L_text("✅ Использовать мои данные", message.from_user.id)),
                    types.KeyboardButton(text=L_text("✏️ Ввести новые данные", message.from_user.id))
                ]
            ],
            resize_keyboard=True
        )
        await message.answer(
            L_text("У вас уже есть сохранённые данные. Что использовать для заказа?", message.from_user.id),
            reply_markup=kb
        )
        await state.set_state(OrderState.choosing_data)
    else:
        await state.set_state(OrderState.house)
        await message.answer(L_text("Введите номер дома:", message.from_user.id))

@router.message(OrderState.choosing_data)
async def choosing_user_data(message: types.Message, state: FSMContext):
    user = get_user(message.from_user.id)

    if message.text == L_text("✅ Использовать мои данные", message.from_user.id):
        if not user:
            await message.answer(
                L_text("❌ Нет сохранённых данных, введите новые.", message.from_user.id),
                reply_markup=main_menu(message.from_user.id)
            )
            await state.clear()
            return

        await state.update_data(**user)
        await state.set_state(OrderState.time_slot)
        await message.answer(
            L_text("Выберите время:", message.from_user.id),
            reply_markup=time_slots_kb(message.from_user.id)
        )

    elif message.text == L_text("✏️ Ввести новые данные", message.from_user.id):
        await state.set_state(OrderState.house)
        await message.answer(L_text("Введите номер дома:", message.from_user.id))

    else:
        await message.answer(L_text("Пожалуйста, выберите опцию кнопкой.", message.from_user.id))

# ================= Шаги регистрации при заказе =================

@router.message(OrderState.house)
async def order_house(message: types.Message, state: FSMContext):
    await state.update_data(house=message.text.strip())
    await state.set_state(OrderState.entrance)
    await message.answer(L_text("Введите номер подъезда слева направо:", message.from_user.id))

@router.message(OrderState.entrance)
async def order_entrance(message: types.Message, state: FSMContext):
    await state.update_data(entrance=message.text.strip())
    await state.set_state(OrderState.apartment)
    await message.answer(L_text("Введите номер квартиры:", message.from_user.id))

@router.message(OrderState.apartment)
async def order_apartment(message: types.Message, state: FSMContext):
    await state.update_data(apartment=message.text.strip())
    await state.set_state(OrderState.floor)
    await message.answer(L_text("Введите этаж:", message.from_user.id))

@router.message(OrderState.floor)
async def order_floor(message: types.Message, state: FSMContext):
    await state.update_data(floor=message.text.strip())
    await state.set_state(OrderState.door_code)
    await message.answer(L_text("Введите код домофона:", message.from_user.id))

@router.message(OrderState.door_code)
async def order_door_code(message: types.Message, state: FSMContext):
    await state.update_data(door_code=message.text.strip())
    await state.set_state(OrderState.location)
    await message.answer(L_text("Отправьте вашу локацию 📍 через 📎", message.from_user.id))

@router.message(OrderState.location)
async def order_location(message: types.Message, state: FSMContext):
    if not message.location:
        await message.answer(L_text("Пожалуйста, отправьте локацию 📍", message.from_user.id))
        return

    await state.update_data(
        latitude=float(message.location.latitude),
        longitude=float(message.location.longitude)
    )
    await state.set_state(OrderState.first_name)
    await message.answer(L_text("Введите имя:", message.from_user.id))

@router.message(OrderState.first_name)
async def order_first_name(message: types.Message, state: FSMContext):
    await state.update_data(first_name=message.text.strip())
    await state.set_state(OrderState.last_name)
    await message.answer(L_text("Введите фамилию:", message.from_user.id))

@router.message(OrderState.last_name)
async def order_last_name(message: types.Message, state: FSMContext):
    await state.update_data(last_name=message.text.strip())
    await state.set_state(OrderState.phone)
    await message.answer(L_text("Введите телефон:", message.from_user.id))

@router.message(OrderState.phone)
async def order_phone(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text.strip())
    await state.set_state(OrderState.time_slot)
    await message.answer(
        L_text("Выберите время:", message.from_user.id),
        reply_markup=time_slots_kb(message.from_user.id)
    )

@router.message(OrderState.time_slot)
async def order_time(message: types.Message, state: FSMContext):
    await state.update_data(time_slot=message.text.strip())
    await state.set_state(OrderState.bags)
    await message.answer(
        L_text("Выберите количество пакетов:", message.from_user.id),
        reply_markup=bags_kb(message.from_user.id)
    )

@router.message(OrderState.bags)
async def order_bags(message: types.Message, state: FSMContext):
    if message.text not in ["1", "2", "3", "4"]:
        await message.answer(
            L_text("Выберите количество пакетов кнопкой от 1 до 4", message.from_user.id),
            reply_markup=bags_kb(message.from_user.id)
        )
        return

    await state.update_data(bags=int(message.text))
    await state.set_state(OrderState.payment)
    await message.answer(
        L_text("Выберите тариф:", message.from_user.id),
        reply_markup=tariff_kb(message.from_user.id)
    )

@router.message(OrderState.payment)
async def order_payment(message: types.Message, state: FSMContext):
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

    order_data = {
        "user_id": message.from_user.id,
        "first_name": data.get("first_name"),
        "last_name": data.get("last_name"),
        "username": message.from_user.username or "—",
        "phone": data.get("phone"),
        "house": data.get("house"),
        "entrance": data.get("entrance"),
        "apartment": data.get("apartment"),
        "floor": data.get("floor"),
        "door_code": data.get("door_code"),
        "latitude": data.get("latitude"),
        "longitude": data.get("longitude"),
        "time_slot": data.get("time_slot"),
        "bags": data.get("bags"),
        "payment": message.text,
        "courier_id": 0,
        "status": "Новый",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    try:
        order_id = add_order(**order_data)

        await message.answer(
            f"{L_text('✅ Ваш заказ №', message.from_user.id)}{order_id} "
            f"{L_text('успешно создан!', message.from_user.id)}",
            reply_markup=main_menu(message.from_user.id)
        )

        uid = message.from_user.id

        admin_text = (
            f"🆕 <b>{L_text('Заказ №', uid)}{order_id}</b>\n\n"
            f"👤 <b>{L_text('Имя:', uid)}</b> {order_data['first_name']}\n"
            f"👤 <b>{L_text('Фамилия:', uid)}</b> {order_data['last_name']}\n"
            f"💬 <b>Username:</b> @{order_data['username']}\n"
            f"📞 <b>{L_text('Телефон:', uid)}</b> {order_data['phone']}\n\n"
            f"🏢 <b>{L_text('Дом:', uid)}</b> {order_data['house']}\n"
            f"🚪 <b>{L_text('Подъезд:', uid)}</b> {order_data['entrance']}\n"
            f"🏡 <b>{L_text('Квартира:', uid)}</b> {order_data['apartment']}\n"
            f"⬆️ <b>{L_text('Этаж:', uid)}</b> {order_data['floor']}\n"
            f"🔑 <b>{L_text('Код домофона:', uid)}</b> {order_data['door_code']}\n"
            f"📍 <a href='https://maps.google.com/?q={order_data['latitude']},{order_data['longitude']}'>{L_text('📍 Локация', uid)}</a>\n\n"
            f"⏰ <b>{L_text('Время:', uid)}</b> {order_data['time_slot']}\n"
            f"🗑 <b>{L_text('Пакетов:', uid)}</b> {order_data['bags']}\n"
            f"💰 <b>{L_text('Оплата:', uid)}</b> {order_data['payment']}\n"
            f"🕒 <b>{L_text('Создан:', uid)}</b> {order_data['created_at']}"
        )

        await message.bot.send_message(
            ADMIN_CHAT_ID,
            admin_text,
            parse_mode="HTML",
            reply_markup=admin_order_buttons(order_id, message.from_user.id)
        )

    except Exception as e:
        logging.error(f"Ошибка при создании заказа: {e}")
        await message.answer(L_text("⚠️ Ошибка при сохранении заказа. Попробуйте снова.", message.from_user.id))

    finally:
        await state.clear()

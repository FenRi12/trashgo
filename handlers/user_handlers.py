import logging
from datetime import datetime
from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards import time_slots_kb, bags_kb, tariff_kb, main_menu, admin_order_buttons
from database import add_order, get_orders_by_user
from config import ADMIN_CHAT_ID

router = Router()

# ===========================
# FSM состояния заказа
# ===========================
class OrderState(StatesGroup):
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

# ===========================
# Начало оформления заказа
# ===========================
@router.message(F.text == "🚮 Заказать вынос мусора")
async def start_order(message: types.Message, state: FSMContext):
    await state.set_state(OrderState.house)
    await message.answer("Введите номер дома:")
    logging.info(f"Пользователь {message.from_user.id} начал заказ")

# ===========================
# Пошаговая логика
# ===========================
@router.message(OrderState.house)
async def process_house(message: types.Message, state: FSMContext):
    await state.update_data(house=str(message.text).strip())
    await state.set_state(OrderState.entrance)
    await message.answer("Введите номер подъезда слева направо:")

@router.message(OrderState.entrance)
async def process_entrance(message: types.Message, state: FSMContext):
    await state.update_data(entrance=str(message.text).strip())
    await state.set_state(OrderState.apartment)
    await message.answer("Введите номер квартиры:")

@router.message(OrderState.apartment)
async def process_apartment(message: types.Message, state: FSMContext):
    await state.update_data(apartment=str(message.text).strip())
    await state.set_state(OrderState.floor)
    await message.answer("Введите этаж:")

@router.message(OrderState.floor)
async def process_floor(message: types.Message, state: FSMContext):
    await state.update_data(floor=str(message.text).strip())
    await state.set_state(OrderState.door_code)
    await message.answer("Введите код домофона:")

@router.message(OrderState.door_code)
async def process_door_code(message: types.Message, state: FSMContext):
    await state.update_data(door_code=str(message.text).strip())
    await state.set_state(OrderState.location)
    await message.answer("Отправьте вашу локацию 📍 через 📎")

@router.message(OrderState.location)
async def process_location(message: types.Message, state: FSMContext):
    if not message.location:
        await message.answer("Пожалуйста, отправьте локацию 📍")
        return
    await state.update_data(
        latitude=float(message.location.latitude),
        longitude=float(message.location.longitude)
    )
    await state.set_state(OrderState.first_name)
    await message.answer("Введите имя:")

@router.message(OrderState.first_name)
async def process_first_name(message: types.Message, state: FSMContext):
    await state.update_data(first_name=str(message.text).strip())
    await state.set_state(OrderState.last_name)
    await message.answer("Введите фамилию:")

@router.message(OrderState.last_name)
async def process_last_name(message: types.Message, state: FSMContext):
    await state.update_data(last_name=str(message.text).strip())
    await state.set_state(OrderState.phone)
    await message.answer("Введите телефон:")

@router.message(OrderState.phone)
async def process_phone(message: types.Message, state: FSMContext):
    await state.update_data(phone=str(message.text).strip())
    await state.set_state(OrderState.time_slot)
    await message.answer("Выберите время:", reply_markup=time_slots_kb)

@router.message(OrderState.time_slot)
async def process_time_slot(message: types.Message, state: FSMContext):
    await state.update_data(time_slot=str(message.text).strip())
    await state.set_state(OrderState.bags)
    await message.answer("Выберите количество пакетов:", reply_markup=bags_kb)

@router.message(OrderState.bags)
async def process_bags(message: types.Message, state: FSMContext):
    if message.text not in ["1", "2", "3", "4"]:
        await message.answer("Выберите количество пакетов кнопкой от 1 до 4", reply_markup=bags_kb)
        return
    await state.update_data(bags=int(message.text))
    await state.set_state(OrderState.payment)
    await message.answer("Выберите тариф:", reply_markup=tariff_kb)

# ===========================
# Завершение заказа
# ===========================
@router.message(OrderState.payment)
async def process_payment(message: types.Message, state: FSMContext):
    data = await state.get_data()

    # 🔹 Вывод состояния для отладки
    logging.info(f"STATE DATA перед сохранением: {data}")

    # Подготовка данных для базы
    order_data = {
        "user_id": int(message.from_user.id),
        "first_name": data.get("first_name", "—"),
        "last_name": data.get("last_name", "—"),
        "username": message.from_user.username or "Не указан",
        "phone": data.get("phone", "—"),
        "house": data.get("house", "—"),
        "entrance": data.get("entrance", "—"),
        "apartment": data.get("apartment", "—"),
        "floor": data.get("floor", "—"),
        "door_code": data.get("door_code", "—"),
        "latitude": float(data.get("latitude", 0.0)),
        "longitude": float(data.get("longitude", 0.0)),
        "time_slot": data.get("time_slot", "—"),
        "bags": int(data.get("bags", 0)),
        "payment": str(message.text).strip() or "—",
        "courier_id": 0,
        "status": "Новый",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    try:
        order_id = add_order(**order_data)
        await message.answer(f"✅ Ваш заказ #{order_id} успешно создан!", reply_markup=main_menu)

        # Отправка админу
        admin_text = (
            f"🆕 <b>Новый заказ №{order_id}</b>\n\n"
            f"👤 <b>Имя:</b> {order_data['first_name']}\n"
            f"👤 <b>Фамилия:</b> {order_data['last_name']}\n"
            f"💬 <b>Username:</b> @{order_data['username']}\n"
            f"📞 <b>Телефон:</b> {order_data['phone']}\n\n"
            f"🏢 <b>Дом:</b> {order_data['house']}\n"
            f"🚪 <b>Подъезд:</b> {order_data['entrance']}\n"
            f"🏡 <b>Квартира:</b> {order_data['apartment']}\n"
            f"⬆️ <b>Этаж:</b> {order_data['floor']}\n"
            f"🔑 <b>Код домофона:</b> {order_data['door_code']}\n"
            f"📍 <a href='https://maps.google.com/?q={order_data['latitude']},{order_data['longitude']}'>Локация</a>\n\n"
            f"⏰ <b>Время:</b> {order_data['time_slot']}\n"
            f"🗑 <b>Пакетов:</b> {order_data['bags']}\n"
            f"💰 <b>Оплата:</b> {order_data['payment']}\n"
            f"🕒 <b>Создан:</b> {order_data['created_at']}"
        )

        await message.bot.send_message(
            ADMIN_CHAT_ID,
            admin_text,
            parse_mode="HTML",
            reply_markup=admin_order_buttons(order_id)
        )
        logging.info(f"✅ Заказ #{order_id} создан пользователем {message.from_user.id}")

    except Exception as e:
        logging.error(f"Ошибка при создании заказа: {e}")
        await message.answer("⚠️ Ошибка при сохранении заказа. Попробуйте снова.")
    finally:
        await state.clear()

# ===========================
# Мои заказы (пользователю)
# ===========================
@router.message(lambda msg: msg.text == "📦 Мои заказы")
async def show_my_orders(message: types.Message):
    try:
        # Получаем только последние 2 заказа пользователя
        orders = get_orders_by_user(message.from_user.id)[:2]

        logging.info(f"[DEBUG] Всего заказов для {message.from_user.id}: {len(orders)}")
        for i, o in enumerate(orders, 1):
            logging.info(f"[DEBUG] Заказ {i}: {o}")

    except Exception as e:
        logging.error(f"[ERROR] Ошибка получения заказов: {e}")
        await message.answer("⚠️ Не удалось получить заказы.", reply_markup=main_menu)
        return

    if not orders:
        await message.answer("📭 У вас пока нет заказов.", reply_markup=main_menu)
        return

    for o in orders:
        # Локация с ссылкой
        location = (
            f"<a href='https://maps.google.com/?q={o.get('latitude',0)},{o.get('longitude',0)}'>Локация</a>"
            if o.get('latitude') and o.get('longitude') else "—"
        )

        text = (
            f"🆔 Заказ №{o['order_id']}\n"
            f"👤 Имя: {o.get('first_name','—')}\n"
            f"👤 Фамилия: {o.get('last_name','—')}\n"
            f"💬 Username: @{o.get('username','—')}\n"
            f"📞 Телефон: {o.get('phone','—')}\n\n"
            f"🏢 Дом: {o.get('house','—')}\n"
            f"🚪 Подъезд: {o.get('entrance','—')}\n"
            f"🏡 Квартира: {o.get('apartment','—')}\n"
            f"⬆️ Этаж: {o.get('floor','—')}\n"
            f"🔑 Код домофона: {o.get('door_code','—')}\n"
            f"📍 {location}\n\n"
            f"⏰ Время: {o.get('time_slot','—')}\n"
            f"🗑 Пакетов: {o.get('bags',0)}\n"
            f"💰 Оплата: {o.get('payment','—')}\n"
            f"🕒 Создан: {o.get('created_at','—')}"
        )

        await message.answer(text, parse_mode="HTML", reply_markup=main_menu)
        logging.info(f"[DEBUG] Отправлено пользователю: {o['order_id']}")

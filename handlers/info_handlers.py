# info_handlers.py

from aiogram import Router, types
from database import get_orders_by_user, safe_str, safe_int, safe_float
from keyboards import main_menu
from localization import L_text
import logging

router = Router()


# ===========================
#   📦 Мои заказы
# ===========================
@router.message(lambda msg: msg.text == L_text("📦 Мои заказы", msg.from_user.id))
async def show_my_orders(message: types.Message):
    logging.info(f"[DEBUG] Пользователь {message.from_user.id} нажал 'Мои заказы'")

    try:
        orders = get_orders_by_user(message.from_user.id)[:2]
    except Exception as e:
        logging.error(f"[ERROR] Ошибка получения заказов: {e}")
        await message.answer(
            L_text("⚠️ Не удалось получить заказы.", message.from_user.id),
            reply_markup=main_menu(message.from_user.id)
        )
        return

    if not orders:
        await message.answer(
            L_text("📭 У вас пока нет заказов.", message.from_user.id),
            reply_markup=main_menu(message.from_user.id)
        )
        return

    for o in orders:
        try:
            lat = safe_float(o.get("latitude"))
            lon = safe_float(o.get("longitude"))

            location = (
                f"<a href='https://maps.google.com/?q={lat},{lon}'>"
                f"{L_text('📍 Локация', message.from_user.id)}</a>"
                if lat and lon else "—"
            )

            username = safe_str(o.get("username"))
            username_str = f"@{username}" if username and username != "Не указан" else "—"

            text = (
                f"🆔 {L_text('Заказ №', message.from_user.id)}{safe_int(o.get('order_id'))}\n"
                f"👤 {L_text('Имя:', message.from_user.id)} {safe_str(o.get('first_name'))}\n"
                f"👤 {L_text('Фамилия:', message.from_user.id)} {safe_str(o.get('last_name'))}\n"
                f"💬 Username: {username_str}\n"
                f"📞 {L_text('Телефон:', message.from_user.id)} {safe_str(o.get('phone'))}\n\n"
                f"🏢 {L_text('Дом:', message.from_user.id)} {safe_str(o.get('house'))}\n"
                f"🚪 {L_text('Подъезд:', message.from_user.id)} {safe_str(o.get('entrance'))}\n"
                f"🏡 {L_text('Квартира:', message.from_user.id)} {safe_str(o.get('apartment'))}\n"
                f"⬆️ {L_text('Этаж:', message.from_user.id)} {safe_str(o.get('floor'))}\n"
                f"🔑 {L_text('Код домофона:', message.from_user.id)} {safe_str(o.get('door_code'))}\n"
                f"📍 {location}\n\n"
                f"⏰ {L_text('Время:', message.from_user.id)} {safe_str(o.get('time_slot'))}\n"
                f"🗑 {L_text('Пакетов:', message.from_user.id)} {safe_int(o.get('bags'))}\n"
                f"💰 {L_text('Оплата:', message.from_user.id)} {safe_str(o.get('payment'))}\n"
                f"🕒 {L_text('Создан:', message.from_user.id)} {safe_str(o.get('created_at'))}"
            )

            await message.answer(
                text,
                parse_mode="HTML",
                reply_markup=main_menu(message.from_user.id)
            )

        except Exception as e:
            logging.error(f"[ERROR] Ошибка при формировании текста заказа: {e}")
            await message.answer(
                L_text("⚠️ Не удалось показать заказ.", message.from_user.id),
                reply_markup=main_menu(message.from_user.id)
            )


# ===========================
#   💰 Тарифы
# ===========================
@router.message(lambda msg: msg.text == L_text("💰 Тарифы", msg.from_user.id))
async def show_tariffs(message: types.Message):
    text = (
        f"💰 <b>{L_text('Тарифы', message.from_user.id)}</b>\n\n"
        f"• {L_text('Разовый — 13 000 сум', message.from_user.id)}\n"
        f"• {L_text('Месячный — 300 000 сум', message.from_user.id)}\n"
    )

    await message.answer(text, parse_mode="HTML", reply_markup=main_menu(message.from_user.id))


# ===========================
#   ℹ️ Как это работает
# ===========================
@router.message(lambda msg: msg.text == L_text("ℹ️ Как это работает", msg.from_user.id))
async def how_it_works(message: types.Message):
    text = L_text(
        "Сервис «Выноса бытового мусора» - удобно, чисто и без хлопот!Не хотите выходить из дома, чтобы вынести мусор? Мы все сделаем за вас!Курьер заберет мусор от вашей двери и отнесет до ближайших мусорных контейнеров -аккуратно и в любое удобное для вас время.- Работаем с 7:00 до 23:00- Услуга для квартир, офисов, салонов красоты и др..\n",
        message.from_user.id
    )

    await message.answer(text, reply_markup=main_menu(message.from_user.id))


# ===========================
#   📞 Связаться с оператором
# ===========================
@router.message(lambda msg: msg.text == L_text("📞 Связаться с оператором", msg.from_user.id))
async def contact_operator(message: types.Message):
    text = L_text(
        "📞 Оператор:@TozaGo",
        message.from_user.id
    )
    await message.answer(text, reply_markup=main_menu(message.from_user.id))

# admin_handlers.py
from aiogram import Router, F
from aiogram.types import CallbackQuery
from database import update_order_status, get_order
from localization import L_text
from keyboards import admin_order_buttons

router = Router()

@router.callback_query(F.data.startswith(("assign_", "done_", "cancel_")))
async def admin_actions(callback: CallbackQuery):
    try:
        action, order_id_str = callback.data.split("_")
        order_id = int(order_id_str)
    except Exception:
        await callback.answer("Ошибка: некорректные данные", show_alert=True)
        return

    order = get_order(order_id)
    if not order:
        await callback.answer("Ошибка: заказ не найден", show_alert=True)
        return

    user_id = order["user_id"] if isinstance(order, dict) else order.user_id

    if action == "assign":
        update_order_status(order_id, L_text("В работе", user_id))
        await callback.message.bot.send_message(
            user_id,
            f"{L_text('🚚 Ваш заказ #', user_id)}{order_id} {L_text('принят курьером и выполняется!', user_id)}"
        )
        # admin feedback (show to admin) — also in client's language (вариант 2)
        await callback.answer(L_text("Заказ назначен", user_id))

    elif action == "done":
        update_order_status(order_id, L_text("Выполнен", user_id))
        await callback.message.bot.send_message(
            user_id,
            f"{L_text('✅ Ваш заказ #', user_id)}{order_id} {L_text('успешно выполнен!', user_id)}"
        )
        await callback.answer(L_text("Заказ выполнен", user_id))

    elif action == "cancel":
        update_order_status(order_id, L_text("Отменён", user_id))
        await callback.message.bot.send_message(
            user_id,
            f"{L_text('❌ Ваш заказ #', user_id)}{order_id} {L_text('был отменён администратором.', user_id)}"
        )
        await callback.answer(L_text("Заказ отменён", user_id))

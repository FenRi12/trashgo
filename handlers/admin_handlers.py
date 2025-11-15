from aiogram import Router, F
from aiogram.types import CallbackQuery
from database import update_order_status, get_order

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

    # Проверяем тип
    if isinstance(order, dict):
        user_id = order.get("user_id")
    else:
        user_id = order.user_id

    if action == "assign":
        update_order_status(order_id, "В работе")
        await callback.message.bot.send_message(
            user_id,
            f"🚚 Ваш заказ #{order_id} принят курьером и выполняется!"
        )
        await callback.answer("Заказ назначен")

    elif action == "done":
        update_order_status(order_id, "Выполнен")
        await callback.message.bot.send_message(
            user_id,
            f"✅ Ваш заказ #{order_id} успешно выполнен!"
        )
        await callback.answer("Заказ выполнен")

    elif action == "cancel":
        update_order_status(order_id, "Отменён")
        await callback.message.bot.send_message(
            user_id,
            f"❌ Ваш заказ #{order_id} был отменён администратором."
        )
        await callback.answer("Заказ отменён")

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🚮 Заказать вынос мусора")],
        [KeyboardButton(text="📦 Мои заказы")],
        [KeyboardButton(text="💰 Тарифы"), KeyboardButton(text="ℹ️ Как это работает")],
        [KeyboardButton(text="📞 Связаться с оператором")]
    ],
    resize_keyboard=True
)

time_slots_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Утро")],
        [KeyboardButton(text="День")],
        [KeyboardButton(text="Вечер")],
        [KeyboardButton(text="Отмена")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

bags_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=str(i))] for i in range(1, 5)
    ] + [[KeyboardButton(text="Отмена")]],
    resize_keyboard=True,
    one_time_keyboard=True
)

tariff_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Разовый — 13 000 сум")],
        [KeyboardButton(text="Месячный — 300 000 сум")],
        [KeyboardButton(text="Отмена")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

location_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Отправить локацию", request_location=True)],
        [KeyboardButton(text="Отмена")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

confirm_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Подтвердить и отправить админу")],
        [KeyboardButton(text="Отмена")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

def admin_order_buttons(order_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Назначить курьера", callback_data=f"assign_{order_id}"),
                InlineKeyboardButton(text="Отменить", callback_data=f"cancel_{order_id}")
            ],
            [
                InlineKeyboardButton(text="Заказ выполнен", callback_data=f"done_{order_id}")
            ]
        ]
    )

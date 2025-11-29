# keyboards.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from localization import L_text

# Главная клавиатура
def main_menu(user_id: int) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=L_text("🚮 Заказать вынос мусора", user_id))],
            [KeyboardButton(text=L_text("📦 Мои заказы", user_id))],
            [
                KeyboardButton(text=L_text("💰 Тарифы", user_id)),
                KeyboardButton(text=L_text("ℹ️ Как это работает", user_id))
            ],
            [KeyboardButton(text=L_text("📞 Связаться с оператором", user_id))],
            [KeyboardButton(text=L_text("🌐 Выбрать язык", user_id))]
        ],
        resize_keyboard=True
    )

def time_slots_kb(user_id: int) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=L_text("7:00 - 11:00", user_id))],
            [KeyboardButton(text=L_text("11:00 - 17:00", user_id))],
            [KeyboardButton(text=L_text("17:00 - 22:00", user_id))],
            [KeyboardButton(text=L_text("Отмена", user_id))]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

def bags_kb(user_id: int) -> ReplyKeyboardMarkup:
    rows = [[KeyboardButton(text=str(i))] for i in range(1, 5)]
    rows.append([KeyboardButton(text=L_text("Отмена", user_id))])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True, one_time_keyboard=True)

def tariff_kb(user_id: int) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=L_text("Разовый — 13 000 сум", user_id))],
            [KeyboardButton(text=L_text("Месячный — 300 000 сум", user_id))],
            [KeyboardButton(text=L_text("Отмена", user_id))]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

def location_kb(user_id: int) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=L_text("Отправить локацию", user_id), request_location=True)],
            [KeyboardButton(text=L_text("Отмена", user_id))]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

def confirm_kb(user_id: int) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=L_text("Подтвердить и отправить админу", user_id))],
            [KeyboardButton(text=L_text("Отмена", user_id))]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

def admin_order_buttons(order_id: int, user_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=L_text("Назначить курьера", user_id),
                    callback_data=f"assign_{order_id}"
                ),
                InlineKeyboardButton(
                    text=L_text("Отменить", user_id),
                    callback_data=f"cancel_{order_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text=L_text("Заказ выполнен", user_id),
                    callback_data=f"done_{order_id}"
                )
            ]
        ]
    )

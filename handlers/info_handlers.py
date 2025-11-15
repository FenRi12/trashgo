from aiogram import Router, types
from keyboards import main_menu

router = Router()

@router.message(lambda msg: msg.text == "💰 Тарифы")
async def tariffs(message: types.Message):
    text = "💳 Тарифы:\nРазовый — 13 000 сум\nМесячный — 300 000 сум"
    await message.answer(text, reply_markup=main_menu)

@router.message(lambda msg: msg.text == "ℹ️ Как это работает")
async def how_it_works(message: types.Message):
    text = ("Сервис «Выноса бытового мусора» - удобно, чисто и без хлопот!Не хотите выходить из дома, чтобы вынести мусор? Мы все сделаем за вас!Курьер заберет мусор от вашей двери и отнесет до ближайших мусорных контейнеров -аккуратно и в любое удобное для вас время.- Работаем с 7:00 до 23:00- Услуга для квартир, офисов, салонов красоты и др.")
    await message.answer(text, reply_markup=main_menu)

@router.message(lambda msg: msg.text == "📞 Связаться с оператором")
async def contact_operator(message: types.Message):
    text = "📞 Связаться с оператором: @TozaGo"
    await message.answer(text, reply_markup=main_menu)

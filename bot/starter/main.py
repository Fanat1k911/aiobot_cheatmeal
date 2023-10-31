import asyncio
import datetime
import logging
import os

import dotenv
from aiogram import Dispatcher, types, F, Bot
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from bot.settings import config

from bot.keyboards import keyboards
from bot.utils.make_report import Location

logging.basicConfig(level=logging.INFO)
dp = Dispatcher()
bot = Bot(token=config.TOKEN_API, parse_mode = 'HTML')

time_now = datetime.datetime.now().strftime('%H:%M')
today_now = datetime.datetime.date(datetime.datetime.now()).strftime('%d.%m.%Y')
data_day = [[f'Отчёт за {today_now}'],
['ОБЩАЯ ВЫРУЧКА:'],
['ИТОГО НАЛИЧНЫХ:'],

['КУПОЛ'],
['Наличные:'],
['Б/Н:'],
['Итого:'],
['Чеков:'],
['Ср. Чек:'],

['Итог по смене:'],

['Кассовая смена закрыта без расхождений;'],
['Размен есть;'],
['Зал убран;'],
['Телефон на зарядку поставлен;'],
['Менажницы наполнены;'],
['Технических неисправностей не было;'],
['Холодильники заполнены.']]
report = []

@dp.message(Command('start', 'Start'))
async def cmd_start(msg: types.Message) -> None:
    await msg.answer(f'<b>Привет, {msg.from_user.first_name.capitalize()}</b> 👋')


@dp.message(Command('reports', 'Reports'))
async def command_vision(msg: Message, state: FSMContext):
    await msg.answer('Выберите локацию продаж:', reply_markup=keyboards.inline_area_kb)
    await state.set_state(Location.choose_location)


@dp.message(Location.choose_location)
@dp.callback_query(F.data == 'poolbar_area')
async def to_poolbar(callback: CallbackQuery, state: FSMContext):
    await state.update_data(Poolbar='poolbar_area')
    await callback.answer('Выбрана локация <ПУЛБАР>')
    await callback.message.answer(f"Введите сумму БЕЗНАЛИЧНЫХ оплат:")
    await state.set_state(Location.nocash)


@dp.message(Location.choose_location)
@dp.callback_query(F.data == 'window_area')
async def to_poolbar(callback: CallbackQuery, state: FSMContext):
    await state.update_data(ЛОКАЦИЯ='Пулбар')
    await callback.answer('Выбрана локация <ОКОШКО>')
    await callback.message.answer(f"Введите сумму БЕЗНАЛИЧНЫХ оплат:")
    await state.set_state(Location.nocash)


@dp.message(Location.nocash)
async def get_no_cash(msg: Message, state: FSMContext):
    await state.update_data(БЕЗНАЛИЧНЫЕ=msg.text)
    user_data = await state.get_data()
    await msg.answer(f'Введите сумму НАЛИЧНЫХ оплат:')
    print(user_data)
    await state.set_state(Location.cash)


@dp.message(Location.cash)
async def set_cash(msg: Message, state: FSMContext):
    await state.update_data(НАЛИЧНЫЕ=msg.text)
    user_data = await state.get_data()
    print(user_data)
    await state.set_state(Location.more_report)
    # await msg.answer(f'Good! Были ли другие локации с прибылью?', reply_markup=keyboards.yes_or_no_kb)
    await msg.answer(f'Good! Были ли другие локации с прибылью?', reply_markup=keyboards.category_kb)


async def main():
    await dp.start_polling(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    dp.include_routers(choose_loc.router)


if __name__ == '__main__':
    asyncio.run(main())

# C:\Users\HomeMachine\Desktop\ngrok.exe http 8080
# Emoji : win+.
# botID = 6373698793
# from aiogram.enums.dice_emoji import DiceEmoji  - класс эмоджи игровая группа

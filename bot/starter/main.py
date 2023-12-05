import asyncio
import datetime
import logging
import os
from pprint import pprint

from aiogram import Dispatcher, types, F, Bot
from aiogram.filters import CommandStart
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.storage.memory import MemoryStorage

from aiobot_cheatmeal.bot.settings import config
from aiobot_cheatmeal.bot.keyboards import keyboards
from aiobot_cheatmeal.bot.utils.make_report import Location

logging.basicConfig(level=logging.INFO)
dp = Dispatcher()
bot = Bot(token=config.TOKEN_API, parse_mode='HTML')

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
Poolbar, Window, Curds, report = {}, {}, {}, {}
result_report = MemoryStorage()
result = {}


@dp.message(CommandStart())
async def cmd_start(msg: Message) -> None:
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
    await state.set_state(Location.poolbar_choosed)


@dp.message(Location.poolbar_choosed)
@dp.callback_query(F.data == 'poolbar_area')
async def poolbar_info(msg: Message, state: FSMContext):
    print('Все идет по плану, щас будем вводить суммы')
    if msg.text.isdigit():
        Poolbar['Отчёт за:'] = today_now
        Poolbar['Безналичные'] = msg.text
        # pbar.storage.update(Poolbar)
        print('Poolbar items >>>', Poolbar.items())
        await state.set_state(Location.cash)
        await msg.answer(f'Введите сумму НАЛИЧНЫХ оплат:')
    else:
        await msg.reply('Введите, пожалуйста, сумму цифрами без пробелов и знаков препинаний')


@dp.message(Location.cash)
@dp.callback_query(F.data == 'poolbar_area')
async def poolbar_to_cash(msg: Message, state: FSMContext):
    if msg.text.isdigit():
        Poolbar['Наличные'] = msg.text

        await result_report.update_data('Poolbar', Poolbar)
        result.update(Poolbar)

        await state.set_state(Location.any_report)
        await msg.answer(f'Good! Были ли другие локации с прибылью?',
                         reply_markup=keyboards.yes_or_no_kb)
    else:
        await msg.reply('Введите, пожалуйста, сумму цифрами без пробелов и знаков препинаний')


@dp.message(Location.any_report, F.text == 'ДА')
async def go_more_report(msg: Message, state: FSMContext):
    print('ЭТО БЫЛО "ДА"!', msg.text)
    await state.set_state(Location.choose_location)
    await msg.answer('Выберите локацию продаж:', reply_markup=keyboards.inline_area_kb)


@dp.message(Location.any_report, F.text == 'НЕТ')
async def go_more_report(msg: Message, state: FSMContext):
    await state.set_state(Location.wastes)
    print('Других локаций с прибылью не было')
    await msg.answer('Хорошо! Сегодня были траты наличных?', reply_markup=keyboards.yes_or_no_kb)


@dp.message(Location.wastes, F.text == 'ДА')
async def go_wastes(msg: Message, state: FSMContext):
    await state.set_state(Location.category_choosed)
    await msg.answer('Выберите категорию трат', reply_markup=keyboards.category_kb)

    print('result_report >>>', result_report.storage.items())
    print('result >>>', result.items())
    print(keyboards.inline_area_kb.model_dump()['inline_keyboard'][0][0][
              'callback_data'])  # TODO: доступ к кнопке получили, теперь нужно ее попробовать удалить из общего списка кнопок
    # for key, value in keyboards.inline_area_kb.dict().items():
    #     print(key, value)
    #     print()


# @dp.callback_query(F.data == 'Connection')
# async def fill_wastes(msg: Message, state: FSMContext):
#     print('Пришли к заполнению допонительных трат')


# TODO: разобраться как корректно фильтровать переход из одного состояния в другое
# TODO: попробовать разбить локации на разные файлы кода


async def main():
    await dp.start_polling(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    # dp.include_routers(choose_loc.router)


if __name__ == '__main__':
    asyncio.run(main())

# C:\Users\HomeMachine\Desktop\ngrok.exe http 8080
# Emoji : win+.
# botID = 6373698793
# from aiogram.enums.dice_emoji import DiceEmoji  - класс эмоджи игровая группа

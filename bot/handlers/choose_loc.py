from aiogram import Router,Dispatcher
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.keyboards.keyboards import inline_area_kb
from bot.utils.make_report import Location
from bot.starter.main import dp

# router_loc = Router()
#
# @dp.message(Command('reports', 'Reports'))
# async def command_vision(msg: Message, state: FSMContext):
#     await state.set_state(Location.Out_window)
#     await msg.answer('Выберите локацию продаж', reply_markup=inline_area_kb)

# @router_loc.message(CommandStart())
# async def command_start(message: Message, state: FSMContext) -> None:
#     await state.set_state(Location.Poolbar)
#     await message.answer("Hi there! What's your name?")

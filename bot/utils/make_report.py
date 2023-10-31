from aiogram.fsm.state import State, StatesGroup

choose_location = ['Poolbar', 'Window', 'Curds']


class Location(StatesGroup):
    choose_location = State()
    nocash = State()
    cash = State()
    more_report = State()

from aiogram.dispatcher.filters.state import StatesGroup, State


class mailing(StatesGroup):
    audit = State()
    text = State()
    confirming = State()

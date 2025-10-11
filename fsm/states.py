from aiogram.fsm.state import State, StatesGroup


class NewUser(StatesGroup):
    input_name = State()
    input_user_name = State()

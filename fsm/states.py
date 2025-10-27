from aiogram.fsm.state import State, StatesGroup


class NewReferral(StatesGroup):
    input_name = State()
    input_user_name = State()


class NewUser(StatesGroup):
    input_name = State()


class Slideshow(StatesGroup):
    running = State()

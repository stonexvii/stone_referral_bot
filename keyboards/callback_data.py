from aiogram.filters.callback_data import CallbackData


class UserMainMenu(CallbackData, prefix='UMM'):
    button: str


class BackButton(CallbackData, prefix='BB'):
    user_name: str

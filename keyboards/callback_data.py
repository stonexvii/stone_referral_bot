from aiogram.filters.callback_data import CallbackData


class UserMainMenu(CallbackData, prefix='UMM'):
    button: str


class ReferralMenu(CallbackData, prefix='RM'):
    button: str


class BackButton(CallbackData, prefix='BB'):
    button: str

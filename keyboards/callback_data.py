from aiogram.filters.callback_data import CallbackData


class CallbackMainMenu(CallbackData, prefix='CMM'):
    button: str


class CallbackReferral(CallbackData, prefix='CR'):
    button: str


class CallbackBackButton(CallbackData, prefix='CBB'):
    button: str


class CallbackWelcome(CallbackData, prefix='CW'):
    button: str


class CallbackProject(CallbackData, prefix='CP'):
    button: str

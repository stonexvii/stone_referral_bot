from collections import namedtuple

from .callback_data import CallbackMainMenu, CallbackReferral, CallbackBackButton, CallbackWelcome, CallbackProject

Button = namedtuple('Button', ['text', 'callback'])


class MainMenuButton:
    def __init__(self, text: str, url: str | None = None, button: str | None = None):
        self.text = text
        if button:
            self.callback_data = CallbackMainMenu(
                button=button,
            )
        if url:
            self.url = url

    def as_kwargs(self):
        return self.__dict__


class ReferralMenuButton:
    def __init__(self, text: str, button: str):
        self.text = text
        self.callback_data = CallbackReferral(
            button=button,
        )

    def as_kwargs(self):
        return self.__dict__


class BackButton:
    def __init__(self, text: str, button: str = 'to_main'):
        self.text = text
        self.callback_data = CallbackBackButton(
            button=button,
        )

    def as_kwargs(self):
        return self.__dict__


class WelcomeButton:
    def __init__(self, text: str, button: str):
        self.text = text
        self.callback_data = CallbackWelcome(
            button=button,
        )

    def as_kwargs(self):
        return self.__dict__


class ProjectButton:
    def __init__(self, text: str, button: str):
        self.text = text
        self.callback_data = CallbackProject(
            callback=button,
        )

    def as_kwargs(self):
        return self.__dict__

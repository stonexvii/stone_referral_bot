from database.tables import Project, Button
from .callback_data import CallbackMainMenu, CallbackReferral, CallbackBackButton, CallbackWelcome, CallbackProject


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
    def __init__(self, project: Project):
        self.text = project.button
        self.callback_data = CallbackProject(
            callback=project.name,
        )

    def as_kwargs(self):
        return self.__dict__


class ProjectInlineButton:
    def __init__(self, button: Button):
        self.text = button.text
        if button.callback:
            pass
        if button.url:
            self.url = button.url

    def as_kwargs(self):
        return self.__dict__

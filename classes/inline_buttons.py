from keyboards.callback_data import UserMainMenu


class UserMainMenuButton:
    def __init__(self, text: str, url: str | None = None, button: str | None = None):
        self.text = text
        if button:
            self.callback_data = UserMainMenu(
                button=button,
            )
        if url:
            self.url = url

    def as_kwargs(self):
        return self.__dict__

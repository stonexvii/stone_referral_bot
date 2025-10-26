from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.tables import Project
from .buttons import BackButton, ProjectInlineButton


def ikb_project_menu(project: Project):
    keyboard = InlineKeyboardBuilder()
    for button in project.buttons:
        keyboard.button(
            **ProjectInlineButton(button).as_kwargs()
        )
    keyboard.button(**BackButton('Назад', 'to_projects').as_kwargs())
    keyboard.adjust(1)
    return keyboard.as_markup()

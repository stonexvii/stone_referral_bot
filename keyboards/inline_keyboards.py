from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.tables import User, Menu, Project
from .buttons import MainMenuButton, ReferralMenuButton, BackButton, WelcomeButton, ProjectButton, PortfolioButton


def ikb_welcome(text: str, callback: str):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(**WelcomeButton(text, callback).as_kwargs())
    return keyboard.as_markup()


def ikb_main_menu(user: User):
    keyboard = InlineKeyboardBuilder()
    buttons = [
        MainMenuButton('⭐️ Кто такой Стоун? ⭐️', button='about_stone'),
        MainMenuButton('🛠 Проекты', button='projects'),
        MainMenuButton('Рефералы 💌', button='referrals_menu'),
        MainMenuButton('✉️ Написать в личку ✉️', url='https://t.me/STONE_XVII'),
    ]
    if user.tg_username:
        buttons.append(MainMenuButton('📲 Оставить заявку 📲', button='contact_stone'))
    for button in buttons:
        keyboard.button(**button.as_kwargs())

    keyboard.adjust(1, 2, 1, 1)
    return keyboard.as_markup()


def ikb_about_menu():
    keyboard = InlineKeyboardBuilder()
    buttons = [
        PortfolioButton('Портфолио', callback='portfolio'),
        MainMenuButton('Канал', url='https://t.me/stone_live'),
        MainMenuButton('Скачать PDF', button='download_pdf'),
        BackButton('Назад'),
    ]
    for button in buttons:
        keyboard.button(**button.as_kwargs())
    keyboard.adjust(1, 2, 1)
    return keyboard.as_markup()


def ikb_portfolio(trigger: bool, media_id: int, admin: bool):
    keyboard = InlineKeyboardBuilder()
    slide_show = {
        'text': 'Стоп' if trigger else 'Авто',
        'callback': 'stop_slideshow' if trigger else 'start_slideshow',
    }
    if trigger:
        buttons = [
            PortfolioButton(**slide_show),
            BackButton('Назад', 'to_about'),
        ]
    else:

        if admin:
            keyboard.button(**PortfolioButton('Удалить', 'delete_media', media_id).as_kwargs())
        buttons = [
            PortfolioButton(**slide_show),
            PortfolioButton('Дальше', 'portfolio'),
            BackButton('Назад', 'to_about'),
        ]
    for button in buttons:
        keyboard.button(**button.as_kwargs())
    keyboard.adjust(3, 1)
    return keyboard.as_markup()


def ikb_projects_menu(projects: list[Project]):
    keyboard = InlineKeyboardBuilder()
    buttons = [ProjectButton(project) for project in projects]
    buttons += [MainMenuButton('Канал', url='https://t.me/stone_live')]
    for button in buttons:
        keyboard.button(**button.as_kwargs())
    keyboard.button(**BackButton('Назад', 'to_main').as_kwargs())
    keyboard.adjust(1)
    return keyboard.as_markup()


def ikb_referrals_menu(user: User):
    keyboard = InlineKeyboardBuilder()
    if user.is_referral:
        buttons = [
            ReferralMenuButton('Мои рефералы', 'my_referrals'),
        ]
    else:
        buttons = [
            ReferralMenuButton('➕ Стать рефералом', 'new_referral'),
        ]
    buttons.append(BackButton('Назад'))
    for button in buttons:
        keyboard.button(**button.as_kwargs())
    keyboard.adjust(1)
    return keyboard.as_markup()


def ikb_back(target: str = 'to_main'):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(**BackButton('Назад', target).as_kwargs())
    return keyboard.as_markup()

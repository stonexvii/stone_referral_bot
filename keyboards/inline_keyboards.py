from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.tables import Users
from .buttons import MainMenuButton, ReferralMenuButton, BackButton, WelcomeButton, ProjectButton


def ikb_welcome(text: str, callback: str):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(**WelcomeButton(text, callback).as_kwargs())
    return keyboard.as_markup()


def ikb_main_menu(user: Users):
    keyboard = InlineKeyboardBuilder()
    buttons = [
        MainMenuButton('🎤 Кто такой Стоун? 🎤', button='about_stone'),
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
        MainMenuButton('Канал', url='https://t.me/stone_event'),
        MainMenuButton('Скачать PDF', button='download_pdf'),
        BackButton('Назад'),
    ]
    for button in buttons:
        keyboard.button(**button.as_kwargs())
    keyboard.adjust(3, 1)
    return keyboard.as_markup()


def ikb_projects_menu():
    keyboard = InlineKeyboardBuilder()
    buttons = [
        ProjectButton('💡 Разгоны 💡', 'dispersal'),
        ProjectButton('🛠 Ремонт мероприятий 🛠', 'event_fix'),
        ProjectButton('💀 Кошмары невест 💀', 'brides_nightmares'),
        MainMenuButton('Канал', url='https://t.me/stone_event'),
    ]
    for button in buttons:
        keyboard.button(**button.as_kwargs())
    keyboard.button(**BackButton('Назад', 'to_main').as_kwargs())
    keyboard.adjust(1)
    return keyboard.as_markup()


def ikb_dispersal_menu():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text='Ссылка на анкету',
        url='https://forms.gle/TBwUhnYvozhzcTiAA',
    )
    keyboard.button(**BackButton('Назад', 'to_projects').as_kwargs())
    keyboard.adjust(1)
    return keyboard.as_markup()


def ikb_event_fix():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text='Вызвать мастера',
        url='https://t.me/STONE_XVII',
    )
    keyboard.button(**BackButton('Назад', 'to_projects').as_kwargs())
    keyboard.adjust(1)
    return keyboard.as_markup()


def ikb_referrals_menu(user: Users):
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

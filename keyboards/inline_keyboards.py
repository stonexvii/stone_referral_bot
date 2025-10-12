from aiogram.utils.keyboard import InlineKeyboardBuilder

import config
from .buttons import UserMainMenuButton, Button
from .callback_data import ReferralMenu, BackButton


def ikb_user_main_menu():
    keyboard = InlineKeyboardBuilder()
    buttons = [
        UserMainMenuButton('ℹ️ Кто такой Стоун? ℹ️', url=config.CHANNEL_URL),
        UserMainMenuButton('💡 Разгоны', button='dispersal_of_events'),
        UserMainMenuButton('Рефералы 💰', button='referrals'),
        UserMainMenuButton('✉️ Связь со Стоуном ✉️', button='contact_stone'),
    ]
    for button in buttons:
        keyboard.button(**button.as_kwargs())

    keyboard.adjust(1, 2, 1)
    return keyboard.as_markup()


def ikb_referrals_menu():
    keyboard = InlineKeyboardBuilder()
    buttons = [
        Button('Твои рефералы', ReferralMenu(
            button='my_referrals'
        ),
               ),
        Button('Назад', BackButton(
            button='to_main',
        ),
               ),
    ]
    for button in buttons:
        keyboard.button(
            text=button.text,
            callback_data=button.callback,
        )
    keyboard.adjust(1)
    return keyboard.as_markup()


def ikb_dispersal_menu():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text='Ссылка на анкету',
        url='https://forms.gle/TBwUhnYvozhzcTiAA',
    )
    keyboard.button(
        text='Назад',
        callback_data=BackButton(
            button='to_main',
        ),
    )
    return keyboard.as_markup()


def ikb_back(to_menu: str = 'to_main'):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text='Назад',
        callback_data=BackButton(
            button=to_menu,
        )
    )
    return keyboard.as_markup()

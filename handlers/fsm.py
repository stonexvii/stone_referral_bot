from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from datetime import date

import config
# from classes import FileManager
from database import requests
from database.tables import Users
from fsm import NewUser
from keyboards import ikb_user_main_menu

fsm_router = Router()


@fsm_router.message(NewUser.input_name)
async def input_user_name(message: Message, state: FSMContext):
    data = await state.get_data()
    if message.from_user.username:
        user = await requests.new_user(
            user_tg_id=message.from_user.id,
            user_name=message.text,
            tg_user_name='@' + message.from_user.username,
            register_date=date.today(),
            referral_id=data['referral_id'],
        )
        message_text = f'Привет, {user.user_name}!\nВот твоя реферальная ссылка:\n{config.REFERRAL_LINK_BASE}{message.from_user.id}\n\nДелись ей со своими друзьями! Они получат скидку от меня, а ты получишь кэшбек от сделки'
        keyboard = ikb_user_main_menu()
        await state.clear()
    else:
        await state.set_state(NewUser.input_user_name)
        await state.update_data(
            {
                'user_name': message.text,
            }
        )
        message_text = 'Telegram не даёт мне доступ к твоему нику в телеграм\nУкажи его самостоятельно, пожалуйста\n(или ссылку на свой канал)'
        keyboard = None
    await message.answer(
        text=message_text,
        reply_markup=keyboard,
    )


@fsm_router.message(NewUser.input_user_name)
async def input_user_name(message: Message, state: FSMContext):
    tg_user_name = message.text
    if tg_user_name.startswith('http'):
        tg_user_name = '@' + tg_user_name.rsplit('/', 1)[-1]
    elif not tg_user_name.count('@'):
        tg_user_name = '@' + message.text
    data = await state.get_data()
    user = await requests.new_user(
        user_tg_id=message.from_user.id,
        user_name=data['user_name'],
        tg_user_name=tg_user_name,
        register_date=date.today(),
        referral_id=data['referral_id'],
    )
    message_text = f'Привет, {user.user_name}!\nВот твоя реферальная ссылка:\n{config.REFERRAL_LINK_BASE}{message.from_user.id}\n\nДелись ей со своими друзьями! Они получат скидку от меня, а ты получишь кэшбек от сделки'
    keyboard = ikb_user_main_menu()
    await message.answer(
        text=message_text,
        reply_markup=keyboard,
    )
    await state.clear()
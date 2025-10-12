from datetime import date

from aiogram import Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

import config
from database import requests
from fsm import NewUser
from utils import FileManager
from .inline import main_menu
from config

fsm_router = Router()


@fsm_router.message(NewUser.input_name)
async def input_user_name(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    if message.from_user.username:
        user = await requests.new_user(
            user_tg_id=message.from_user.id,
            user_name=message.text,
            tg_user_name='@' + message.from_user.username,
            register_date=date.today(),
            referral_id=data['referral_id'],
        )
        await state.clear()
        await main_menu(message, user, bot)
        await bot.send_message(
            chat_id=config.ADMIN_TG_ID,
            text=f'У нас новый реферал: {message.text} (@{message.from_user.username})'
        )

    else:
        await state.set_state(NewUser.input_user_name)
        await state.update_data(
            {
                'user_name': message.text,
            }
        )
        message_text = await FileManager.read('input_user_name', name=message.text)
        await message.answer(
            text=message_text,
        )


@fsm_router.message(NewUser.input_user_name)
async def input_user_name(message: Message, state: FSMContext, bot: Bot):
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
    await bot.send_message(
        chat_id=config.ADMIN_TG_ID,
        text=f'У нас новый реферал: {data['user_name']} ({tg_user_name})'
    )
    await state.clear()
    await main_menu(message, user, bot)

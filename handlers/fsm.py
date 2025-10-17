from datetime import date

from aiogram import Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InputMediaPhoto

import config
from database import requests
from database.tables import Users
from fsm.states import NewReferral
from utils import FileManager
from .main_menu import message_main_menu
import messages
from keyboards import ikb_back
from middlewares.middleware import UserMiddleware

fsm_router = Router()
fsm_router.message.middleware(UserMiddleware())


@fsm_router.message(NewReferral.input_name)
async def input_name(message: Message, state: FSMContext, user: Users, bot: Bot):
    data = await state.get_data()
    if message.from_user.username:
        await requests.new_referral(
            user_tg_id=message.from_user.id,
            name=message.from_user.full_name,
            tg_username=message.from_user.username,
        )
        # user = await requests.new_user(
        #     user_tg_id=message.from_user.id,
        #     user_name=message.text,
        #     tg_user_name='@' + message.from_user.username,
        #     register_date=date.today(),
        #     referral_id=data['referral_id'],
        # )
        await bot.delete_message(
            chat_id=message.from_user.id,
            message_id=message.message_id,
        )
        await message_main_menu(message, user, state, bot)
        await bot.send_message(
            chat_id=config.ADMIN_TG_ID,
            text=f'У нас новый реферал: {message.text} (@{message.from_user.username})'
        )

    else:
        await state.set_state(NewReferral.input_user_name)
        await state.update_data(
            {
                'user_name': message.text,
            }
        )
        msg_text = await FileManager.read('input_user_name', name=message.text)
        await bot.edit_message_media(
            chat_id=message.from_user.id,
            message_id=message.message.message_id,
            media=InputMediaPhoto(
                media=messages.NO_USER_NAME,
                caption=msg_text,
            ),
            reply_markup=ikb_back(),
        )


@fsm_router.message(NewReferral.input_user_name)
async def input_username(message: Message, state: FSMContext, user: Users, bot: Bot):
    tg_user_name = message.text
    if tg_user_name.startswith('http'):
        tg_user_name = '@' + tg_user_name.rsplit('/', 1)[-1]
    elif not tg_user_name.count('@'):
        tg_user_name = '@' + message.text
    data = await state.get_data()
    user = await requests.new_user(
        user_tg_id=message.from_user.id,
        name=data['user_name'],
        tg_username=tg_user_name,
        register_date=date.today(),
        referral_id=user.referral_id,
    )
    await bot.send_message(
        chat_id=config.ADMIN_TG_ID,
        text=f'У нас новый реферал: {data['user_name']} ({tg_user_name})'
    )
    await state.clear()
    await main_menu(message, user, bot)

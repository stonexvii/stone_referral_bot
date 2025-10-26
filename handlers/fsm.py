from aiogram import Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

import config
from database import requests
from database.tables import User
from fsm.states import NewReferral
from middlewares.middleware import UserMiddleware
from .main_menu import message_main_menu

fsm_router = Router()
fsm_router.message.middleware(UserMiddleware())


@fsm_router.message(NewReferral.input_name)
async def input_name(message: Message, state: FSMContext, user: User, bot: Bot):
    await requests.new_referral(
        user_tg_id=message.from_user.id,
        name=message.from_user.full_name,
        tg_username=message.from_user.username,
    )
    await bot.delete_message(
        chat_id=message.from_user.id,
        message_id=message.message_id,
    )
    await message_main_menu(message, user, state, bot)
    await bot.send_message(
        chat_id=config.ADMIN_TG_ID,
        text=f'У нас новый реферал: {message.text} (@{message.from_user.username})'
    )

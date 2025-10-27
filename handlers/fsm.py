import asyncio

from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

import config
from database import requests
from database.tables import User
from fsm import NewReferral, Slideshow
from keyboards.callback_data import CallbackBackButton
from middlewares.middleware import UserMiddleware
from .inline.about import about_handler
from .main_menu import message_main_menu

fsm_router = Router()
fsm_router.message.middleware(UserMiddleware())


async def get_task(task_name: str):
    loop = asyncio.get_running_loop()
    for task in asyncio.all_tasks(loop):
        if task.get_name() == task_name:
            return task


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


@fsm_router.callback_query(CallbackBackButton.filter(F.button == 'to_about'), Slideshow.running)
async def back_button(callback: CallbackQuery, bot: Bot, state: FSMContext):
    task_name = await state.get_value('task_name')
    task = await get_task(task_name)
    task.cancel()
    await state.clear()
    await about_handler(callback, bot)

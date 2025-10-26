from aiogram import Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, InputMediaPhoto

from database import requests
from database.tables import User
from keyboards import ikb_main_menu
from middlewares.middleware import UserMiddleware
from utils import FileManager

inline_router = Router()
inline_router.callback_query.middleware(UserMiddleware())


async def callback_main_menu(callback: CallbackQuery, user: User, bot: Bot):
    # media = await FileManager.media_kwargs(
    #     text='main_menu',
    #     name=user.name,
    # )
    msg_data = await requests.get_menu(
        'main_menu',
        name=user.name,
    )
    await bot.edit_message_media(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        media=InputMediaPhoto(**msg_data),
        reply_markup=ikb_main_menu(user),
    )


async def message_main_menu(message: Message, user: User, state: FSMContext, bot: Bot):
    message_id = await state.get_value('message_id')
    # media = await FileManager.media_kwargs(
    #     text='main_menu',
    #     name=user.name,
    # )
    msg_data = await requests.get_menu(
        'main_menu',
        name=user.name,
    )
    await bot.edit_message_media(
        chat_id=message.from_user.id,
        message_id=message_id,
        media=InputMediaPhoto(**msg_data),
        reply_markup=ikb_main_menu(user),
    )
    await state.clear()

from aiogram import Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, InputMediaPhoto

from database.tables import Users
from keyboards import ikb_main_menu
from middlewares.middleware import UserMiddleware
from utils import FileManager

inline_router = Router()
inline_router.callback_query.middleware(UserMiddleware())


async def callback_main_menu(callback: CallbackQuery, user: Users, bot: Bot):
    media = await FileManager.media_kwargs(
        text='main_menu',
        name=user.name,
    )
    await bot.edit_message_media(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        media=InputMediaPhoto(**media),
        reply_markup=ikb_main_menu(user),
    )


async def message_main_menu(message: Message, user: Users, state: FSMContext, bot: Bot):
    message_id = await state.get_value('message_id')
    media = await FileManager.media_kwargs(
        text='main_menu',
        name=user.name,
    )
    await bot.edit_message_media(
        chat_id=message.from_user.id,
        message_id=message_id,
        media=InputMediaPhoto(**media),
        reply_markup=ikb_main_menu(user),
    )
    await state.clear()

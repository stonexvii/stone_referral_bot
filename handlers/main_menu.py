from aiogram import Router, Bot, F
from aiogram.types import CallbackQuery, Message, InputMediaPhoto
from aiogram.fsm.context import FSMContext
import config
import messages
from database import requests
from database.tables import Users
from keyboards import ikb_back, ikb_main_menu, ikb_dispersal_menu, ikb_referrals_menu, ikb_about_menu
from keyboards.callback_data import CallbackMainMenu, CallbackReferral, CallbackBackButton
from middlewares.middleware import UserMiddleware
from utils import FileManager
from fsm.states import NewReferral

inline_router = Router()
inline_router.callback_query.middleware(UserMiddleware())


async def callback_main_menu(callback: CallbackQuery, user: Users, bot: Bot):
    msg_text = await FileManager.read('main_menu', name=user.name)
    await bot.edit_message_media(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        media=InputMediaPhoto(
            media=messages.MAIN_PICT,
            caption=msg_text,
        ),
        reply_markup=ikb_main_menu(),
    )


async def message_main_menu(message: Message, user: Users, state: FSMContext, bot: Bot):
    message_id = await state.get_value('message_id')
    msg_text = await FileManager.read('main_menu', name=user.name)
    await bot.edit_message_media(
        chat_id=message.from_user.id,
        message_id=message_id,
        media=InputMediaPhoto(
            media=messages.MAIN_PICT,
            caption=msg_text,
        ),
        reply_markup=ikb_main_menu(),
    )
    await state.clear()

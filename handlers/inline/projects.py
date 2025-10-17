from aiogram import Router, Bot, F
from aiogram.types import CallbackQuery, Message, InputMediaPhoto
from aiogram.fsm.context import FSMContext
import config
import messages
from database import requests
from database.tables import Users
from keyboards import ikb_back, ikb_main_menu, ikb_dispersal_menu, ikb_referrals_menu, ikb_about_menu, \
    ikb_projects_menu, ikb_event_fix
from keyboards.callback_data import CallbackMainMenu, CallbackReferral, CallbackBackButton, CallbackProject
from middlewares.middleware import UserMiddleware
from utils import FileManager
from fsm.states import NewReferral

projects_router = Router()


@projects_router.callback_query(CallbackMainMenu.filter(F.button == 'projects'))
async def projects_menu(callback: CallbackQuery, user: Users, bot: Bot):
    msg_text = await FileManager.read('projects')
    await bot.edit_message_media(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        media=InputMediaPhoto(
            media=messages.DISPERSAL_PICT,
            caption=msg_text,
        ),
        reply_markup=ikb_projects_menu(),
    )


@projects_router.callback_query(CallbackProject.filter(F.button == 'dispersal'))
async def dispersal_handler(callback: CallbackQuery, user: Users, bot: Bot):
    msg_text = await FileManager.read('dispersal')
    await bot.edit_message_media(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        media=InputMediaPhoto(
            media=messages.DISPERSAL_PICT,
            caption=msg_text,
        ),
        reply_markup=ikb_dispersal_menu(),
    )


@projects_router.callback_query(CallbackProject.filter(F.button == 'event_fix'))
async def dispersal_handler(callback: CallbackQuery, user: Users, bot: Bot):
    msg_text = await FileManager.read('event_fix')
    await bot.edit_message_media(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        media=InputMediaPhoto(
            media=messages.EVENT_FIX,
            caption=msg_text,
        ),
        reply_markup=ikb_event_fix(),
    )


@projects_router.callback_query(CallbackProject.filter(F.button == 'brides_nightmares'))
async def dispersal_handler(callback: CallbackQuery, user: Users, bot: Bot):
    await callback.answer(
        text='Проект в разработке\nСкоро релиз!\nСледите за новостями в канале',
        show_alert=True,
    )
    # msg_text = await FileManager.read('event_fix')
    # await bot.edit_message_media(
    #     chat_id=callback.from_user.id,
    #     message_id=callback.message.message_id,
    #     media=InputMediaPhoto(
    #         media=messages.EVENT_FIX,
    #         caption=msg_text,
    #     ),
    #     reply_markup=ikb_event_fix(),
    # )

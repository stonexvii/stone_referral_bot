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

about_router = Router()
about_router.callback_query.middleware(UserMiddleware())


@about_router.callback_query(CallbackMainMenu.filter(F.button == 'about_stone'))
async def about_handler(callback: CallbackQuery, user: Users, bot: Bot):
    msg_text = await FileManager.read('about')
    await bot.edit_message_media(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        media=InputMediaPhoto(
            media=messages.ABOUT_PICT,
            caption=msg_text,
        ),
        reply_markup=ikb_about_menu(),
    )


@about_router.callback_query(CallbackMainMenu.filter(F.button == 'download_pdf'))
async def download_handler(callback: CallbackQuery, user: Users, bot: Bot):
    await callback.answer(
        text='PDF в разработке!\nБудет доступно позже',
        show_alert=True,
    )


@about_router.callback_query(CallbackMainMenu.filter(F.button == 'contact_stone'))
async def contact_stone(callback: CallbackQuery, user: Users, bot: Bot):
    referral_user = await requests.get_user(user.referral_id)
    await bot.send_message(
        chat_id=config.ADMIN_TG_ID,
        text=f'{user.name} кинул заявку\n' + (
            f'Его привел: {referral_user.tg_username}\n' if referral_user else '') + f'@{user.tg_username}'
    )
    await callback.answer(
        text='Спасибо!\nМы передали Стоуну твою заявку, скоро он с тобой свяжется',
        show_alert=True,
    )
